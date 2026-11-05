#!/usr/bin/env python3
"""Browser QA (headless Chromium via Playwright). Run after build.py and qa.py:

    pip install playwright && python3 -m playwright install chromium
    python3 _build/qa_browser.py [--axe path/to/axe.min.js]

Checks the opening animation (landing on any page, once per session, #hash and reduced-motion skips),
the house wired as you scroll (circuits, rooms, HUD, messages, estimate card at the end), menus, form validation,
the instant electrical estimate end to end (prices recalculated here from site.config.json and compared with what
the page shows), console errors and horizontal overflow on phones.
With --axe, runs axe-core (WCAG 2.1 A/AA) on key pages. Exits non-zero on failures."""
import asyncio, functools, http.server, socketserver, threading, json, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
E = CFG.get("estimator") or {}
AXE = sys.argv[sys.argv.index("--axe") + 1] if "--axe" in sys.argv else None
res = []
def rec(ok, msg, extra=""): res.append(("PASS" if ok else "FAIL", msg + (f"  [{extra}]" if extra and not ok else "")))

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (ConnectionResetError, BrokenPipeError): pass
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 8822), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = "http://127.0.0.1:8822"
OFFERED = CFG.get("services") or []
SVC_PAGE = f"/services/{OFFERED[0]}/" if OFFERED else "/services/"
SVC_CITY = f"/services/{OFFERED[0]}/windsor/" if OFFERED and os.path.exists(os.path.join(ROOT, f"services/{OFFERED[0]}/windsor")) else None

def expected(job, values=None):
    """Recompute a job's range from the config, independently of estimate.js."""
    j = next(x for x in E["jobs"] if x["id"] == job)
    values = values or {}
    base, units, mult, adds = j.get("base", 0), 0, 1, 0
    for i in j["inputs"]:
        v = values.get(i["id"])
        if i["type"] == "range":
            v = i["default"] if v is None else v; units += i.get("per_unit", 0) * max(0, v - i.get("free_units", 0))
        elif i["type"] == "count":
            v = i.get("default", 0) if v is None else v; units += i.get("per_unit", 0) * v
        elif i["type"] == "choice":
            o = next((x for x in i["options"] if x["id"] == v), i["options"][0]); adds += o.get("add", 0); mult *= o.get("mult", 1)
        elif v:
            adds += i.get("add", 0)
    mid = base + adds + units * mult
    pct, r, mn = E.get("range_pct", 15) / 100, E.get("round_to", 25), E.get("minimum_job", 0)
    rnd = lambda n: int(round(n / r) * r)
    lo, hi = max(mn, rnd(mid * (1 - pct))), max(mn, rnd(mid * (1 + pct)))
    if hi <= lo: hi = lo + r
    return f"${lo:,}", f"${hi:,}"

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        errors = []
        async def page(w=1440, h=900, reduced=False, seen=True):
            ctx = await br.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
            if seen: await ctx.add_init_script("try{sessionStorage.setItem('el-intro','1')}catch(e){}")
            pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            return ctx, pg

        # ---- opening animation
        if CFG.get("intro", True):
            land = SVC_PAGE if CFG.get("intro_scope", "all") == "all" else "/"
            ctx, pg = await page(seen=False)
            await pg.goto(B + land, wait_until="commit"); await pg.wait_for_timeout(700)
            showing = await pg.evaluate("!!document.querySelector('.intro') && !document.documentElement.classList.contains('no-intro')")
            reading = await pg.evaluate("document.querySelectorAll('.intro .ib__b').length")
            await pg.wait_for_timeout(4800)
            gone = await pg.evaluate("!document.querySelector('.intro') && document.documentElement.classList.contains('is-ready')")
            rec(showing and gone, f"Opening animation plays when landing on {land} and clears itself", f"showing={showing} gone={gone}")
            rec(reading == 12, "Intro panel has 12 breakers to flip on", f"parts={reading}")
            await pg.goto(B + "/about/", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro does not replay on the next page in the same session")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/#faq-title", wait_until="commit"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped when the URL has a #hash")
            await ctx.close()
            ctx, pg = await page(seen=False, reduced=True)
            await pg.goto(B + "/"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.documentElement.classList.contains('no-intro')"), "Intro skipped for reduced motion")
            await ctx.close()
            ctx, pg = await page(seen=False)
            await pg.goto(B + "/", wait_until="commit"); await pg.wait_for_timeout(500)
            await pg.mouse.click(10, 500); await pg.wait_for_timeout(2400)
            rec(await pg.evaluate("!document.querySelector('.intro')"), "A click skips the intro")
            await ctx.close()

        # ---- home: the house wired as you scroll
        ctx, pg = await page()
        await pg.goto(B + "/"); await pg.wait_for_timeout(1500)
        if CFG.get("house_scene", True):
            live = await pg.evaluate("document.documentElement.classList.contains('house-live') && getComputedStyle(document.querySelector('.house__pin')).position==='sticky'")
            dark = await pg.evaluate("document.querySelectorAll('.house .room.is-lit').length")
            await pg.evaluate("window.__houseSeek(0.5)"); await pg.wait_for_timeout(500)
            mid = await pg.evaluate("[document.querySelectorAll('.house .room.is-lit').length, document.querySelectorAll('.house .wire.is-on').length, parseInt(document.querySelector('.house__load b').textContent,10), document.querySelector('.house__name').textContent]")
            await pg.evaluate("window.__houseSeek(0.99)"); await pg.wait_for_timeout(1200)
            end = await pg.evaluate("[document.querySelectorAll('.house .room.is-lit').length, document.querySelectorAll('.house .wire').length, document.querySelectorAll('.house .wire.is-on').length, document.querySelector('[data-house]').classList.contains('is-end'), !!document.querySelector('.hmsg--final.is-on'), getComputedStyle(document.querySelector('.hero.house .hero__est')).opacity, document.querySelectorAll('.house__brk li.is-on').length]")
            rec(live and dark == 0 and 1 <= mid[0] < end[1] and mid[2] > 0 and end[0] == end[1] and end[2] == end[1] and end[3] and end[4] and float(end[5]) > 0.9 and end[6] == await pg.evaluate("document.querySelectorAll('.house__brk li').length"),
                "House scene: pinned, starts dark, circuits trace and rooms light up in turn, all on at the end with the final message and the estimate card",
                f"live={live} dark={dark} mid={mid} end={end}")
            await pg.evaluate("window.__houseSeek(0)"); await pg.wait_for_timeout(300)
            ctx2, pg2 = await page(reduced=True)
            await pg2.goto(B + "/"); await pg2.wait_for_timeout(600)
            st = await pg2.evaluate("[getComputedStyle(document.querySelector('.hero.house')).height, innerHeight, getComputedStyle(document.querySelector('.house .room .glow')).opacity]")
            rec(float(st[0][:-2]) < st[1] * 1.6 and st[2] == "1", "Reduced motion: hero not pinned, house shown fully powered", f"{st}")
            await ctx2.close()
        if E.get("enabled", True):
            jobs = [j for j in E["jobs"] if not j.get("service") or j["service"] in OFFERED]
            await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(200)
            if len(jobs) > 1:
                await pg.check(f'.hero .picker input[value="{jobs[1]["id"]}"]', force=True)
                await pg.click(".hero .picker__go"); await pg.wait_for_load_state(); await pg.wait_for_timeout(400)
                chosen = await pg.evaluate("(document.querySelector('#est-form input[name=job]:checked')||{}).value")
                rec("electrical-estimate" in pg.url and chosen == jobs[1]["id"], "Hero job picker opens the estimate with that job selected", f"url={pg.url} chosen={chosen}")
        await ctx.close()

        # ---- instant estimate
        if E.get("enabled", True):
            jobs = [j for j in E["jobs"] if not j.get("service") or j["service"] in OFFERED]
            ctx, pg = await page()
            await pg.goto(B + "/electrical-estimate/"); await pg.wait_for_timeout(400)
            async def shown():
                return [await pg.text_content("#est-low"), await pg.text_content("#est-high")]
            bad = []
            for j in jobs:
                await pg.check(f'#est-form input[name=job][value="{j["id"]}"]', force=True); await pg.wait_for_timeout(80)
                if await shown() != list(expected(j["id"])): bad.append(f'{j["id"]} default {await shown()} vs {expected(j["id"])}')
                vis = await pg.evaluate(f"[!document.querySelector('.job[data-job=\"{j['id']}\"]').hidden, document.querySelectorAll('.job:not([hidden])').length, !document.querySelector('.est-art[data-art=\"{j['id']}\"]').hidden]")
                if vis != [True, 1, True]: bad.append(f'{j["id"]} panel/preview {vis}')
                vals = {}
                for i in j["inputs"]:
                    k = f'{j["id"]}-{i["id"]}'
                    if i["type"] == "range":
                        v = i["max"] - i.get("step", 1) * 2; vals[i["id"]] = v
                        await pg.fill(f"#i-{k}", str(v))
                    elif i["type"] == "count":
                        await pg.click(f'#i-{k} ~ .stepper__b[data-step="1"]'); await pg.click(f'#i-{k} ~ .stepper__b[data-step="1"]')
                        vals[i["id"]] = i.get("default", 0) + 2
                    elif i["type"] == "choice":
                        o = i["options"][-1]; vals[i["id"]] = o["id"]
                        await pg.check(f'input[name="{k}"][value="{o["id"]}"]', force=True)
                    else:
                        vals[i["id"]] = True; await pg.check(f'input[name="{k}"]', force=True)
                await pg.wait_for_timeout(80)
                if await shown() != list(expected(j["id"], vals)): bad.append(f'{j["id"]} options {await shown()} vs {expected(j["id"], vals)}')
            rec(not bad, f"Estimate matches the config for all {len(jobs)} jobs, at defaults and with every option changed", "; ".join(bad[:4]))
            nj = next(((j, i, o) for j in jobs for i in j["inputs"] if i["type"] == "choice" for o in i["options"] if o.get("note")), None)
            if nj:
                j, i, o = nj
                await pg.check(f'#est-form input[name=job][value="{j["id"]}"]', force=True)
                await pg.check(f'input[name="{j["id"]}-{i["id"]}"][value="{o["id"]}"]', force=True); await pg.wait_for_timeout(100)
                rec(o["note"] in (await pg.text_content("#est-notes")), f"Option notes appear in the result card ({j['label']}: {o['label']})")
            await pg.click("#est-lead-open"); await pg.wait_for_timeout(600)
            fields = await pg.evaluate("Object.fromEntries([...document.querySelectorAll('#est-lead input[type=hidden]')].map(i=>[i.name,i.value]))")
            rec(not await pg.evaluate("document.getElementById('est-lead').hidden") and fields.get("Job") and fields.get("Details") and "$" in fields.get("Estimate shown", ""),
                "Lead form opens with the job, the chosen options and the estimate filled in", json.dumps(fields)[:200])
            await pg.click("#est-lead button[type=submit]"); await pg.wait_for_timeout(300)
            rec(await pg.evaluate("document.querySelector('#est-lead .form__status').classList.contains('is-visible') && document.activeElement.id==='lead-name'"), "Empty estimate form shows errors and focuses the first field")
            await ctx.close()
            ctx, pg = await page(390, 844)
            await pg.goto(B + "/electrical-estimate/"); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('.job:not([hidden])').scrollIntoView()"); await pg.wait_for_timeout(700)
            rec(await pg.evaluate("document.getElementById('est-live').classList.contains('is-visible')"), "Phones: live price bar shows while the result card is off screen")
            await ctx.close()

        # ---- contact form validation
        ctx, pg = await page()
        await pg.goto(B + "/contact/"); await pg.click(".form button[type=submit]"); await pg.wait_for_timeout(200)
        rec(await pg.evaluate("document.querySelector('.form .form__status').classList.contains('is-visible') && document.querySelectorAll('.form [aria-invalid=true]').length>=5"), "Contact form: empty submit shows errors on required fields")
        await pg.fill("#email", "not-an-email"); await pg.click(".form button[type=submit]")
        rec("valid email" in (await pg.text_content("#email-error")), "Contact form: invalid email message")
        await ctx.close()

        # ---- phones: menu, overflow, call bar
        ctx, pg = await page(390, 844)
        over = []
        pages = ["/", "/electrical-estimate/", SVC_PAGE, "/services/", "/service-areas/", "/service-areas/windsor/", "/contact/", "/faq/", "/about/", "/privacy-policy.html", "/404.html"] + ([SVC_CITY] if SVC_CITY else [])
        for u in pages:
            await pg.goto(B + u); await pg.wait_for_timeout(250)
            if await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1"): over.append(u)
        rec(not over, f"No horizontal scrolling at 390px on {len(pages)} key pages", ", ".join(over))
        await pg.goto(B + "/"); await pg.click(".burger"); await pg.wait_for_timeout(800)
        rec(await pg.evaluate("document.getElementById('mobile-nav').classList.contains('is-open') && document.querySelector('.burger').getAttribute('aria-expanded')==='true'"), "Mobile menu opens from the burger button")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(300)
        await pg.evaluate("window.scrollTo(0,1400)"); await pg.wait_for_timeout(600)
        rec(await pg.evaluate("document.querySelector('.callbar').classList.contains('is-visible')"), "Mobile call bar appears after scrolling")
        await ctx.close()

        # ---- axe
        if AXE:
            src = open(AXE).read()
            ctx, pg = await page()
            for u in ["/", "/electrical-estimate/", SVC_PAGE, "/contact/", "/service-areas/windsor/"]:
                await pg.goto(B + u); await pg.wait_for_timeout(1500); await pg.add_script_tag(content=src)
                v = await pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21a','wcag21aa']}).then(r=>r.violations.map(v=>v.id+' ('+v.nodes.length+')'))")
                rec(not v, f"axe WCAG 2.1 AA on {u}: {len(v)} violations", ", ".join(v))
            await ctx.close()

        rec(not errors, f"No JavaScript errors in the console ({len(errors)})", " | ".join(errors[:4]))
        await br.close()
    for s, m in res: print(s, m)
    f = sum(1 for s, _ in res if s == "FAIL")
    print(f"\n{len(res) - f} passed, {f} failed")
    sys.exit(1 if f else 0)

asyncio.run(main())
