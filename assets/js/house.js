/* Electrician Template — the house wired as you scroll (home hero). No dependencies.
   The hero is pinned for several screens (main.css, HOUSE SCROLL SCENE). Scroll position becomes progress p (0-1):
     0.00-0.07  hero copy over the dark house
     0.07-0.15  power comes in from the pole: the service drop, meter and feed light up
     0.15-0.22  the main panel energizes, breakers flip on
     0.22-0.88  six circuits, one after another: the wire traces from the panel to the room, then the room lights up
     0.90+      everything is on, the final message and the estimate card appear
   The camera (the SVG viewBox) glides from room to room. Each circuit's wire gets --w (0-1) and each room
   gets .is-lit; the CSS does the rest. With reduced motion or no JavaScript the house is simply shown powered. */
(function () {
  "use strict";
  var sec = document.querySelector("[data-house]");
  var svg = sec && sec.querySelector("svg.house");
  if (!sec || !svg) return;
  var doc = document.documentElement;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  doc.classList.add("house-live");

  var circuits = [];
  try { circuits = (JSON.parse(sec.getAttribute("data-circuits")) || []).map(function (c) { return [c.id, c.n, c.d]; }); } catch (e) { circuits = []; }
  var ids = circuits.map(function (c) { return c[0]; });
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var smooth = function (t) { t = clamp(t); return t * t * (3 - 2 * t); };

  /* time slots for each circuit */
  var START = 0.07, ROOMS_FROM = 0.22, ROOMS_TO = 0.88, END = 0.9;
  var slots = {};
  var rooms = ids.filter(function (id) { return id !== "service" && id !== "panel"; });
  slots.service = [START, 0.15];
  slots.panel = [0.15, ROOMS_FROM];
  var step = (ROOMS_TO - ROOMS_FROM) / Math.max(1, rooms.length);
  rooms.forEach(function (id, i) { slots[id] = [ROOMS_FROM + i * step, ROOMS_FROM + (i + 1) * step]; });

  /* load each circuit adds to the HUD's amp counter (for show) */
  var LOAD = { service: 0, panel: 4, kitchen: 32, living: 9, bedrooms: 8, basement: 16, garage: 40, exterior: 34 };
  var MSG = { kitchen: 0, living: 1, basement: 2, garage: 3 };

  /* camera keyframes: [p, centre x, centre y, visible width] in drawing units (viewBox is 1600 x 900) */
  var CAM = { service: [330, 430, 1000], panel: [520, 770, 760], kitchen: [1000, 620, 920], living: [630, 620, 920],
    bedrooms: [800, 470, 1100], basement: [800, 780, 1080], garage: [1320, 620, 820], exterior: [760, 560, 1750] };
  var keys = function (mobile) {
    var k = [[0, mobile ? 820 : 600, mobile ? 560 : 520, mobile ? 1550 : 1900]];
    ids.forEach(function (id) {
      var s = slots[id], c = CAM[id]; if (!s || !c) return;
      var w = mobile ? Math.max(520, c[2] * 0.62) : c[2];
      if (id === "exterior") w = mobile ? 1150 : 1750;
      k.push([(s[0] + s[1]) / 2, c[0], c[1], w]);
    });
    k.push([END + 0.02, mobile ? 840 : 1250, mobile ? 520 : 520, mobile ? 1450 : 2150]);
    return k;
  };

  var el = function (sel) { return sec.querySelector(sel); };
  var wires = {}, roomEls = {};
  ids.forEach(function (id) {
    wires[id] = svg.querySelector('.wire[data-c="' + id + '"]');
    roomEls[id] = svg.querySelector('[data-room="' + id + '"]');
  });
  var svc = svg.querySelector('.svc'), panel = svg.querySelector('.panel');
  var hudCount = el(".house__count b"), hudName = el(".house__name"), hudDet = el(".house__detail"), hudLoad = el(".house__load b"), hudMeter = el(".house__meter b");
  var hudBrk = Array.prototype.slice.call(sec.querySelectorAll(".house__brk li"));
  var msgs = Array.prototype.slice.call(sec.querySelectorAll(".hmsg"));
  var lit = {};

  var setLit = function (id, on) {
    if (!!lit[id] === on) return;
    lit[id] = on;
    var r = roomEls[id];
    if (id === "service" && svc) svc.classList.toggle("is-on", on);
    if (r) {
      r.classList.toggle("is-lit", on);
      if (on && id !== "panel") { r.classList.remove("is-flick"); void r.getBoundingClientRect(); r.classList.add("is-flick"); }
    }
    if (wires[id]) wires[id].classList.toggle("is-on", on);
    hudBrk.forEach(function (li) { if (li.getAttribute("data-c") === id) li.classList.toggle("is-on", on); });
  };

  var cam = null, target = null, lastName = "", running = false, mobile = false, kf = keys(false);
  var p = 0;

  var update = function () {
    var r = sec.getBoundingClientRect(), vh = window.innerHeight;
    p = clamp(-r.top / Math.max(1, r.height - vh));
    if (window.__houseForce != null) p = window.__houseForce;
    sec.classList.toggle("is-start", p < START - 0.01);
    sec.classList.toggle("is-end", p >= END);
    svg.classList.toggle("is-all", p >= END);

    var load = 0, active = -1;
    ids.forEach(function (id, i) {
      var s = slots[id]; if (!s) return;
      var t = (p - s[0]) / (s[1] - s[0]);
      if (t >= 0 && t < 1) active = i;
      if (id === "service") {
        if (svc) svc.style.setProperty("--w", clamp(t / 0.8).toFixed(4));
        setLit(id, t >= 0.8);
      } else if (id === "panel") {
        setLit(id, t >= 0.45);
      } else {
        if (wires[id]) wires[id].style.setProperty("--w", clamp(t / 0.55).toFixed(4));
        setLit(id, t >= 0.55);
      }
      if (lit[id]) load += LOAD[id] || 0;
    });
    if (p >= END) active = ids.length - 1;

    var name, det, n;
    if (active < 0) { name = "Power off"; det = "Scroll to wire the house"; n = 0; }
    else if (p >= END) { name = "All circuits on"; det = "Permitted · inspected"; n = ids.length; }
    else { name = circuits[active][1]; det = circuits[active][2]; n = active + 1; }
    if (hudName && name !== lastName) { hudName.textContent = name; hudDet.textContent = det; lastName = name; }
    if (hudCount) hudCount.textContent = String(n).padStart(2, "0");
    if (hudLoad) hudLoad.textContent = String(load).padStart(3, "0");
    if (hudMeter) hudMeter.style.transform = "scaleX(" + clamp((p - START) / (END - START)).toFixed(4) + ")";

    /* messages */
    var showing = null;
    ids.forEach(function (id) {
      if (MSG[id] == null || !slots[id]) return;
      var t = (p - slots[id][0]) / (slots[id][1] - slots[id][0]);
      if (t >= 0.35 && t < 1.05) showing = String(MSG[id]);
    });
    if (p >= END) showing = "final";
    msgs.forEach(function (m) { m.classList.toggle("is-on", m.getAttribute("data-msg") === showing); });

    /* camera target */
    var a = kf[0], b = kf[kf.length - 1];
    for (var i = 0; i < kf.length - 1; i++) { if (p >= kf[i][0] && p <= kf[i + 1][0]) { a = kf[i]; b = kf[i + 1]; break; } }
    if (p >= kf[kf.length - 1][0]) a = b = kf[kf.length - 1];
    var t2 = a === b ? 1 : smooth((p - a[0]) / (b[0] - a[0]));
    target = [a[1] + (b[1] - a[1]) * t2, a[2] + (b[2] - a[2]) * t2, a[3] + (b[3] - a[3]) * t2];
    if (!cam) cam = target.slice();
    if (!running) { running = true; requestAnimationFrame(frame); }
  };

  /* where the camera's focus sits on screen: phones keep it below the messages, and higher at the end, above the estimate card */
  var anchor = function () {
    if (!mobile) return 0.5;
    var e = clamp((p - 0.86) / 0.06);
    return 0.6 - 0.32 * e;
  };
  var setView = function () {
    var w = svg.clientWidth || window.innerWidth, h = svg.clientHeight || window.innerHeight;
    var vw = cam[2], vhh = vw * h / w;
    svg.setAttribute("viewBox", (cam[0] - vw / 2).toFixed(1) + " " + (cam[1] - vhh * anchor()).toFixed(1) + " " + vw.toFixed(1) + " " + vhh.toFixed(1));
  };
  var frame = function () {
    var done = true;
    for (var i = 0; i < 3; i++) {
      var d = target[i] - cam[i];
      if (Math.abs(d) > 0.3) { cam[i] += d * 0.12; done = false; } else cam[i] = target[i];
    }
    setView();
    if (done) { running = false; return; }
    requestAnimationFrame(frame);
  };

  var onResize = function () { mobile = window.innerWidth < 900; kf = keys(mobile); cam = null; update(); };
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { ticking = false; var r = sec.getBoundingClientRect(); if (r.bottom > -50 && r.top < window.innerHeight + 50) update(); });
  }, { passive: true });
  window.addEventListener("resize", onResize);
  onResize();

  /* for automated checks: jump the scene to progress p (0-1) */
  window.__houseSeek = function (v) {
    var r = sec.getBoundingClientRect(), top = window.scrollY + r.top;
    window.scrollTo(0, top + v * (sec.offsetHeight - window.innerHeight));
    update();
  };
})();
