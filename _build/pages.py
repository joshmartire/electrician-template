# -*- coding: utf-8 -*-
# Copy for the home page and the standalone pages (about, FAQ, thank-you, legal).
# Items in HTML comments marked CLIENT REVIEW must be confirmed with the client before launch.

GENERAL_FAQS = [
("What areas do you serve?", "We do electrical work in {cities}. If your property is nearby but outside these communities, contact us and we'll let you know whether we can help."),
("How accurate is the instant electrical estimate?", "It's a ballpark range based on the job and the options you choose. Your panel, the wire route, wall types and access can change the final price, which is confirmed in writing after a site visit."),
("Do I need a permit for electrical work?", "In Ontario, most electrical work needs a permit (a notification) filed with the Electrical Safety Authority, and the work is inspected. We file it on every job that needs one."),
("How do I check that an electrician is licensed?", "In Ontario, a business doing electrical work for pay must hold an ESA Electrical Contractor Licence. Ask for the licence number and check it on ESA's website before you hire."),
("Do I need a panel upgrade for an EV charger?", "Not always. A load calculation shows what your panel can spare, and an EV energy management system often lets a charger share a smaller service safely."),
("Is knob and tube or aluminum wiring dangerous?", "Both can be safe when they're in good condition, but both have known weak points, and many insurers ask about them. An inspection tells you what you have and what it needs."),
("Why does my breaker keep tripping?", "Usually too much on one circuit, a faulty appliance or damaged wiring. If it trips again right after you reset it, leave it off and call an electrician."),
("What counts as an electrical emergency?", "Smoke, a burning smell, sparks, partial power loss, water near electrical equipment and storm damage to the service. If there's smoke or fire, call 911 first."),
("How long does a typical job take?", "Outlets, lights and repairs are often done in a few hours. EV chargers and panel upgrades usually take a day. Rewiring and renovations take longer, and we give you a schedule in writing."),
("What should I check before hiring any electrician?", "Check the ESA licence number, ask who files the permit, get the scope and price in writing, and ask for proof of liability insurance and WSIB coverage where applicable."),
("How do I get started?", "Use the instant electrical estimate for a ballpark number, call us, or send your details through our quote form. We'll follow up to book a visit."),
]

def _and(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def home(cfg, cities, services=None, all_offered=True):
    names = [c["name"] for c in cities]
    city_text = _and(names)
    d = {
        "desc": f"Electrician serving {city_text}: panel upgrades, EV chargers, rewiring, pot lights, generators, repairs, inspections and an instant estimate.",
        "eyebrow": f"Electrician · {cfg['region_label']}",
        "lead": "Panel upgrades, EV chargers, rewiring, lighting and repairs, done by licensed electricians, permitted on every job and inspected. See a ballpark for your job in about a minute.",
        # CLIENT REVIEW: confirm these badges describe how the client actually works.
        "tags": ["Permit filed on every job", "Written, itemized quotes", "Emergency calls answered"],
        # Scroll scene at the top of the home page (assets/js/house.js): a house is wired circuit by circuit as you
        # scroll. "circuits" label each stage in the HUD (id, name, detail); ids must match the drawing in
        # electric_art.house_svg(). "messages" appear one after another while the house powers up.
        "house": {
            "circuits": [
                ("service", "Service & meter", "Utility power in"),
                ("panel", "Main panel", "200 A · new breakers"),
                ("kitchen", "Kitchen", "Dedicated circuits · GFCI"),
                ("living", "Living room", "Pot lights · dimmers"),
                ("bedrooms", "Bedrooms", "Arc-fault protected"),
                ("basement", "Basement", "Sump pump · rec room"),
                ("garage", "Garage", "EV charger · 240 V"),
                ("exterior", "Outside", "Soffits · hot tub · surge"),
            ],
            "messages": [
                ("Safe for your family.", "Every circuit protected. Every connection tight."),
                ("Bright where it counts.", "Slim LED pot lights, laid out on a plan."),
                ("Ready for the storm.", "Sump pump on its own circuit, generator ready."),
                ("Ready for your EV.", "A dedicated 240 V circuit, sized for overnight charging."),
            ],
            "final": ("Powered.", "Safe. Inspected. Ready for what's next."),
        },
        "statement_eyebrow": "It starts behind the wall.",
        "statement": "Anyone can hang a light fixture. What keeps a home safe for decades is the part you never see: tight connections, the right wire for the load, protection on every circuit and a permit on every job. That's where we put the most care.",
        "statement_points": [
            ("Permitted and inspected", "We file the permit and the work is inspected, so you have the paperwork insurers and buyers ask for."),
            ("Priced in writing", "Parts, labour, permit and anything not included listed separately, so you can compare quotes properly."),
            ("Sized for what's next", "A load calculation before big additions, so the panel can carry the EV, the heat pump and the hot tub."),
        ],
        "services_lead": "Panels and power, wiring and lighting, and the repairs, inspections and commercial work that keep everything running. Pick a service to see what's included and what to ask before you hire.",
        # "warning signs" band: (icon, title, text). Shown on the home page with a call button.
        "signs": [
            ("heat", "Warm outlets or switches", "A cover plate that's warm to the touch usually means a loose or failing connection."),
            ("flicker", "Flickering or dimming", "Lights that dim when something starts, or flicker across the house, can point to the panel or service."),
            ("trip", "Breakers that keep tripping", "One trip is a warning. Repeated trips mean an overloaded or damaged circuit."),
            ("smell", "Burning smell or buzzing", "A hot plastic smell, buzzing or crackling needs an electrician today. Turn off the circuit if it's safe."),
            ("old", "Fuses, two-prong outlets, old panels", "Signs of wiring built for a different era, and the questions insurers ask."),
            ("spark", "Sparks or scorch marks", "Sparks when plugging in, or black marks on an outlet, mean stop using it now."),
        ],
        "process": [
            ("Estimate online", "Use the instant estimate for a ballpark, or call us. No pressure either way."),
            ("Site visit", "We look at your panel, the route and what you want, and answer your questions."),
            ("Quote in writing", "Parts, labour, permit and what isn't included, every line item, to review on your own time."),
            ("Install & inspect", "Clean, tidy work, the permit closed out and the paperwork in your hands."),
        ],
        "why_lead": "Electrical work is hidden once it's done, so you have to trust what's behind the wall. These are the standards every job runs on.",
        # CLIENT REVIEW: confirm these working standards with the client.
        "features": [
            ("Straight answers", "If a repair makes sense, we'll say so. If the panel needs replacing, we'll show you why."),
            ("Written, itemized quotes", "Parts, labour, permit and extras listed separately, every time."),
            ("Permits on every job", "Filed and inspected, with paperwork you can hand to your insurer or a buyer."),
            ("Clean, labelled work", "Tidy runs, every breaker labelled, drop sheets down and the mess cleaned up."),
        ],
        "faqs": [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS[1:5]],
    }
    if not all_offered and services:
        low = [x["name"].lower() for x in services]
        d["desc"] = f"Electrician serving {city_text}: " + (", ".join(low[:5]) + " and more." if len(low) > 5 else _and(low) + ".")
        if len(d["desc"]) > 158:
            d["desc"] = f"Electrician serving {city_text}: " + ", ".join(low[:3]) + " and more."
        d["services_lead"] = "Pick a service to see what's included, how the work runs and what to ask before you hire."
        d["lead"] = "Electrical work done by licensed electricians, permitted on every job and inspected. See a ballpark for your job in about a minute."
    return d


def simple_pages(cfg, cities, services, city_text, all_offered=True):
    biz = cfg["business_name"]
    offered = {x["slug"]: x for x in services}
    esa = cfg.get("inspection_short") or "ESA"
    lic = (cfg.get("licence_number") or "").strip()

    def links(slugs, limit=None):
        out = [f"[[{sl}|{offered[sl]['name'].lower()}]]" for sl in dict.fromkeys(slugs) if sl in offered]
        return out[:limit] if limit else out
    faqs = [(q.replace("{cities}", city_text), a.replace("{cities}", city_text)) for q, a in GENERAL_FAQS]
    est_on = (cfg.get("estimator") or {}).get("enabled", True)
    lic_line = (f"<p>{biz} is an {esa} Licensed Electrical Contractor, licence number {lic}. You can check it on {esa}'s website.</p>" if lic else
                "<!-- CLIENT INPUT NEEDED: add the client's ESA licence number in site.config.json (licence_number). It then appears here and in the footer. -->")

    def about(here):
        work = _and(links([x["slug"] for x in services], 6) or ["electrical work"])
        return f"""
<!-- CLIENT REVIEW: replace or extend with the client's real story: founding year, owner and master electrician names, crew, insurance and WSIB status, suppliers, warranties, memberships and real project photos. Do not add claims that can't be verified. -->
<h2>Who we are</h2>
<p>{biz} is an electrical contractor serving {city_text}. We work for homeowners, renovators and businesses, and our work includes {work}.</p>
{lic_line}
<p>Electrical work disappears behind the wall once it's done, so you have to trust what you can't see. That's why we explain what we're doing, put our prices in writing, file the permit and leave every panel labelled.</p>
<h2>How we work</h2>
<ul>
<li><strong>Permits on every job that needs one.</strong> Filed with {esa}, inspected, and the paperwork handed to you.</li>
<li><strong>Load calculations before big additions.</strong> So the panel can carry what you're adding.</li>
<li><strong>Clear, written quotes.</strong> Parts, labour, permit and anything that isn't included, spelled out.</li>
<li><strong>Respect for your home.</strong> Drop sheets, dust control, small patchable openings and a tidy site.</li>
</ul>
<h2>Where we work</h2>
<p>We work across {city_text}. Each community has its own housing and wiring, which we cover on our pages for [[area:{cities[0]['slug']}|{cities[0]['name']}]], [[area:{cities[1]['slug']}|{cities[1]['name']}]] and [[area:{cities[2]['slug']}|{cities[2]['name']}]].</p>
<h2>Before you hire anyone</h2>
<p>Whoever you choose, ask for their {esa} licence number and check it, ask who files the permit, and get the scope and price in writing, along with proof of liability insurance and WSIB coverage where applicable. Good electricians are glad to answer those questions. When you're ready, {"try our [[estimate|instant electrical estimate]] or " if est_on else ""}[[contact|request a quote]].</p>
"""

    def faq(here):
        out = '<h2>Frequently asked questions</h2><div class="faq">'
        for q, a in faqs:
            if "instant electrical estimate" in q.lower() and not est_on:
                continue
            out += f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{a}</p></div></details>'
        l = links(["panel-upgrades", "ev-charger-installation", "knob-and-tube-replacement", "pot-lights"] + [x["slug"] for x in services], 4) or ["our services"]
        out += '</div><h2>Service-specific questions</h2><p>Each service page answers common questions about that type of work. Start with ' + (
            l[0] if len(l) == 1 else ", ".join(l[:-1]) + " or " + l[-1]) + ', or browse [[services|all services]].</p>'
        return out

    def thanks(here):
        return f"""<h2>We've received your request</h2>
<p>Thanks for contacting {biz}. We'll review your details and follow up by phone or email to book a visit.</p>
<p>If something is sparking, smells like it's burning or you've lost power to part of the house, don't wait for our reply: call us at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>. If there's smoke or fire, call 911.</p>
<p>While you wait, you can browse [[services|our services]] or read our [[faq|frequently asked questions]].</p>"""

    tool_privacy = ""
    if est_on:
        tool_privacy = """<p><strong>Instant electrical estimate.</strong> The instant electrical estimate runs entirely in your web browser. The choices you make, such as the job type, distances and quantities, are not sent to us or to anyone else unless you choose to submit the estimate form.</p>"""

    def privacy(here):
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: This is a draft based on the website as built (quote and estimate forms via {cfg['form_provider_name']}, static hosting, estimate calculated in the browser, no analytics or advertising). Confirm actual data handling, retention periods, email provider and any CRM, financing or other tools before publishing. If analytics, advertising pixels, chat or booking tools are added, this policy must be updated. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>This Privacy Policy explains how {cfg['legal_name']} ("we", "us") collects, uses and protects personal information through this website and when you contact us about electrical services. We handle personal information in accordance with applicable Canadian privacy law, including the <em>Personal Information Protection and Electronic Documents Act</em> (PIPEDA).</p>
<h2>Information we collect</h2>
<p><strong>Information you give us.</strong> When you submit our quote form or send us an instant estimate, we collect your name, phone number, email address, property location or address, the service you're interested in and any details you choose to share. Estimate submissions also include the job type, the options you chose and the estimated price range shown to you. If you call or email us, we collect the information you provide in that conversation.</p>
{tool_privacy}
<p><strong>Technical information.</strong> When you visit, our hosting provider's servers may automatically log technical information such as your IP address and browser details for security and operational purposes. We do not use this website to collect analytics, and we do not use advertising or tracking cookies.</p>
<h2>How we use your information</h2>
<ul>
<li>To respond to your inquiry and book a visit.</li>
<li>To prepare quotes, contracts and work schedules, and to file electrical permits, request utility locates and coordinate with your utility for your project.</li>
<li>To communicate with you about your project before, during and after the work.</li>
<li>To handle warranty questions and to meet legal, accounting and tax obligations.</li>
</ul>
<p>We do not sell your personal information, and we do not use it for unrelated marketing without your consent.</p>
<h2>Who we share it with</h2>
<p>Quote and estimate requests submitted through this website are transmitted through {cfg['form_provider_name']}, a third-party form service that delivers submissions to our email. To complete your project, your name, address and project details may be shared with the Electrical Safety Authority for permits and inspections, your local electricity utility for disconnects and reconnects, the utility locate service, and suppliers or subcontractors when needed, and with professional advisors or authorities where required by law. Service providers we use may store or process information outside Canada, including in the United States and Europe, where it may be subject to the laws of those jurisdictions.</p>
<h2>How long we keep it</h2>
<p>We keep personal information only as long as needed for the purposes above, including any period required for legal, tax, permit or warranty reasons, and then securely delete or destroy it.</p>
<h2>How we protect it</h2>
<p>We use reasonable administrative, technical and physical safeguards appropriate to the sensitivity of the information. No method of transmission or storage is completely secure, so we cannot promise absolute security. Please don't include sensitive information, such as financial details, in our website forms.</p>
<h2>Your choices and rights</h2>
<p>You may ask to access the personal information we hold about you, ask us to correct it, or withdraw your consent to our use of it, subject to legal and contractual restrictions. To make a request, contact us using the details below. If you're not satisfied with our response, you may contact the Office of the Privacy Commissioner of Canada.</p>
<h2>Cookies</h2>
<p>This website does not set cookies. See our [[cookies|Cookie Policy]] for details on the limited browser storage the site uses.</p>
<h2>Contact us</h2>
<p>Questions about privacy can be sent to <a href="mailto:{cfg['privacy_contact']}">{cfg['privacy_contact']}</a> or by phone at <a href="tel:{cfg['phone_e164']}">{cfg['phone_display']}</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The effective date above shows when it was last changed.</p>
"""

    def terms(here):
        est = """<h2>Instant electrical estimates</h2>
<p>The instant electrical estimate is an automated ballpark calculated from the options you choose and our general pricing. It is not a quote or an offer. The actual price is confirmed only in a written quote after a site visit, and can differ because of your panel and service, the wire route, wall and ceiling types, access, code requirements found on site, utility charges and other factors.</p>
""" if est_on else ""
        return f"""
<!-- CLIENT REVIEW / LEGAL REVIEW REQUIRED: Draft website terms. Project-specific terms (payment schedules, deposits, warranties, cancellations) belong in the client's written contracts, not here. Have the limitation of liability and governing-law sections reviewed by a lawyer. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<p>These Terms and Conditions apply to your use of this website, operated by {cfg['legal_name']} ("we", "us"). By using the website, you agree to these terms.</p>
<h2>Use of this website</h2>
<p>You may use this website for lawful purposes, such as learning about our services and contacting us. You agree not to misuse the website, attempt to interfere with its operation, or submit false or misleading information through our forms.</p>
<h2>Information on this website</h2>
<p>Content on this website is general information about electrical services. It is not electrical, engineering or code-compliance advice for your specific property, and it is not a substitute for a licensed electrician. Electrical work can cause serious injury, fire or death if done incorrectly. Codes, permit requirements and utility rules change over time. While we try to keep information accurate and current, we don't warrant that it is complete or error-free.</p>
{est}<h2>Quotes and project agreements</h2>
<p>Nothing on this website is an offer, quote or contract. Pricing, scope, schedules, payment terms, warranties and cancellation terms for any project are set out only in a written quote or contract provided to you. If there is a conflict between this website and your written contract, the contract applies.</p>
<h2>Intellectual property</h2>
<p>The text, design, graphics and logos on this website belong to us or our licensors. You may view and print pages for personal, non-commercial use, but you may not copy, reproduce or republish website content for commercial purposes without our written permission.</p>
<h2>Third-party links and services</h2>
<p>This website may link to third-party websites or use third-party services, such as our form provider and the Electrical Safety Authority's website. We aren't responsible for the content, terms or privacy practices of those third parties.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any indirect or consequential loss arising from your use of this website or reliance on its general information or automated estimates. Nothing in these terms limits any rights you have under applicable consumer protection law.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the Province of {cfg['legal_jurisdiction']} and the federal laws of Canada that apply there.</p>
<h2>Changes and contact</h2>
<p>We may update these terms from time to time. Questions can be sent to <a href="mailto:{cfg['email']}">{cfg['email']}</a>. Our [[privacy|Privacy Policy]] explains how we handle personal information.</p>
"""

    def cookies(here):
        return f"""
<!-- CLIENT REVIEW: accurate for the template as built (no cookies, no analytics, no pixels; the instant estimate runs in the browser). If Google Analytics, Meta Pixel, Google Ads tags, chat widgets, financing or booking embeds are added, update this page and add a consent mechanism that blocks non-essential tags until the visitor agrees, where required. -->
<p><strong>Effective date:</strong> {cfg['policy_effective_date']}</p>
<h2>Does this website use cookies?</h2>
<p>No. This website does not set cookies, and it does not use analytics, advertising pixels or other tracking technologies.</p>
<h2>Browser storage we use</h2>
<p>The website uses your browser's <em>session storage</em> to remember that the opening animation has already played during your visit, so it isn't shown again on every page. This stores a single value with no personal information, isn't shared with us or anyone else, and is cleared automatically when you close your browser tab. Because it's needed only to provide the website as you'd expect, it doesn't require consent.</p>
<h2>Third-party services</h2>
<p>When you submit one of our forms, your browser sends it to {cfg['form_provider_name']}, which delivers it to us by email. That service may display its own pages, such as a spam-protection check, and may use cookies on its own domain under its own policies. Our hosting provider may log technical information such as IP addresses for security purposes, as explained in our [[privacy|Privacy Policy]].</p>
<h2>Managing storage</h2>
<p>You can clear or block site data at any time through your browser settings. The website will continue to work, although the opening animation may play again.</p>
<h2>Changes</h2>
<p>If we add tools that use cookies or similar technologies, we will update this policy and, where required, ask for your consent before those tools run.</p>
"""

    return {
        "about": dict(title=f"About {biz}", desc=f"{biz} is an electrical contractor serving {city_text}. How we quote, permit and wire, and what to ask any electrician.", eyebrow="About us", h1="About Us", lead="An electrical contractor built around straight answers, written prices and work that passes inspection the first time.", inner=about, active="about"),
        "faq": dict(title="Electrical FAQ", desc=f"Answers about electrical permits, ESA licences, panel upgrades, EV chargers, old wiring and hiring an electrician in {city_text}.", eyebrow="FAQ", h1="Frequently Asked Questions", lead="Straight answers about electrical work and how we do it, before you commit to anything.", inner=faq, active="faq"),
        "thanks": dict(title="Thank You", desc="Your request has been sent.", eyebrow="Request sent", h1="Thank You", lead="Your details are on their way to us.", inner=thanks, noindex=True, aside=False, cta=False, hero_ctas=False),
        "privacy": dict(title="Privacy Policy", desc=f"How {biz} collects, uses and protects personal information submitted through this website, its forms and the instant electrical estimate.", eyebrow="Legal", h1="Privacy Policy", lead="How we collect, use and protect your personal information.", inner=privacy, mark="doc", aside=False, cta=False, hero_ctas=False),
        "terms": dict(title="Terms and Conditions", desc=f"Terms and conditions for using the {biz} website and its instant electrical estimate.", eyebrow="Legal", h1="Terms and Conditions", lead="The terms that apply when you use this website.", inner=terms, mark="doc", aside=False, cta=False, hero_ctas=False),
        "cookies": dict(title="Cookie Policy", desc=f"How the {biz} website uses cookies and browser storage.", eyebrow="Legal", h1="Cookie Policy", lead="What this website stores in your browser, and what it doesn't.", inner=cookies, mark="doc", aside=False, cta=False, hero_ctas=False),
    }
