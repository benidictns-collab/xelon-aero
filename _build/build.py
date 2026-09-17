# -*- coding: utf-8 -*-
"""Генератор статического сайта XELON AERO. Запуск: python3 _build/build.py"""
import json, os, math, datetime
from html import escape as esc
import data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = D.SITE
TODAY = datetime.date.today().isoformat()

# ------------------------------------------------------------------ icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    "grid": '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/>',
    "ship": '<path d="M3 17c2 2 4 2 6 0s4-2 6 0 4 2 6 0"/><path d="M5 14 4 9h16l-1 5"/><path d="M8 9V5h8v4"/>',
    "signal": '<path d="M4 20c0-8.8 7.2-16 16-16"/><path d="M8 20a12 12 0 0 1 12-12"/><path d="M12 20a8 8 0 0 1 8-8"/><circle cx="18" cy="18" r="2"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
    "weight": '<path d="M6 8h12l2 12H4L6 8Z"/><circle cx="12" cy="5" r="2"/>',
    "drone": '<circle cx="5.5" cy="5.5" r="2.5"/><circle cx="18.5" cy="5.5" r="2.5"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/><path d="m7.5 7.5 3 3m6-3-3 3m-6 6 3-3m6 3-3-3"/><rect x="10" y="10" width="4" height="4" rx="1"/>',
    "battery": '<rect x="3" y="7" width="16" height="10" rx="2"/><path d="M21 10v4M7 10v4M11 10v4"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0V8Z"/><path d="M12 17v4"/>',
    "remote": '<rect x="5" y="8" width="14" height="12" rx="3"/><path d="M12 8V3"/><circle cx="9" cy="14" r="1.5"/><circle cx="15" cy="14" r="1.5"/>',
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M9 8h4a2.5 2.5 0 0 1 0 5H9m0-5v9m-1-3h5"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "send": '<path d="M21 3 10 14"/><path d="m21 3-7 18-4-7-7-4 18-7Z"/>',
    "chat": '<path d="M4 20l1.5-4A8 8 0 1 1 9 19.5L4 20Z"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "swipe": '<path d="M4 12h16M8 8l-4 4 4 4M16 8l4 4-4 4"/>',
    "box": '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    "handshake": '<path d="m11 17 2 2a1.5 1.5 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.5 1.5 0 0 0 2-2L15 11l-3 1-2-2 3-3h3l4 4"/><path d="M3 11l4-4h3M3 11l6 6"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L4 16.7 7.3 20l5.3-5.3a4 4 0 0 0 5.1-5.4l-2.6 2.6-2.4-.6-.6-2.4 2.6-2.6Z"/>',
    "filter": '<path d="M4 5h16l-6 8v5l-4 2v-7L4 5Z"/>',
    "fiber": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
    "check": '<path d="m5 12 5 5 9-10"/>',
}
def icon(name, cls=""):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'

LOGO_MARK = '''<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#1E4FD9"/><path d="M11 11l18 18M29 11L11 29" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><circle cx="11" cy="11" r="3.4" fill="none" stroke="#A9BFFF" stroke-width="1.6"/><circle cx="29" cy="11" r="3.4" fill="none" stroke="#A9BFFF" stroke-width="1.6"/><circle cx="11" cy="29" r="3.4" fill="none" stroke="#A9BFFF" stroke-width="1.6"/><circle cx="29" cy="29" r="3.4" fill="none" stroke="#A9BFFF" stroke-width="1.6"/></svg>'''

def count_wrap(v):
    import re as _re
    m = _re.search(r"\d+", v)
    if not m:
        return v
    return v[:m.start()] + f'<span data-count="{m.group()}">{m.group()}</span>' + v[m.end():]

def rub(v):
    return f"{v:,}".replace(",", " ") + " ₽"

# ------------------------------------------------------------------ placeholders
def placeholder_svg(n_arms, label):
    """Схематичный рендер (вид сверху) для моделей без фото."""
    cx, cy, R = 200, 150, 104
    parts = []
    for k in range(n_arms):
        a = math.radians((45 if n_arms == 4 else 30) + 360 / n_arms * k)
        x, y = cx + R * math.cos(a), cy + R * 0.78 * math.sin(a)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="34" fill="none" stroke="currentColor" stroke-opacity=".35" stroke-dasharray="4 5"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="currentColor"/>')
    return f'''<svg class="placeholder" viewBox="0 0 400 300" role="img" aria-label="Схематичное изображение {esc(label)}">
<defs><pattern id="g-{esc(label)}" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="currentColor" stroke-opacity=".08"/></pattern></defs>
<rect width="400" height="300" fill="url(#g-{esc(label)})"/>
{''.join(parts)}
<rect x="{cx-34}" y="{cy-26}" width="68" height="52" rx="10" fill="#fff" stroke="currentColor" stroke-width="3"/>
<rect x="{cx-18}" y="{cy-12}" width="36" height="24" rx="4" fill="currentColor" fill-opacity=".12"/>
<text x="16" y="284" font-family="JetBrains Mono, monospace" font-size="12" fill="#667085">{esc(label)} · {n_arms} ротор{"а" if n_arms==4 else "ов"} · схема</text>
</svg>'''

# ------------------------------------------------------------------ layout
NAV = [
    ("index.html", "Главная", None),
    ("catalog.html", "Каталог", [
        ("agro.html", "Сельхоздроны", "Опрыскиватели 20/30/50 л, погрузчики 15–200 кг"),
        ("fpv.html", "FPV-комплексы ZTK", "Рамы 7″–15″, аккумуляторы, комплектующие"),
        ("fiber.html", "Оптоволоконные системы", "Катушки 10–30 км, модули ZR LINK"),
        ("catalog.html", "Весь каталог с фильтрами", "30 позиций"),
    ]),
    ("terms.html", "Условия", None),
    ("about.html", "О компании", None),
    ("contacts.html", "Контакты", None),
]
AC = ' aria-current="page"'
CATALOG_PAGES = {"catalog.html", "agro.html", "fpv.html", "fiber.html"}

def header(path):
    items = []
    for href, label, sub in NAV:
        active = (href == path) or (sub and path in CATALOG_PAGES)
        cur = ' aria-current="page"' if href == path else ""
        cls = " is-active" if active else ""
        if sub:
            subs = "".join(
                f'<li><a href="{h}"{AC if h == path else ""}>{esc(l)}<small>{esc(s)}</small></a></li>' for h, l, s in sub)
            items.append(f'<li class="nav-item"><a class="nav-link{cls}" href="{href}"{cur}>{label}{icon("chev","caret")}</a><ul class="nav-sub">{subs}</ul></li>')
        else:
            items.append(f'<li class="nav-item"><a class="nav-link{cls}" href="{href}"{cur}>{label}</a></li>')
    return f'''<a class="skip-link" href="#main">Перейти к содержимому</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html" aria-label="XELON AERO — на главную">{LOGO_MARK}<span class="logo-text">XELON <b>AERO</b></span></a>
    <nav class="main-nav" id="main-nav" aria-label="Основная навигация">
      <ul class="nav-list">{''.join(items)}</ul>
      <div class="nav-cta"><a class="btn btn-primary btn-block" href="contacts.html#form">Получить расчёт</a></div>
    </nav>
    <a class="btn btn-primary btn-sm header-cta" href="contacts.html#form">Получить расчёт</a>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Открыть меню">{icon("menu")}</button>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="logo" href="index.html">{LOGO_MARK}<span class="logo-text">XELON <b>AERO</b></span></a>
        <p>Поставка сельскохозяйственных дронов, погрузочных комплексов, FPV-систем и оптоволоконных комплектов связи для B2B-заказчиков.</p>
      </div>
      <div><h4>Каталог</h4><ul>
        <li><a href="agro.html">Сельхоздроны</a></li><li><a href="fpv.html">FPV-комплексы ZTK</a></li>
        <li><a href="fiber.html">Оптоволоконные системы</a></li><li><a href="catalog.html">Весь каталог</a></li></ul></div>
      <div><h4>Компания</h4><ul>
        <li><a href="terms.html">Условия сотрудничества</a></li><li><a href="about.html">О компании</a></li>
        <li><a href="contacts.html">Контакты</a></li></ul></div>
      <div><h4>Связаться</h4><ul>
        <li><a href="mailto:{S['email']}">{S['email']}</a></li>
        <li><a href="https://{S['site_label']}" rel="noopener">{S['site_label']}</a></li>
        <li><a href="contacts.html#form">Запросить коммерческое предложение</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>{esc(S['disclaimer'])}</span>
      <span>© <span data-year>{datetime.date.today().year}</span> XELON AERO</span>
    </div>
  </div>
</footer>'''

def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

ORG = {"@type": "Organization", "name": "XELON AERO", "url": S["url"], "email": S["email"],
       "logo": S["url"] + "/assets/img/logo.svg",
       "parentOrganization": {"@type": "Organization", "name": S["parent"]}}

def page(path, title, desc, body, ld=None, og_img="assets/img/products/sprayer-50l.jpg", extra_js=""):
    url = S["url"] + "/" + ("" if path == "index.html" else path)
    ld_html = "".join(jsonld(x) for x in (ld or []))
    return f'''<!doctype html>
<html lang="ru" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#05080F">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="XELON AERO">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{S['url']}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.remove("no-js")</script>
{ld_html}
</head>
<body data-page="{path}">
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/config.js"></script>
<script src="assets/js/main.js" defer></script>
<!-- Motion (Framer Motion vanilla build). Для продакшена можно положить файл локально в assets/js/vendor/ -->
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.2/dist/motion.js" defer></script>
<script src="assets/js/motion.js" defer></script>
{extra_js}
</body>
</html>'''

def breadcrumbs(trail):
    lis = []
    for i, (href, label) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        else:
            lis.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": l, "item": S["url"] + "/" + ("" if h == "index.html" else h)}
        for i, (h, l) in enumerate(trail)]}
    return f'<nav aria-label="Хлебные крошки"><ol class="breadcrumbs">{"".join(lis)}</ol></nav>', ld

def page_hero(trail, eyebrow, h1, lead, chips=()):
    bc, ld = breadcrumbs(trail)
    ch = "".join(f'<span class="chip">{c}</span>' for c in chips)
    return f'''<section class="dark grid-bg page-hero"><div class="container">
{bc}
<p class="eyebrow mt-24">{eyebrow}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{f'<div class="chips">{ch}</div>' if ch else ''}
</div></section>''', ld

def section_head(num, h2, p=None, right=""):
    inner = f'<span class="num">{num}</span><h2>{h2}</h2>' + (f'<p>{p}</p>' if p else "")
    if right:
        return f'<div class="section-head split"><div>{inner}</div>{right}</div>'
    return f'<div class="section-head">{inner}</div>'

def notice(text, dark=False):
    return f'<p class="notice{" dark-notice" if dark else ""}">{icon("info")}<span>{text}</span></p>'

def currency_toggle():
    return '<div class="currency-toggle" data-currency-toggle role="group" aria-label="Валюта отображения"><button type="button" data-cur="RUB" aria-pressed="true">₽</button><button type="button" data-cur="CNY" aria-pressed="false">¥ RMB</button></div>'

# ------------------------------------------------------------------ product card
def product_media(p, eager=False):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    if p.get("img"):
        from PIL import Image
        w, h = Image.open(os.path.join(ROOT, "assets/img/products", p["img"])).size
        cls = ' class="dark-photo"' if p.get("dark") else ""
        return f'<img src="assets/img/products/{p["img"]}" alt="{esc(p["name"])}" width="{w}" height="{h}" {load} decoding="async"{cls}>'
    ph = p.get("placeholder")
    return placeholder_svg(ph[1], ph[2])

def product_card(p, heading="h3", show_tag=False):
    keys = "".join(f'<div class="pc-key"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["keys"])
    rows = "".join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in p["specs"])
    if p["price"]:
        price = f'''<div class="pc-price"><span class="label">{esc(p["price_label"])}</span>
<span class="value" data-rub="{p["price"]}">{rub(p["price"])}</span><span class="vat">без НДС</span></div>'''
    else:
        price = '<div class="pc-price"><span class="label">Цена</span><span class="value on-request">По запросу</span></div>'
    tag = f'<span class="pc-tag">{esc(D.SUBTYPES[p["sub"]])}</span>' if show_tag else ""
    attrs = f'data-cat="{p["cat"]}" data-sub="{p["sub"]}" data-price="{p["price"] or ""}" data-payload="{p["payload"] or ""}" data-order="{D.P.index(p)}"'
    return f'''<article class="product-card" id="{p["id"]}" {attrs}>
<div class="pc-media">{tag}{product_media(p)}</div>
<div class="pc-body">
<div class="pc-title"><{heading}>{esc(p["name"])}</{heading}><p class="pc-sub">{esc(p["subtitle"])}</p></div>
<dl class="pc-keys" style="margin:0">{keys}</dl>
<details class="specs"><summary>Все характеристики {icon("chev")}</summary><table><tbody>{rows}</tbody></table></details>
{price}
<div class="pc-actions"><a class="btn btn-primary btn-sm" href="contacts.html?model={p["id"]}#form">Запросить КП</a></div>
</div>
</article>'''

def product_ld(p):
    page_url = S["url"] + "/" + D.CATEGORIES[p["cat"]]["page"] + "#" + p["id"]
    o = {"@type": "Product", "@id": page_url, "name": p["name"], "description": p["desc"], "sku": p["id"],
         "category": D.CATEGORIES[p["cat"]]["long"] + " / " + D.SUBTYPES[p["sub"]], "url": page_url,
         "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["specs"]]}
    if p.get("img"):
        o["image"] = S["url"] + "/assets/img/products/" + p["img"]
    if p["price"]:
        o["offers"] = {"@type": "Offer", "price": p["price"], "priceCurrency": "RUB", "url": page_url,
                       "availability": "https://schema.org/PreOrder",
                       "priceSpecification": {"@type": "UnitPriceSpecification", "price": p["price"], "priceCurrency": "RUB", "valueAddedTaxIncluded": False},
                       "seller": {"@type": "Organization", "name": "XELON AERO"},
                       "businessFunction": "http://purl.org/goodrelations/v1#Sell"}
    return o

def itemlist_ld(products, name):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name,
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": product_ld(p)} for i, p in enumerate(products)]}

def by(**kw):
    return [p for p in D.P if all(p.get(k) == v for k, v in kw.items())]

def table_hint():
    return f'<p class="table-hint">{icon("swipe")} Таблицу можно прокручивать по горизонтали</p>'

# ------------------------------------------------------------------ form
def request_form(form_title="Запрос коммерческого предложения"):
    groups = [("agro", "sprayer"), ("agro", "loader"), ("fpv", "frame"), ("fpv", "battery"), ("fpv", "accessory"), ("fiber", "spool"), ("fiber", "module")]
    det = []
    for cat, sub in groups:
        opts = "".join(f'<label><input type="checkbox" name="models" value="{esc(p["name"])}" data-id="{p["id"]}"><span>{esc(p["short"])}</span></label>' for p in by(cat=cat, sub=sub))
        det.append(f'<details><summary>{D.SUBTYPES[sub]} <span class="sel-count" data-sel-count></span></summary><div class="model-opts">{opts}</div></details>')
    return f'''<form class="form-card" id="request-form" novalidate data-request-form>
<h3 style="font-size:22px;margin-bottom:6px">{form_title}</h3>
<p class="muted small" style="margin-bottom:22px">Направьте перечень интересующих моделей и требуемый объём — подготовим точный расчёт стоимости, сроков и условий поставки.</p>
<div class="form-grid">
  <div class="field"><label for="f-company">Название компании <span class="req">*</span></label>
    <input class="input" id="f-company" name="company" autocomplete="organization" required maxlength="160" aria-describedby="e-company">
    <span class="field-error" id="e-company">Укажите название компании</span></div>
  <div class="field"><label for="f-name">Контактное лицо <span class="req">*</span></label>
    <input class="input" id="f-name" name="name" autocomplete="name" required maxlength="120" aria-describedby="e-name">
    <span class="field-error" id="e-name">Укажите имя</span></div>
  <div class="field"><label for="f-email">Email <span class="req">*</span></label>
    <input class="input" id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="160" aria-describedby="e-email">
    <span class="field-error" id="e-email">Введите корректный email</span></div>
  <div class="field"><label for="f-phone">Телефон / мессенджер</label>
    <input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40" placeholder="+7" aria-describedby="e-phone">
    <span class="field-error" id="e-phone">Проверьте номер телефона</span></div>
  <div class="field full" data-models-field><span class="label" id="l-models">Интересующие модели <span class="req">*</span></span>
    <div class="model-picker" role="group" aria-labelledby="l-models" aria-describedby="e-models">{''.join(det)}</div>
    <span class="field-error" id="e-models">Выберите хотя бы одну модель или опишите задачу в комментарии</span></div>
  <div class="field"><label for="f-volume">Объём заказа</label>
    <select class="select" id="f-volume" name="volume">
      <option value="">Выберите</option><option>до 100 шт.</option><option>100–1 000 шт.</option>
      <option>1 000–10 000 шт.</option><option>свыше 10 000 шт.</option><option>Пока не определён</option></select></div>
  <div class="field"><label for="f-qty">Количество, шт.</label>
    <input class="input" id="f-qty" name="quantity" type="number" min="1" step="1" inputmode="numeric" aria-describedby="e-qty">
    <span class="field-error" id="e-qty">Введите целое число больше нуля</span></div>
  <div class="field full"><label for="f-comment">Комментарий</label>
    <textarea class="textarea" id="f-comment" name="comment" maxlength="3000" placeholder="Задачи, требуемая комплектация, регион поставки, сроки"></textarea></div>
  <div class="field full"><label class="consent"><input type="checkbox" name="consent" id="f-consent" required aria-describedby="e-consent">
    <span>Согласен на обработку персональных данных для подготовки коммерческого предложения</span></label>
    <span class="field-error" id="e-consent">Необходимо согласие на обработку данных</span></div>
  <div class="hp" aria-hidden="true"><label>Не заполняйте это поле<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="_subject" value="Заявка на КП — XELON AERO">
  <input type="hidden" name="page" value="">
  <div class="full form-status" role="status" aria-live="polite" data-form-status></div>
  <div class="full form-footer">
    <span class="hint"><span class="req">*</span> обязательные поля</span>
    <button class="btn btn-primary" type="submit">Отправить запрос {icon("arrow")}</button>
  </div>
</div>
</form>'''

def cta_band(title="Готовы обсудить комплектацию поставки", text="Направьте перечень интересующих моделей и требуемый объём — подготовим точный расчёт стоимости, сроков и условий поставки под задачи вашего проекта."):
    return f'''<section class="dark grid-bg cta-band"><div class="container cta-inner">
<div><h2>{title}</h2><p>{text}</p></div>
<div class="hero-actions" style="margin:0"><a class="btn btn-primary" href="contacts.html#form">Получить расчёт {icon("arrow")}</a><a class="btn btn-ghost" href="mailto:{S['email']}">{icon("mail")} {S['email']}</a></div>
</div></section>'''

# ------------------------------------------------------------------ hero blueprint
BLUEPRINT = '''<svg class="blueprint" viewBox="0 0 580 500" fill="none" aria-hidden="true">
<g stroke="currentColor" stroke-opacity=".5">
<circle class="spin-slow" cx="80" cy="80" r="62" stroke-dasharray="3 7"/>
<circle class="spin-slow" cx="500" cy="80" r="62" stroke-dasharray="3 7"/>
<circle class="spin-slow" cx="80" cy="420" r="62" stroke-dasharray="3 7"/>
<circle class="spin-slow" cx="500" cy="420" r="62" stroke-dasharray="3 7"/>
</g>
<g stroke="currentColor" stroke-opacity=".75" stroke-width="1.2">
<path d="M80 80 L170 150 M500 80 L410 150 M80 420 L170 350 M500 420 L410 350"/>
<circle cx="80" cy="80" r="6"/><circle cx="500" cy="80" r="6"/><circle cx="80" cy="420" r="6"/><circle cx="500" cy="420" r="6"/>
</g>
<g stroke="currentColor" stroke-opacity=".45">
<path d="M18 490 H562 M18 482 v16 M562 482 v16"/>
<path d="M572 18 V482 M564 18 h16 M564 482 h16"/>
</g>
<g fill="#7FA2FF" font-family="JetBrains Mono, monospace" font-size="12" letter-spacing="1">
<text x="236" y="478">1870 мм</text>
<text x="556" y="262" transform="rotate(-90 556 262)">1710 мм</text>
<text x="18" y="16">XA / AGRO-50 · TOP VIEW</text>
</g>
</svg>'''

# ================================================================== PAGES
def build_index():
    metrics = [("layers", "3", "категории техники"), ("drone", "9", "моделей в линейке"), ("ship", "FOB", "Шэньчжэнь"),
               ("signal", "30 км", "макс. дальность оптоволокна"), ("shield", "IP65", "класс защиты сельхоздронов"),
               ("weight", "до 200 кг", "грузоподъёмность погрузчиков")]
    m_html = "".join(f'<div class="metric"><span class="metric-icon">{icon(i)}</span><div><div class="metric-value">{count_wrap(v)}</div><div class="metric-label">{l}</div></div></div>' for i, v, l in metrics)
    dirs = [
        ("01", "agro.html", "sprayer-30l.jpg", "Сельскохозяйственные дроны", "Опрыскиватели 20/30/50 л и погрузочно-разбрасывающие платформы от 15 до 200 кг грузоподъёмности.", ["3 модели опрыскивателей", "5 моделей погрузчиков", "Класс защиты IP65"]),
        ("02", "fpv.html", "fpv-an13b.jpg", "FPV-комплексы ZTK", "Линейка рам 7″–15″ для мониторинга, инспекции и специальных задач, скорость до 160 км/ч.", ["4 модели рам", "6 типов аккумуляторов", "Полный набор комплектующих"]),
        ("03", "fiber.html", "zr-link-ground.jpg", "Оптоволоконные системы", "Катушки оптоволокна 10–30 км и модули воздушного/наземного конца для помехозащищённой связи.", ["4 длины катушек", "Воздушный модуль ZR LINK", "Наземный модуль ZR LINK"]),
    ]
    d_html = "".join(f'''<a class="dir-card" href="{href}">
<div class="dir-media"><span class="dir-num">{n}</span><img src="assets/img/products/{img}" alt="" loading="lazy" decoding="async" width="400" height="300"></div>
<div class="dir-body"><h3>{t}</h3><p>{d}</p><ul class="dir-list">{''.join(f"<li>{x}</li>" for x in li)}</ul>
<span class="dir-more">Перейти в раздел {icon("arrow")}</span></div></a>''' for n, href, img, t, d, li in dirs)
    featured = [p for p in D.P if p["id"] in ("sprayer-50l", "loader-s200pro", "fpv-an15b", "spool-zr030")]
    f_html = "".join(product_card(p, show_tag=True) for p in featured)
    terms = "".join(f'<div class="term"><div class="term-k"><span class="kit-icon">{icon(i)}</span>{k}</div><p class="term-v">{v}</p></div>' for i, k, v in D.TERMS)

    body = f'''
<section class="dark grid-bg hero">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow">Экспорт и партнёрство · B2B</p>
      <h1>Поставка <em>сельско&shy;хозяйственных дронов</em>, погрузочных комплексов и FPV&#8209;систем</h1>
      <p class="hero-lead">Три линейки беспилотной техники с полными техническими характеристиками, комплектацией и ценой FOB Шэньчжэнь — для агрохолдингов, дистрибьюторов и интеграторов.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contacts.html#form">Получить расчёт {icon("arrow")}</a>
        <a class="btn btn-ghost" href="catalog.html">{icon("grid")} Каталог техники</a>
      </div>
      <ul class="hero-trust">
        <li>{icon("check")} Полные ТТХ по каждой позиции</li>
        <li>{icon("check")} Цены FOB без НДС</li>
        <li>{icon("check")} Комплектация под задачу</li>
      </ul>
    </div>
    <div class="hero-visual">
      {BLUEPRINT}
      <div class="hero-photo"><img src="assets/img/products/sprayer-50l.jpg" alt="Дрон-опрыскиватель 50 л" width="449" height="349" fetchpriority="high" decoding="async"></div>
      <dl class="callouts" aria-label="Характеристики дрона-опрыскивателя 50 л">
        <div class="callout c1"><dt>Рассев</dt><dd>50 кг / 80 л</dd></div>
        <div class="callout c2"><dt>Защита</dt><dd>IP65</dd></div>
        <div class="callout c3"><dt>Аккумулятор</dt><dd>18S 30000 мА·ч</dd></div>
        <div class="callout c4"><dt>Ширина распыления</dt><dd>6–9 м</dd></div>
      </dl>
    </div>
  </div>
</section>
<section class="dark metrics" aria-label="Ключевые показатели"><div class="container"><div class="metrics-grid">{m_html}</div></div></section>

<section class="section">
  <div class="container">
    {section_head("01 · Структура предложения", "Три направления беспилотной техники", "Полный спектр беспилотной техники для сельского хозяйства и специальных задач. Каждая позиция — с полными ТТХ, комплектацией и ценой.")}
    <div class="dir-grid">{d_html}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    {section_head("02 · Флагманы линеек", "Старшие модели каждого направления", None, '<a class="btn btn-outline" href="catalog.html">Весь каталог ' + icon("arrow") + '</a>')}
    <div class="product-grid cols-4">{f_html}</div>
    <div class="mt-24">{notice(S["disclaimer"])}</div>
  </div>
</section>

<section class="section">
  <div class="container split-2 wide-right">
    <div class="stack">
      {section_head("03 · Коммерческие условия", "Условия поставки", "Точные сроки поставки, условия оплаты и сертификации согласовываются индивидуально после уточнения спецификации заказа.")}
      <a class="btn btn-outline" href="terms.html" style="justify-self:start">Подробнее об условиях {icon("arrow")}</a>
    </div>
    <div class="terms compact">{terms}</div>
  </div>
</section>

<section class="section section-alt" id="form">
  <div class="container form-shell">
    <div class="stack">
      {section_head("04 · Запрос", "Обсудить комплектацию поставки", "Подготовим расчёт стоимости, сроков и условий под задачи вашего проекта.")}
      <ul class="dir-list" style="border:0;padding:0">
        <li>Сельхоздроны — 8 моделей: опрыскиватели и погрузчики</li>
        <li>FPV-комплексы ZTK — 4 рамы, аккумуляторы, комплектующие</li>
        <li>Оптоволокно — 4 катушки, воздушный и наземный модули</li>
      </ul>
    </div>
    {request_form()}
  </div>
</section>'''
    ld = [{"@context": "https://schema.org", **ORG},
          {"@context": "https://schema.org", "@type": "WebSite", "name": "XELON AERO", "url": S["url"], "inLanguage": "ru"}]
    return page("index.html", "XELON AERO — поставка сельхоздронов, дронов-погрузчиков и FPV-систем",
                "Поставка сельскохозяйственных дронов-опрыскивателей 20/30/50 л, погрузчиков 15–200 кг, FPV-комплексов ZTK и оптоволоконных систем связи. FOB Шэньчжэнь, B2B.",
                body, ld)

def build_agro():
    hero, bl = page_hero([("index.html", "Главная"), ("catalog.html", "Каталог"), ("agro.html", "Сельхоздроны")],
                         "Направление 01 · Сельхоздроны", "Сельскохозяйственные дроны-опрыскиватели и погрузчики",
                         "Четырёхроторные платформы для внесения СЗР и рассева удобрений и грузовые платформы для транспортировки и внесения сыпучих материалов.",
                         ["3 модели опрыскивателей", "5 моделей погрузчиков", "IP65", "≥1000 циклов зарядки", "FOB Шэньчжэнь"])
    spr = by(sub="sprayer")
    head = "".join(f'<th scope="col" class="num">{esc(p["short"].upper())}<span class="th-sub">{rub(p["price"])}</span></th>' for p in spr)
    rows = "".join(f'<tr><th scope="row">{esc(r[0])}</th>' + "".join(f'<td class="num">{esc(v)}</td>' for v in r[1:]) + '</tr>' for r in D.SPRAYER_TABLE)
    load = by(sub="loader")
    lrows = "".join(f'<tr><th scope="row" class="model">{m}</th><td class="num">{kg} кг</td><td>{esc(b)}</td><td>{esc(mo)}</td><td>{esc(rc)}</td></tr>' for m, kg, b, mo, rc, n in D.LOADERS)
    kit = [("drone", "Дрон-платформа в сборе"), ("battery", "Аккумуляторы (2 шт.*)"), ("plug", "Зарядное устройство"), ("remote", "Пульт ДУ и полётный контроллер")]
    kit_html = "".join(f'<div class="kit"><span class="kit-icon">{icon(i)}</span><b>{t}</b></div>' for i, t in kit)
    body = f'''{hero}
<section class="section" id="sprayers">
  <div class="container">
    {section_head("01.1 · Опрыскиватели / разбрасыватели", "Дроны-опрыскиватели 20 / 30 / 50 л", "Защита IP65, ≥1000 циклов зарядки. Цены — FOB Шэньчжэнь, руб. без НДС.", currency_toggle())}
    <div class="product-grid cols-3">{''.join(product_card(p) for p in spr)}</div>
    <h3 class="mt-48" style="font-size:24px;margin-bottom:16px">Сравнение характеристик</h3>
    <div class="table-wrap" tabindex="0" role="region" aria-label="Сравнение опрыскивателей">
      <table class="data-table sticky-first"><thead><tr><th scope="col">Характеристика</th>{head}</tr></thead><tbody>{rows}</tbody></table>
    </div>
    {table_hint()}
  </div>
</section>

<section class="section section-alt" id="loaders">
  <div class="container">
    {section_head("01.2 · Погрузчики-разбрасыватели", "Дроны-погрузчики и разбрасыватели", "Пять типоразмеров грузоподъёмностью от 15 до 200 кг для транспортировки и внесения сыпучих материалов.")}
    <div class="split-2 wide-left">
      <div>
        <div class="table-wrap" tabindex="0" role="region" aria-label="Модели погрузчиков">
          <table class="data-table sticky-first"><thead><tr><th scope="col">Модель</th><th scope="col">Грузоподъём.</th><th scope="col">Аккумулятор</th><th scope="col">Двигатели</th><th scope="col">Пульт / контроллер</th></tr></thead><tbody>{lrows}</tbody></table>
        </div>
        {table_hint()}
      </div>
      <figure class="figure" style="margin:0"><img src="assets/img/products/loader-s616.jpg" alt="Дрон-погрузчик S616" width="661" height="399" loading="lazy" decoding="async"><figcaption>S616 — базовая платформа линейки погрузчиков</figcaption></figure>
    </div>
    <h3 class="mt-48" style="font-size:24px;margin-bottom:16px">Что входит в поставку</h3>
    <div class="kit-grid">{kit_html}</div>
    <p class="muted small mt-16">* Зарядное устройство и комплект аккумуляторов входят в стандартную поставку каждой модели; точная спецификация зарядного блока уточняется при заказе.</p>
    <h3 class="mt-48" style="font-size:24px;margin-bottom:16px">Карточки моделей</h3>
    <div class="product-grid cols-3">{''.join(product_card(p) for p in load)}</div>
    <div class="mt-24">{notice(S["disclaimer"] + " Для моделей без фото показаны схематичные изображения.")}</div>
  </div>
</section>
{cta_band()}'''
    return page("agro.html", "Сельхоздроны: опрыскиватели 20/30/50 л и погрузчики 15–200 кг — XELON AERO",
                "Дроны-опрыскиватели 20, 30 и 50 л (FOB от 600 000 руб. без НДС), погрузчики-разбрасыватели S616, S630, S450, S100pro, S200pro. Полные ТТХ и комплектация.",
                body, [bl, itemlist_ld(spr + load, "Сельскохозяйственные дроны")], og_img="assets/img/products/sprayer-30l.jpg")

def build_fpv():
    hero, bl = page_hero([("index.html", "Главная"), ("catalog.html", "Каталог"), ("fpv.html", "FPV-комплексы ZTK")],
                         "Направление 02 · FPV-комплексы", "FPV-комплексы ZTK: рамы 7″–15″, аккумуляторы и комплектующие",
                         "Компактные скоростные рамы для мониторинга, инспекции и облёта и тяжёлые рамы повышенной грузоподъёмности для доставки полезной нагрузки и работы с оптоволоконным модулем.",
                         ["4 модели рам", "до 160 км/ч", "до 8 кг нагрузки", "6 типов аккумуляторов", "ELRS915"])
    frames = by(sub="frame")
    bats = by(sub="battery")
    accs = by(sub="accessory")
    brow = "".join(f'<tr><th scope="row" class="model">{esc(t)}</th><td>{esc(ch)}</td><td class="num">{size}</td><td class="num">{w}</td><td class="price" data-rub="{pr}">{rub(pr)}</td></tr>' for t, ch, size, w, pr in D.BATTERIES)
    compat = '<div class="compat-row compat-head"><b>Аккумулятор</b><span>Рамы ZTK</span></div>' + "".join(f'<div class="compat-row"><b>{a}</b><span>{b}</span></div>' for a, b in D.COMPAT)
    body = f'''{hero}
<section class="section" id="frames">
  <div class="container">
    {section_head("02.1 · Рамы", "FPV-дроны ZTK AN-7, AN-10, AN-13B, AN-15B", "Контроллер F405 V3, рама Mark4 тип X, связь ELRS915. Цены — руб. без НДС за единицу.", currency_toggle())}
    <div class="product-grid cols-4">{''.join(product_card(p) for p in frames)}</div>
  </div>
</section>

<section class="section section-alt" id="batteries">
  <div class="container">
    {section_head("02.2 · Аккумуляторы", "Аккумуляторы для FPV-дронов", "Шесть типоразмеров LiPo-аккумуляторов 6S / 8S с разъёмом XT60 / XT90 под все модели линейки ZTK. Поставляются отдельно от рам и подбираются под требуемое время полёта.")}
    <div class="split-2 wide-left">
      <div>
        <div class="table-wrap" tabindex="0" role="region" aria-label="Аккумуляторы">
          <table class="data-table sticky-first"><thead><tr><th scope="col">Тип</th><th scope="col">Характеристики</th><th scope="col">Размер</th><th scope="col">Вес</th><th scope="col">Цена за шт.<span class="th-sub">Q&lt;1000, без НДС</span></th></tr></thead><tbody>{brow}</tbody></table>
        </div>
        {table_hint()}
      </div>
      <div class="stack">
        <h3 style="font-size:20px">Совместимость с рамами</h3>
        <div class="compat">{compat}</div>
        {notice("Тарификация аккумуляторов — по объёму заказа.")}
      </div>
    </div>
  </div>
</section>

<section class="section" id="accessories">
  <div class="container">
    {section_head("02.3 · Комплектующие", "Комплектующие и наземное оборудование", "Пульты управления, приёмные модули, видеоочки, экраны и зарядные устройства.")}
    <div class="product-grid cols-3">{''.join(product_card(p) for p in accs)}</div>
    <div class="mt-24">{notice(S["disclaimer"] + " Стоимость снижается при увеличении объёма заказа.")}</div>
  </div>
</section>
{cta_band()}'''
    return page("fpv.html", "FPV-комплексы ZTK: рамы AN-7, AN-10, AN-13B, AN-15B — XELON AERO",
                "FPV-дроны ZTK AN-7 (30 000 ₽), AN-10, AN-13B, AN-15B (54 000 ₽), LiPo-аккумуляторы 6S/8S, пульт RadioMaster TX12, ELRS 915, очки 5.8G, зарядные устройства.",
                body, [bl, itemlist_ld(frames + bats + accs, "FPV-комплексы ZTK")], og_img="assets/img/products/fpv-an13b.jpg")

def build_fiber():
    hero, bl = page_hero([("index.html", "Главная"), ("catalog.html", "Каталог"), ("fiber.html", "Оптоволоконные системы")],
                         "Направление 03 · Оптоволоконные системы", "Оптоволоконные комплекты связи",
                         "Катушки оптоволокна 10–30 км и модули воздушного/наземного конца ZR LINK для устойчивой помехозащищённой связи.",
                         ["4 длины катушек", "до 30 км", "Модули ZR LINK", "Корпус — алюминиевый сплав"])
    spools, mods = by(sub="spool"), by(sub="module")
    srow = "".join(f'<tr><th scope="row" class="model">{m}</th><td class="num">{km} км</td><td class="num">{size}</td><td class="num">{w}</td><td class="price" data-rub="{pr}">{rub(pr)}</td></tr>' for m, km, size, w, pr in D.SPOOLS)
    tiers = "".join(f'<div class="tier"><span class="step">{s}</span><span class="qty">{q}</span><div class="bar"><i style="width:{pc}%"></i></div><p>{"Цены по прайсу" if i==0 else "Сниженная цена — по запросу"}</p></div>' for i, (s, q, pc) in enumerate(D.FIBER_TIERS))
    body = f'''{hero}
<section class="section" id="spools">
  <div class="container">
    {section_head("03.1 · Катушки", "Катушки оптоволокна 10 / 15 / 20 / 30 км", "Цены — руб. без НДС за штуку.", currency_toggle())}
    <div class="product-grid cols-4">{''.join(product_card(p) for p in spools)}</div>
    <div class="table-wrap mt-32" tabindex="0" role="region" aria-label="Сравнение катушек">
      <table class="data-table sticky-first"><thead><tr><th scope="col">Модель</th><th scope="col">Длина</th><th scope="col">Размер</th><th scope="col">Вес</th><th scope="col">Цена за шт.</th></tr></thead><tbody>{srow}</tbody></table>
    </div>
    {table_hint()}
  </div>
</section>

<section class="section section-alt" id="modules">
  <div class="container">
    {section_head("03.2 · Модули связи", "Модули воздушного и наземного конца ZR LINK", "Воздушный модуль устанавливается на борт, наземный — подключается к станции оператора.")}
    <div class="product-grid cols-2">{''.join(product_card(p) for p in mods)}</div>
  </div>
</section>

<section class="section" id="tiers">
  <div class="container">
    {section_head("03.3 · Тарифные ступени", "Цена зависит от объёма заказа", "Стоимость оптоволоконных систем и FPV-дронов снижается при увеличении объёма — по три тарифные ступени на каждую позицию.")}
    <div class="tier-grid">{tiers}</div>
    <div class="mt-24">{notice("Цены по данным производителя, уточняются при заказе. Стоимость для второй и третьей ступени рассчитывается по запросу.")}</div>
  </div>
</section>
{cta_band()}'''
    return page("fiber.html", "Оптоволоконные системы связи: катушки 10–30 км и модули ZR LINK — XELON AERO",
                "Катушки оптоволокна ZR010, ZR015, ZR020, ZR030 (27 000–68 000 ₽ без НДС) и модули воздушного/наземного конца ZR LINK для помехозащищённой связи.",
                body, [bl, itemlist_ld(spools + mods, "Оптоволоконные системы")], og_img="assets/img/products/zr-link-ground.jpg")

def build_catalog():
    hero, bl = page_hero([("index.html", "Главная"), ("catalog.html", "Каталог")],
                         "Каталог техники", "Каталог беспилотных авиационных комплексов",
                         "30 позиций в трёх направлениях. Фильтруйте по категории, типу, цене и грузоподъёмности — и отправьте запрос на расчёт.")
    cats = [("all", "Все", len(D.P))] + [(k, v["title"], len(by(cat=k))) for k, v in D.CATEGORIES.items()]
    seg = "".join(f'<label><input type="radio" name="cat" value="{k}"{" checked" if k=="all" else ""}><span>{t} <span class="count">{n}</span></span></label>' for k, t, n in cats)
    subopts = "".join(f'<option value="{k}" data-cat="{next(p["cat"] for p in D.P if p["sub"]==k)}">{v}</option>' for k, v in D.SUBTYPES.items())
    cards = "".join(product_card(p, show_tag=True) for p in D.P)
    body = f'''{hero}
<section class="section-sm">
  <div class="container catalog-layout">
    <div class="stack" style="gap:12px">
      <button class="btn btn-outline filters-toggle" type="button" aria-expanded="false" aria-controls="filters">{icon("filter")} Фильтры</button>
      <form class="filters collapsed" id="filters" aria-label="Фильтры каталога" onsubmit="return false">
        <fieldset class="f-group"><legend>Категория</legend><div class="seg">{seg}</div></fieldset>
        <div class="f-group"><label class="f-label" for="f-sub">Тип техники</label>
          <select class="select" id="f-sub" name="sub"><option value="">Все типы</option>{subopts}</select></div>
        <div class="f-group"><label class="f-label" for="f-price">Цена, руб. без НДС</label>
          <select class="select" id="f-price" name="price"><option value="">Любая</option><option value="0-20000">до 20 000 ₽</option><option value="0-50000">до 50 000 ₽</option><option value="0-100000">до 100 000 ₽</option><option value="100000-700000">100 000 – 700 000 ₽</option><option value="700000-">от 700 000 ₽</option></select>
          <label class="check"><input type="checkbox" name="priced"> Только с указанной ценой</label></div>
        <div class="f-group"><label class="f-label" for="f-payload">Грузоподъёмность / нагрузка</label>
          <select class="select" id="f-payload" name="payload"><option value="">Любая</option><option value="1">от 1 кг</option><option value="5">от 5 кг</option><option value="15">от 15 кг</option><option value="30">от 30 кг</option><option value="50">от 50 кг</option><option value="100">от 100 кг</option></select>
          <span class="hint">Для FPV — номинальная нагрузка</span></div>
        <button class="btn btn-outline btn-sm" type="reset" data-reset>Сбросить фильтры</button>
      </form>
    </div>
    <div>
      <div class="catalog-bar">
        <p class="result-count" aria-live="polite">Найдено: <span data-count>{len(D.P)}</span></p>
        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
          {currency_toggle()}
          <label class="sr-only" for="f-sort">Сортировка</label>
          <select class="select" id="f-sort" style="width:auto;min-width:210px"><option value="">По направлениям</option><option value="price-asc">Цена по возрастанию</option><option value="price-desc">Цена по убыванию</option><option value="payload-desc">Грузоподъёмность ↓</option></select>
        </div>
      </div>
      <div class="product-grid cols-3" data-catalog>{cards}</div>
      <div class="empty-state" data-empty><p style="font-weight:700;color:var(--text);font-size:18px">Ничего не найдено</p><p class="mt-8">Измените параметры фильтра или <a href="contacts.html#form">опишите задачу в заявке</a>.</p></div>
      <div class="mt-24">{notice(S["disclaimer"] + " " + S["price_note"])}</div>
    </div>
  </div>
</section>
{cta_band()}'''
    return page("catalog.html", "Каталог: сельхоздроны, FPV-комплексы, оптоволоконные системы — XELON AERO",
                "Каталог XELON AERO: дроны-опрыскиватели, погрузчики до 200 кг, FPV-рамы ZTK, аккумуляторы, комплектующие, катушки оптоволокна 10–30 км. Фильтр по цене и грузоподъёмности.",
                body, [bl, itemlist_ld(D.P, "Каталог XELON AERO")])

def build_terms():
    hero, bl = page_hero([("index.html", "Главная"), ("terms.html", "Условия сотрудничества")],
                         "Коммерческие условия", "Условия сотрудничества",
                         "Базис поставки, валюта расчётов, ценовые ступени и индивидуальная комплектация под задачи заказчика.")
    terms = "".join(f'<div class="term"><div class="term-k"><span class="kit-icon">{icon(i)}</span>{k}</div><p class="term-v">{v}</p></div>' for i, k, v in D.TERMS)
    tiers = "".join(f'<div class="tier"><span class="step">{s}</span><span class="qty">{q}</span><div class="bar"><i style="width:{pc}%"></i></div></div>' for s, q, pc in D.FIBER_TIERS)
    feats = [
        ("ship", "Экспорт", "Поставка техники на условиях FOB Шэньчжэнь / со склада поставщика. Логистика, сроки и сертификация согласовываются под конкретную спецификацию."),
        ("handshake", "Партнёрство", "Работаем с дистрибьюторами, интеграторами и агрохолдингами: объёмные ступени цен на FPV-дроны и оптоволоконные системы."),
        ("wrench", "Работа под заказ", "Количество моделей и позиций комплектующих формируется индивидуально — от одной платформы до комплексной поставки трёх линеек."),
    ]
    f_html = "".join(f'<div class="feat"><span class="kit-icon">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in feats)
    steps = [("Запрос", "Направьте перечень интересующих моделей и требуемый объём."),
             ("Расчёт", "Готовим расчёт стоимости, сроков и условий поставки."),
             ("Спецификация", "Согласуем комплектацию, условия оплаты и сертификации."),
             ("Поставка", "Отгрузка на согласованном базисе поставки.")]
    s_html = "".join(f'<li><b>{t}</b><p>{d}</p></li>' for t, d in steps)
    body = f'''{hero}
<section class="section">
  <div class="container">
    {section_head("01 · Условия поставки", "Базовые коммерческие условия")}
    <div class="terms">{terms}</div>
    <div class="mt-24">{notice("Точные сроки поставки, условия оплаты и сертификации согласовываются индивидуально после уточнения спецификации заказа.")}</div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head("02 · Ценовые ступени", "Три тарифные ступени по объёму", "Действуют для FPV-дронов и оптоволоконных систем — на каждую позицию.")}
    <div class="tier-grid">{tiers}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    {section_head("03 · Для B2B", "Экспорт, партнёрство и работа под заказ")}
    <div class="feat-grid">{f_html}</div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head("04 · Порядок работы", "Как проходит поставка")}
    <ol class="steps">{s_html}</ol>
  </div>
</section>
{cta_band()}'''
    return page("terms.html", "Условия сотрудничества и поставки — XELON AERO",
                "Базис поставки FOB Шэньчжэнь / со склада поставщика, расчёты в рублях, три ценовые ступени по объёму, индивидуальная комплектация. Экспорт и партнёрство.",
                body, [bl])

def build_about():
    hero, bl = page_hero([("index.html", "Главная"), ("about.html", "О компании")],
                         "XELON TECHNOLOGY GROUP", "XELON AERO — поставщик полного спектра беспилотной техники",
                         "Направление группы компаний XELON, отвечающее за экспорт и партнёрство в сегменте беспилотных авиационных комплексов.")
    body = f'''{hero}
<section class="section">
  <div class="container split-2">
    <div class="stack">
      {section_head("01 · О нас", "Комплексная поставка беспилотных авиационных комплексов")}
      <p style="font-size:17.5px;color:var(--text-2)">XELON AERO формирует поставку из трёх линеек беспилотной техники: сельскохозяйственные дроны-опрыскиватели и разбрасыватели, грузовые дроны-погрузчики и FPV-комплексы для съёмки, мониторинга и специальных задач, а также оптоволоконные системы связи.</p>
      <p style="font-size:17.5px;color:var(--text-2)">Каждая позиция подобрана с полными техническими характеристиками, комплектацией и ценой FOB Шэньчжэнь — для быстрого принятия решения на стороне заказчика.</p>
    </div>
    <div class="org" aria-label="Структура группы">
      <div class="org-node primary"><small>Головная компания</small><b>{S["parent"]}</b></div>
      <div class="org-link"></div>
      <div class="org-node"><small>Ответственное направление</small><b>{S["unit"]} — экспорт и партнёрство</b></div>
      <div class="org-link"></div>
      <div class="org-node"><small>Бренд направления</small><b>XELON AERO</b><span class="muted small">Сельхоздроны · FPV-комплексы ZTK · Оптоволоконные системы</span></div>
    </div>
  </div>
</section>
<section class="dark metrics" aria-label="Ключевые показатели"><div class="container"><div class="metrics-grid">
  {''.join(f'<div class="metric"><span class="metric-icon">{icon(i)}</span><div><div class="metric-value">{count_wrap(v)}</div><div class="metric-label">{l}</div></div></div>' for i, v, l in [("layers","3","категории техники"),("drone","9","моделей дронов в линейке"),("battery","4","модели FPV-дронов ZTK"),("signal","30 км","дальность оптоволокна"),("shield","IP65","защита сельхоздронов"),("weight","до 200 кг","грузоподъёмность")])}
</div></div></section>
<section class="section">
  <div class="container">
    {section_head("02 · Принципы", "Precision · Scale · Technology")}
    <div class="pillars">
      <div class="pillar"><span class="mono">PRECISION</span><h3>Точность данных</h3><p>Полные технические характеристики по каждой позиции — по данным производителя.</p></div>
      <div class="pillar"><span class="mono">SCALE</span><h3>Масштаб поставки</h3><p>Ценовые ступени по объёму и формирование комплектации под задачи заказчика.</p></div>
      <div class="pillar"><span class="mono">TECHNOLOGY</span><h3>Технологичная линейка</h3><p>Беспилотная техника для сельского хозяйства, мониторинга и специальных задач.</p></div>
    </div>
  </div>
</section>
{cta_band()}'''
    ld = [bl, {"@context": "https://schema.org", "@type": "AboutPage", "name": "О компании XELON AERO", "about": ORG}]
    return page("about.html", "О компании — XELON AERO (ГК XELON)",
                "XELON AERO — направление группы компаний XELON по экспорту и партнёрству: поставка сельхоздронов, погрузчиков, FPV-комплексов и оптоволоконных систем.", body, ld)

def build_contacts():
    hero, bl = page_hero([("index.html", "Главная"), ("contacts.html", "Контакты")],
                         "Контакты", "Запросить коммерческое предложение",
                         "Направьте перечень интересующих моделей и требуемый объём — подготовим точный расчёт стоимости, сроков и условий поставки.")
    body = f'''{hero}
<section class="section section-alt" id="form">
  <div class="container form-shell">
    <div class="stack" style="gap:24px">
      <div class="panel panel-dark stack">
        <h3 style="font-size:20px">Связаться напрямую</h3>
        <ul class="contact-list">
          <li><span class="kit-icon">{icon("mail")}</span><div><small>Email</small><a href="mailto:{S['email']}">{S['email']}</a></div></li>
          <li><span class="kit-icon">{icon("globe")}</span><div><small>Сайт группы</small><a href="https://{S['site_label']}" rel="noopener">{S['site_label']}</a></div></li>
          <li><span class="kit-icon">{icon("handshake")}</span><div><small>Ответственное направление</small><span class="v">{S['unit']} — экспорт и партнёрство</span></div></li>
        </ul>
        <div class="messengers">
          <a class="btn btn-ghost btn-sm" href="{S['telegram']}" rel="noopener" target="_blank">{icon("send")} Telegram</a>
          <a class="btn btn-ghost btn-sm" href="{S['whatsapp']}" rel="noopener" target="_blank">{icon("chat")} WhatsApp</a>
        </div>
      </div>
      <div class="panel stack">
        <h3 style="font-size:18px">Что указать в запросе</h3>
        <ul class="dir-list" style="border:0;padding:0;margin:0">
          <li>Модели и позиции комплектующих</li><li>Требуемый объём (влияет на ценовую ступень)</li><li>Задачи и регион поставки</li>
        </ul>
      </div>
      {notice(S["disclaimer"])}
    </div>
    {request_form()}
  </div>
</section>'''
    ld = [bl, {"@context": "https://schema.org", "@type": "ContactPage", "name": "Контакты XELON AERO",
               "mainEntity": {**ORG, "contactPoint": {"@type": "ContactPoint", "email": S["email"], "contactType": "sales", "availableLanguage": ["ru"]}}}]
    return page("contacts.html", "Контакты и запрос КП — XELON AERO",
                f"Запросите коммерческое предложение на поставку дронов XELON AERO: форма заявки, email {S['email']}, Telegram и WhatsApp для B2B.", body, ld)

def build_404():
    body = f'''<section class="dark grid-bg page-hero" style="min-height:60vh;display:grid;align-items:center"><div class="container">
<p class="eyebrow">Ошибка 404</p><h1>Страница не найдена</h1><p class="lead">Возможно, она была перемещена. Перейдите в каталог или на главную.</p>
<div class="hero-actions"><a class="btn btn-primary" href="catalog.html">Каталог</a><a class="btn btn-ghost" href="index.html">На главную</a></div></div></section>'''
    return page("404.html", "Страница не найдена — XELON AERO", "Страница не найдена.", body).replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">')

# ------------------------------------------------------------------ write
def main():
    pages = {"index.html": build_index, "catalog.html": build_catalog, "agro.html": build_agro, "fpv.html": build_fpv,
             "fiber.html": build_fiber, "terms.html": build_terms, "about.html": build_about, "contacts.html": build_contacts,
             "404.html": build_404}
    for name, fn in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(fn())
    pri = {"index.html": "1.0", "catalog.html": "0.9", "agro.html": "0.9", "fpv.html": "0.9", "fiber.html": "0.9", "contacts.html": "0.8", "terms.html": "0.7", "about.html": "0.6"}
    urls = "".join(f'  <url><loc>{S["url"]}/{"" if n=="index.html" else n}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for n, p in pri.items())
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {S['url']}/sitemap.xml\n")
    open(os.path.join(ROOT, "assets/img/logo.svg"), "w").write(LOGO_MARK.replace(' class="logo-mark"', ' xmlns="http://www.w3.org/2000/svg"'))
    print("built", len(pages), "pages")

if __name__ == "__main__":
    main()
