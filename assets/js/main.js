/* XELON AERO — site scripts (no dependencies) */
(function () {
  "use strict";
  var CFG = window.XELON_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }
  };
  var fmt = function (n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "); };

  /* ---------- Mobile nav ---------- */
  var toggle = $(".nav-toggle"), nav = $("#main-nav");
  if (toggle && nav) {
    var menuIcon = toggle.innerHTML;
    var closeIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
    var setNav = function (open) {
      if (window.XA && window.XA.navToggle && window.matchMedia("(max-width: 1023px)").matches) window.XA.navToggle(nav, open);
      else nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
      toggle.innerHTML = open ? closeIcon : menuIcon;
      document.body.style.overflow = open ? "hidden" : "";
    };
    toggle.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { setNav(false); toggle.focus(); } });
    window.matchMedia("(min-width: 1024px)").addEventListener("change", function (m) { if (m.matches) setNav(false); });
  }


  /* ---------- Currency display (₽ / RMB) ---------- */
  var rate = Number(CFG.rubPerCny);
  var toggles = $$("[data-currency-toggle]");
  function renderCurrency(cur) {
    $$("[data-rub]").forEach(function (el) {
      var rub = Number(el.getAttribute("data-rub"));
      el.textContent = cur === "CNY" ? "≈ " + fmt(rub / rate) + " ¥" : fmt(rub) + " ₽";
      el.title = cur === "CNY" ? "Ориентировочно по курсу " + rate + " ₽/¥. Базовая цена: " + fmt(rub) + " ₽ без НДС" : "";
    });
    toggles.forEach(function (t) {
      $$("button", t).forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-cur") === cur)); });
    });
    store.set("xa-currency", cur);
  }
  if (rate > 0 && toggles.length) {
    toggles.forEach(function (t) {
      t.classList.add("is-enabled");
      t.addEventListener("click", function (e) { var b = e.target.closest("button[data-cur]"); if (b) renderCurrency(b.getAttribute("data-cur")); });
    });
    if (store.get("xa-currency") === "CNY") renderCurrency("CNY");
  }

  /* ---------- Catalog filters ---------- */
  var grid = $("[data-catalog]"), filters = $("#filters");
  if (grid && filters) {
    var cards = $$(".product-card", grid);
    var countEl = $("[data-count]"), emptyEl = $("[data-empty]"), sortEl = $("#f-sort");
    var subSel = $("#f-sub", filters);
    var fToggle = $(".filters-toggle");
    if (fToggle) fToggle.addEventListener("click", function () {
      var collapsed = filters.classList.toggle("collapsed");
      fToggle.setAttribute("aria-expanded", String(!collapsed));
    });

    var state = function () {
      var fd = new FormData(filters);
      return { cat: fd.get("cat") || "all", sub: fd.get("sub") || "", price: fd.get("price") || "", priced: !!fd.get("priced"), payload: fd.get("payload") || "", sort: sortEl ? sortEl.value : "" };
    };
    var syncSubOptions = function (cat) {
      $$("option[data-cat]", subSel).forEach(function (o) { o.hidden = cat !== "all" && o.getAttribute("data-cat") !== cat; });
      var cur = subSel.selectedOptions[0];
      if (cur && cur.hidden) subSel.value = "";
    };
    var apply = function (pushUrl) {
      var s = state();
      syncSubOptions(s.cat);
      s = state();
      var range = s.price ? s.price.split("-") : null;
      var min = range ? Number(range[0] || 0) : 0, max = range && range[1] ? Number(range[1]) : Infinity;
      var shown = 0;
      var flip = pushUrl && window.XA && window.XA.flip ? window.XA.flip : function (list, fn) { fn(); };
      flip(cards, function () {
      cards.forEach(function (c) {
        var price = c.dataset.price ? Number(c.dataset.price) : null;
        var payload = c.dataset.payload ? Number(c.dataset.payload) : null;
        var ok = (s.cat === "all" || c.dataset.cat === s.cat) &&
          (!s.sub || c.dataset.sub === s.sub) &&
          (!s.priced || price !== null) &&
          (!range || (price !== null && price >= min && price <= max)) &&
          (!s.payload || (payload !== null && payload >= Number(s.payload)));
        c.hidden = !ok;
        if (ok) shown++;
      });
      var sorted = cards.slice().sort(function (a, b) {
        var pa = a.dataset.price ? +a.dataset.price : null, pb = b.dataset.price ? +b.dataset.price : null;
        if (s.sort === "price-asc" || s.sort === "price-desc") {
          if (pa === null && pb === null) return a.dataset.order - b.dataset.order;
          if (pa === null) return 1; if (pb === null) return -1;
          return s.sort === "price-asc" ? pa - pb : pb - pa;
        }
        if (s.sort === "payload-desc") {
          var la = a.dataset.payload ? +a.dataset.payload : -1, lb = b.dataset.payload ? +b.dataset.payload : -1;
          return lb - la || a.dataset.order - b.dataset.order;
        }
        return a.dataset.order - b.dataset.order;
      });
      sorted.forEach(function (c) { grid.appendChild(c); });
      });
      countEl.textContent = shown;
      emptyEl.classList.toggle("show", shown === 0);
      if (pushUrl) {
        var q = new URLSearchParams();
        if (s.cat !== "all") q.set("cat", s.cat);
        if (s.sub) q.set("sub", s.sub);
        if (s.price) q.set("price", s.price);
        if (s.priced) q.set("priced", "1");
        if (s.payload) q.set("payload", s.payload);
        if (s.sort) q.set("sort", s.sort);
        var qs = q.toString();
        history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
      }
    };
    // restore from URL
    var p = new URLSearchParams(location.search);
    if (p.get("cat")) { var r = $('input[name="cat"][value="' + CSS.escape(p.get("cat")) + '"]', filters); if (r) r.checked = true; }
    ["sub", "price", "payload"].forEach(function (k) { if (p.get(k)) { var el = filters.elements[k]; if (el) el.value = p.get(k); } });
    if (p.get("priced")) filters.elements.priced.checked = true;
    if (p.get("sort") && sortEl) sortEl.value = p.get("sort");

    filters.addEventListener("change", function () { apply(true); });
    if (sortEl) sortEl.addEventListener("change", function () { apply(true); });
    filters.addEventListener("reset", function () { setTimeout(function () { if (sortEl) sortEl.value = ""; apply(true); }, 0); });
    apply(false);
  }

  /* ---------- Request form ---------- */
  $$("[data-request-form]").forEach(function (form) {
    var status = $("[data-form-status]", form);
    var btn = $('button[type="submit"]', form);
    var modelsField = $("[data-models-field]", form);
    form.elements.page.value = document.title;

    var updateCounts = function () {
      $$(".model-picker details", form).forEach(function (d) {
        var n = $$("input:checked", d).length;
        $("[data-sel-count]", d).textContent = n ? "выбрано: " + n : "";
      });
    };
    // prefill ?model=
    var pre = new URLSearchParams(location.search).get("model");
    if (pre) {
      var box = $('input[data-id="' + CSS.escape(pre) + '"]', form);
      if (box) { box.checked = true; var det = box.closest("details"); if (det) det.open = true; }
    }
    updateCounts();
    form.addEventListener("change", function (e) { if (e.target.name === "models") { updateCounts(); if (modelsField.classList.contains("invalid")) validate(); } });

    var setErr = function (field, bad) {
      if (!field) return;
      field.classList.toggle("invalid", bad);
      $$("input,select,textarea", field).forEach(function (i) { if (i.type !== "checkbox" || i.name === "consent") i.setAttribute("aria-invalid", String(bad)); });
    };
    var fieldOf = function (name) { var el = form.elements[name]; el = el && el.length && !el.tagName ? el[0] : el; return el ? el.closest(".field") : null; };
    var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    var phoneRe = /^[+()\-\s\d]{6,20}$/;

    function validate() {
      var el = form.elements, firstBad = null, check = function (name, bad) { setErr(fieldOf(name), bad); if (bad && !firstBad) firstBad = name; };
      check("company", el.company.value.trim().length < 2);
      check("name", el.name.value.trim().length < 2);
      check("email", !emailRe.test(el.email.value.trim()));
      check("phone", el.phone.value.trim() !== "" && !phoneRe.test(el.phone.value.trim()));
      check("quantity", el.quantity.value !== "" && !(Number(el.quantity.value) >= 1 && Number.isInteger(Number(el.quantity.value))));
      var hasModels = $$('input[name="models"]:checked', form).length > 0;
      var modelsBad = !hasModels && el.comment.value.trim().length < 10;
      setErr(modelsField, modelsBad); if (modelsBad && !firstBad) firstBad = "models";
      check("consent", !el.consent.checked);
      return firstBad;
    }
    ["company", "name", "email", "phone", "quantity"].forEach(function (n) {
      form.elements[n].addEventListener("blur", function () { if (form.dataset.touched) validate(); });
      form.elements[n].addEventListener("input", function () { var f = fieldOf(n); if (f && f.classList.contains("invalid")) validate(); });
    });

    var show = function (type, msg) {
      status.className = "full form-status show " + type; status.textContent = msg;
      if (window.XA && window.XA.pop) window.XA.pop(status);
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.dataset.touched = "1";
      var bad = validate();
      if (bad) {
        show("err", "Проверьте выделенные поля.");
        var target = bad === "models" ? $('input[name="models"]', form) : form.elements[bad];
        if (target) { if (bad === "models") { var d = $(".model-picker details", form); if (d) d.open = true; } target.focus({ preventScroll: false }); }
        return;
      }
      if (form.elements._gotcha.value) return; // bot

      var fd = new FormData(form);
      var payload = {};
      fd.forEach(function (v, k) { if (k === "models") { (payload.models = payload.models || []).push(v); } else if (k !== "_gotcha") payload[k] = v; });
      payload.models = (payload.models || []).join(", ");
      payload.consent = "да";

      var endpoint = CFG.crmWebhook || CFG.formEndpoint || "";
      if (!endpoint || /YOUR_FORM_ID/.test(endpoint)) {
        console.warn("[XELON AERO] Форма в демо-режиме. Укажите formEndpoint в assets/js/config.js", payload);
        show("warn", "Демо-режим: форма ещё не подключена к почте/CRM. Напишите нам на info@gk-xelon.ru — или администратору сайта нужно указать Formspree ID в assets/js/config.js.");
        return;
      }
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Отправка…";
      fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r; })
        .then(function () {
          form.reset(); updateCounts(); delete form.dataset.touched;
          show("ok", "Спасибо! Запрос отправлен — мы подготовим расчёт стоимости, сроков и условий поставки и свяжемся с вами.");
        })
        .catch(function () { show("err", "Не удалось отправить запрос. Попробуйте ещё раз или напишите на info@gk-xelon.ru."); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
