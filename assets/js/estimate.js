/* Electrician Template — instant electrical estimate (no dependencies).
   Prices come from site.config.json ("estimator"), embedded in the page as #est-config.
   Everything is calculated in the browser; nothing is sent until the visitor submits the lead form.
   Job total = (base + choice adds + check adds + unit-priced work x choice multipliers), where unit-priced work is
   each range input's per_unit x (value - free_units) plus each count input's per_unit x count.
   The result is shown as +/- range_pct, rounded to round_to and never below minimum_job. */
(function () {
  "use strict";
  var cfgEl = document.getElementById("est-config");
  var form = document.getElementById("est-form");
  if (!cfgEl || !form) return;
  var C = JSON.parse(cfgEl.textContent);
  var $ = function (id) { return document.getElementById(id); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-CA"); };
  var round = function (n) { var r = C.round_to || 25; return Math.round(n / r) * r; };
  var jobs = C.jobs || [];
  var byId = function (id) { for (var i = 0; i < jobs.length; i++) if (jobs[i].id === id) return jobs[i]; return jobs[0]; };
  var result = $("est-result"), low = $("est-low"), high = $("est-high"), sum = $("est-sum"), notes = $("est-notes"), incl = $("est-incl"), prevH = $("est-prev-h");

  /* deep link from the home page picker: ?job=ev */
  try {
    var q = new URLSearchParams(location.search).get("job");
    if (q) { var r = form.querySelector('input[name="job"][value="' + q.replace(/[^a-z0-9\-]/gi, "") + '"]'); if (r) r.checked = true; }
  } catch (e) {}

  var num = function (el, lo, hi, d) { var v = parseFloat(el && el.value); if (isNaN(v)) v = d; return Math.max(lo, Math.min(hi, v)); };

  /* exposed so the automated checks can compute the same thing */
  var compute = function (job, read) {
    var base = job.base || 0, units = 0, mult = 1, adds = 0, parts = [], noteList = [];
    job.inputs.forEach(function (inp) {
      var v = read(inp);
      if (inp.type === "range") {
        units += (inp.per_unit || 0) * Math.max(0, v - (inp.free_units || 0));
        parts.push(inp.label + ": " + v + " " + (inp.unit || ""));
      } else if (inp.type === "count") {
        units += (inp.per_unit || 0) * v;
        if (v) parts.push(inp.label + ": " + v);
      } else if (inp.type === "choice") {
        var o = inp.options.filter(function (x) { return x.id === v; })[0] || inp.options[0];
        adds += o.add || 0; if (o.mult) mult *= o.mult;
        if (o.note) noteList.push(o.note);
        parts.push(inp.label + ": " + o.label);
      } else if (inp.type === "check") {
        if (v) { adds += inp.add || 0; parts.push(inp.label); }
      }
    });
    var mid = base + adds + units * mult;
    var pct = (C.range_pct || 15) / 100, min = C.minimum_job || 0;
    var lo = Math.max(min, round(mid * (1 - pct))), hi = Math.max(min, round(mid * (1 + pct)));
    if (hi <= lo) hi = lo + (C.round_to || 25);
    return { lo: lo, hi: hi, mid: mid, parts: parts, notes: noteList };
  };
  window.__estCompute = function (jobId, values) {
    var job = byId(jobId);
    return compute(job, function (inp) {
      if (values && values[inp.id] != null) return values[inp.id];
      if (inp.type === "range") return inp["default"];
      if (inp.type === "count") return inp["default"] || 0;
      if (inp.type === "choice") return inp.options[0].id;
      return false;
    });
  };

  var readFrom = function (job) {
    var wrap = form.querySelector('.job[data-job="' + job.id + '"]');
    return function (inp) {
      var k = job.id + "-" + inp.id;
      if (inp.type === "range") return num($("i-" + k), inp.min, inp.max, inp["default"]);
      if (inp.type === "count") return num($("i-" + k), 0, inp.max || 20, 0);
      if (inp.type === "choice") { var c = wrap.querySelector('input[name="' + k + '"]:checked'); return c ? c.value : inp.options[0].id; }
      var cb = wrap.querySelector('input[name="' + k + '"]'); return !!(cb && cb.checked);
    };
  };

  var lastKey = "";
  var calc = function () {
    var jEl = form.querySelector('input[name="job"]:checked');
    var job = byId(jEl ? jEl.value : null);
    Array.prototype.forEach.call(form.querySelectorAll(".job"), function (w) { w.hidden = w.getAttribute("data-job") !== job.id; });
    Array.prototype.forEach.call(document.querySelectorAll(".est-art"), function (a) { a.hidden = a.getAttribute("data-art") !== job.id; });
    var read = readFrom(job);
    var res = compute(job, read);
    low.textContent = money(res.lo); high.textContent = money(res.hi);
    var lv = $("est-live-v"); if (lv) lv.textContent = money(res.lo) + " – " + money(res.hi);
    sum.textContent = job.label + " · " + res.parts.slice(0, 3).join(" · ");
    notes.innerHTML = "";
    res.notes.forEach(function (n) { var p = document.createElement("p"); p.textContent = n; notes.appendChild(p); });
    incl.textContent = job.includes ? "Includes " + job.includes + "." : "";
    var key = res.lo + "-" + res.hi;
    if (key !== lastKey) { result.classList.remove("is-new"); void result.offsetWidth; result.classList.add("is-new"); lastKey = key; }

    /* preview details */
    var art = document.querySelector('.est-art[data-art="' + job.id + '"]');
    var label = "";
    job.inputs.forEach(function (inp) {
      if (inp.type === "range" && !label) label = read(inp) + " " + (inp.unit || "").toUpperCase();
    });
    if (job.id === "potlights" && art) {
      var n = read(job.inputs.filter(function (i) { return i.type === "range"; })[0] || {});
      var rows = Math.max(1, Math.ceil(n / 10));
      Array.prototype.forEach.call(art.querySelectorAll(".ja-pot"), function (p) {
        var i = +p.getAttribute("data-i");
        p.classList.toggle("is-show", i < rows * 10);
        p.classList.toggle("is-on", i < n);
      });
    }
    if (job.id === "panel" && art) {
      var kind = read(job.inputs[0]); var on = kind === "replace" ? 6 : kind === "100-200" ? 8 : 10;
      Array.prototype.forEach.call(art.querySelectorAll(".ja-brk"), function (b, i) { b.classList.toggle("is-on", i < on); });
      var amp = art.querySelector(".ja-amp"); if (amp) amp.textContent = kind === "200-400" ? "400 A" : "200 A";
      label = "";
    }
    if (job.id === "outlets" && art) {
      var cnt = 0; job.inputs.forEach(function (i) { if (i.type === "count") cnt += read(i); });
      Array.prototype.forEach.call(art.querySelectorAll(".ja-out"), function (o, i) { o.classList.toggle("is-on", i < Math.min(5, cnt)); });
      label = cnt + " DEVICES";
    }
    if (prevH) prevH.textContent = label;

    /* keep the lead form's hidden fields in sync */
    var set = function (id, v) { var el = $(id); if (el) el.value = v; };
    set("lead-job", job.label);
    set("lead-details", res.parts.join("; "));
    set("lead-estimate-shown", money(res.lo) + " – " + money(res.hi) + " " + (C.currency || "CAD"));
  };

  form.addEventListener("submit", function (e) { e.preventDefault(); });
  form.addEventListener("change", calc);
  form.addEventListener("input", function (e) {
    var t = e.target;
    if (t.hasAttribute("data-range")) { var n = t.closest(".len").querySelector("[data-num]"); n.value = t.value; }
    if (t.hasAttribute("data-num") && t.value !== "") { var rr = t.closest(".len").querySelector("[data-range]"); rr.value = t.value; }
    calc();
  });
  Array.prototype.forEach.call(form.querySelectorAll(".len__range"), function (r) {
    var fill = function () { r.style.setProperty("--fill", ((r.value - r.min) / (r.max - r.min) * 100).toFixed(1)); };
    r.addEventListener("input", fill); fill();
  });
  form.addEventListener("input", function (e) { if (e.target.hasAttribute("data-num")) { var rr = e.target.closest(".len").querySelector("[data-range]"); rr.style.setProperty("--fill", ((rr.value - rr.min) / (rr.max - rr.min) * 100).toFixed(1)); } });
  Array.prototype.forEach.call(form.querySelectorAll(".stepper__b"), function (b) {
    b.addEventListener("click", function () {
      var inp = b.parentNode.querySelector("input");
      var max = parseInt(inp.max, 10) || 20;
      inp.value = Math.max(0, Math.min(max, (parseInt(inp.value, 10) || 0) + (+b.getAttribute("data-step")))); calc();
    });
  });
  calc();

  /* phones: show the live price bar while the result card is off screen */
  var live = $("est-live");
  if (live && result && "IntersectionObserver" in window) {
    var tool = document.getElementById("estimator"), inTool = false, resVis = false;
    var upLive = function () { live.classList.toggle("is-visible", inTool && !resVis); };
    new IntersectionObserver(function (en) { resVis = en[0].isIntersecting; upLive(); }).observe(result);
    new IntersectionObserver(function (en) { inTool = en[0].isIntersecting; upLive(); }).observe(tool);
  }

  /* reveal the lead form */
  var open = $("est-lead-open"), lead = $("est-lead");
  if (open && lead) open.addEventListener("click", function () {
    lead.hidden = false;
    open.setAttribute("aria-expanded", "true");
    lead.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    setTimeout(function () { var n = $("lead-name"); if (n) n.focus({ preventScroll: true }); }, 350);
  });
})();
