/* XELON AERO — motion layer (Motion / Framer Motion vanilla API)
   Rules (framer-motion + ui-ux-pro-max skills):
   - animate only transform + opacity; springs for physical interactions,
     decelerating ease for entrances; exits ~65% of enter duration;
   - stagger 30–50ms per item; 1–2 key animated elements per view;
   - content is visible without JS/Motion; nothing is parked hidden above the fold;
   - prefers-reduced-motion → no motion at all. */
(function () {
  "use strict";
  var M = window.Motion;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var header = document.querySelector(".site-header");

  // Header shadow on scroll works regardless of Motion (plain class toggle).
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }
  if (!M || !M.animate || reduce) return;

  var animate = M.animate, inView = M.inView, stagger = M.stagger;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var EASE_OUT = [0.22, 1, 0.36, 1];
  var SPRING = { type: "spring", stiffness: 380, damping: 30 };     // interactions
  var SPRING_SOFT = { type: "spring", stiffness: 220, damping: 28 }; // layout moves
  var hoverCapable = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var XA = window.XA = window.XA || {};

  /* ---------- 1. Hero entrance (only if we're early enough to avoid a flash) ---------- */
  var early = performance.now() < 900;
  var heroSeq = $$(".hero .eyebrow, .hero h1, .hero-lead, .hero-actions, .hero-trust, .page-hero .breadcrumbs, .page-hero .eyebrow, .page-hero h1, .page-hero .lead, .page-hero .chips");
  if (early && heroSeq.length) {
    animate(heroSeq, { opacity: [0, 1], y: [18, 0] }, { duration: 0.55, delay: stagger(0.06), ease: EASE_OUT });
    var photo = document.querySelector(".hero-photo");
    if (photo) animate(photo, { opacity: [0, 1], scale: [0.96, 1] }, { duration: 0.7, delay: 0.15, ease: EASE_OUT });
    var callouts = $$(".callout");
    if (callouts.length) animate(callouts, { opacity: [0, 1], scale: [0.9, 1] }, { duration: 0.45, delay: stagger(0.08, { startDelay: 0.45 }), ease: EASE_OUT });
  }

  /* ---------- 2. Scroll reveals with stagger (below the fold only) ---------- */
  var GROUPS = [
    [".dir-grid", ".dir-card"], [".product-grid:not([data-catalog])", ".product-card"], [".kit-grid", ".kit"],
    [".tier-grid", ".tier"], [".feat-grid", ".feat"], [".steps", "li"], [".terms", ".term"],
    [".pillars", ".pillar"], [".compat", ".compat-row"], [".org", ".org-node"], [".metrics-grid", ".metric"]
  ];
  var vh = window.innerHeight;
  GROUPS.forEach(function (g) {
    $$(g[0]).forEach(function (container) {
      var items = $$(":scope > " + g[1], container);
      if (!items.length || container.getBoundingClientRect().top < vh * 0.9) return; // already on screen: leave at rest
      animate(items, { opacity: 0, y: 22 }, { duration: 0 });
      inView(container, function () {
        animate(items, { opacity: 1, y: 0 }, { duration: 0.5, delay: stagger(0.045), ease: EASE_OUT });
      }, { amount: 0.12 });
    });
  });
  $$(".section-head, .table-wrap, .figure").forEach(function (el) {
    if (el.getBoundingClientRect().top < vh * 0.9) return;
    animate(el, { opacity: 0, y: 16 }, { duration: 0 });
    inView(el, function () { animate(el, { opacity: 1, y: 0 }, { duration: 0.5, ease: EASE_OUT }); }, { amount: 0.2 });
  });

  /* ---------- 3. Count-up metrics (meaning: quantities) ---------- */
  $$("[data-count]").forEach(function (el) {
    var target = Number(el.getAttribute("data-count"));
    if (!target || target < 3) return;
    inView(el, function () {
      animate(0, target, { duration: Math.min(1.4, 0.5 + target / 300), ease: EASE_OUT, onUpdate: function (v) { el.textContent = Math.round(v); } });
    }, { amount: 1 });
  });

  /* ---------- 4. Press feedback: spring scale 0.97 ---------- */
  document.addEventListener("pointerdown", function (e) {
    var t = e.target.closest(".btn, .nav-toggle, .seg label, .model-opts label, .currency-toggle button");
    if (!t) return;
    animate(t, { scale: 0.97 }, SPRING);
    var release = function () { animate(t, { scale: 1 }, SPRING); t.removeEventListener("pointerup", release); t.removeEventListener("pointerleave", release); };
    t.addEventListener("pointerup", release); t.addEventListener("pointerleave", release);
  });

  /* ---------- 5. Card hover lift (pointer devices only) ---------- */
  if (hoverCapable) {
    $$(".dir-card, .product-card").forEach(function (card) {
      card.addEventListener("pointerenter", function () { animate(card, { y: -4 }, SPRING); });
      card.addEventListener("pointerleave", function () { animate(card, { y: 0 }, SPRING); });
    });
  }

  /* ---------- 6. Sliding nav indicator (shared-element style) ---------- */
  var list = document.querySelector(".nav-list");
  if (list && window.matchMedia("(min-width: 1024px)").matches) {
    var ind = document.createElement("span"); ind.className = "nav-ind"; ind.setAttribute("aria-hidden", "true");
    list.appendChild(ind); list.classList.add("has-ind");
    var links = $$(":scope > .nav-item > .nav-link", list);
    var active = links.filter(function (l) { return l.classList.contains("is-active") || l.getAttribute("aria-current") === "page"; })[0];
    var moveTo = function (link, instant) {
      if (!link) { animate(ind, { opacity: 0 }, { duration: 0.15 }); return; }
      var lr = list.getBoundingClientRect(), r = link.getBoundingClientRect();
      var pad = 12, w = Math.max(8, r.width - pad * 2);
      animate(ind, { x: r.left - lr.left + pad, scaleX: w / 100, opacity: 1 }, instant ? { duration: 0 } : SPRING);
    };
    var place = function () { moveTo(active, true); };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(place); else place();
    window.addEventListener("resize", place);
    links.forEach(function (l) {
      l.addEventListener("pointerenter", function () { moveTo(l); });
      l.addEventListener("focus", function () { moveTo(l); });
    });
    list.addEventListener("pointerleave", function () { moveTo(active); });
    list.addEventListener("focusout", function (e) { if (!list.contains(e.relatedTarget)) moveTo(active); });
  }

  /* ---------- 7. Mobile menu: enter 280ms / exit 180ms ---------- */
  XA.navToggle = function (nav, open) {
    var items = $$(".nav-list > .nav-item, .nav-cta", nav);
    if (open) {
      nav.classList.add("open");
      animate(nav, { opacity: [0, 1] }, { duration: 0.2, ease: EASE_OUT });
      animate(items, { opacity: [0, 1], y: [-10, 0] }, { duration: 0.28, delay: stagger(0.035), ease: EASE_OUT });
    } else {
      animate(nav, { opacity: 0 }, { duration: 0.18, ease: [0.55, 0, 1, 0.45] }).then(function () {
        nav.classList.remove("open"); nav.style.opacity = "";
      });
    }
  };

  /* ---------- 8. Spec table expand ---------- */
  $$("details.specs").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      animate($$("tr", d), { opacity: [0, 1], y: [-6, 0] }, { duration: 0.3, delay: stagger(0.02), ease: EASE_OUT });
    });
  });

  /* ---------- 9. Catalog: FLIP layout animation (like `layout` prop) ---------- */
  XA.flip = function (cards, mutate) {
    var before = new Map();
    cards.forEach(function (c) { if (!c.hidden) before.set(c, c.getBoundingClientRect()); });
    mutate();
    cards.forEach(function (c) {
      if (c.hidden) return;
      var prev = before.get(c), now = c.getBoundingClientRect();
      if (prev) {
        var dx = prev.left - now.left, dy = prev.top - now.top;
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) animate(c, { x: [dx, 0], y: [dy, 0] }, SPRING_SOFT);
      } else if (now.top < window.innerHeight + 200) {
        animate(c, { opacity: [0, 1], scale: [0.96, 1] }, { duration: 0.32, ease: EASE_OUT });
      }
    });
  };

  /* ---------- 10. Form status pop ---------- */
  XA.pop = function (el) { animate(el, { opacity: [0, 1], y: [-6, 0] }, { duration: 0.25, ease: EASE_OUT }); };
})();
