# XELON AERO — корпоративный сайт (статический HTML/CSS/JS)

Сборка не нужна: залейте содержимое папки на любой хостинг (nginx, Apache, Netlify, GitHub Pages, S3). `index.html` — главная.

## Страницы
- `index.html` — главная
- `catalog.html` — весь каталог с фильтрами (категория, тип, цена, грузоподъёмность, сортировка; параметры в URL)
- `agro.html`, `fpv.html`, `fiber.html` — разделы каталога
- `terms.html` — условия, `about.html` — о компании, `contacts.html` — контакты и форма
- `404.html`, `sitemap.xml`, `robots.txt`

## Перед запуском
1. **Форма**: на formspree.io создайте форму, вставьте ID в `assets/js/config.js` (`formEndpoint`). Для своей CRM укажите `crmWebhook` (POST JSON).
2. **Мессенджеры**: Telegram и WhatsApp в `_build/data.py` → `SITE` (сейчас заглушки), затем пересоберите.
3. **Домен**: `SITE.url` в `_build/data.py` (canonical, sitemap, Open Graph). Сейчас стоит gk-xelon.ru.
4. **Курс RMB** (необязательно): `rubPerCny` в `config.js`. После этого на страницах с ценами появится переключатель ₽/¥.
5. **Фото**: `assets/img/products/` — изображения из презентации, разрешение низкое. Замените их файлами крупнее с теми же именами. Для S630, S450, S100pro и S200pro фото нет, поэтому на карточках стоят схемы.

## Как менять данные
Все цены и ТТХ хранятся в `_build/data.py` (взяты из «Дроны Презентация.pdf»). После правки выполните
`python3 _build/build.py` (Python 3.9+, Pillow) — HTML, JSON-LD (Product/Offer, BreadcrumbList) и sitemap пересоберутся.
Папку `_build/` на хостинг загружать не обязательно.
