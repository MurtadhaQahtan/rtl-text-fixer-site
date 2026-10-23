# -*- coding: utf-8 -*-
"""Static site generator for https://murtadhaqahtan.github.io/rtl-text-fixer-site/ . Run from the repo root:
   python3 _src/demo.py && python3 _src/gen.py ."""
import json, re, html, os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from content_en import EN
from content_rtl import AR, FA, UR, HE
from content_ltr import TR, RU, ES, FR, DE, PT, HI
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
ORIGIN = 'https://murtadhaqahtan.github.io'
BASE = ORIGIN + '/rtl-text-fixer-site/'
P = '/rtl-text-fixer-site/'
# ---------------------------------------------------------------------------------------------------------------
# STORE PLACEHOLDER: the app is not in the Microsoft Store yet (name not reserved). When the Store ID exists, set
# STORE_ID = '9NXXXXXXXXXX' (and PRICE if wanted) and regenerate: Store badges, "offers" and installUrl appear.
STORE_ID = None
PRICE = None          # e.g. '2.99' (USD) — only once the price is set in Partner Center
# ---------------------------------------------------------------------------------------------------------------
STORE = f'https://apps.microsoft.com/detail/{STORE_ID}' if STORE_ID else None
README_REPO = 'https://github.com/MurtadhaQahtan/rtl-text-fixer-app'
TODAY = datetime.date.today().isoformat()
LANGS = [EN, AR, FA, UR, HE, TR, RU, ES, FR, DE, PT, HI]
UI_LANGS = ['en', 'ar', 'fa', 'ur', 'he', 'tr', 'ru', 'es', 'fr', 'de', 'pt-BR', 'hi']
SHOT = {'ar': 'shot-ar.png', 'he': 'shot-he.png', 'ur': 'shot-ur.png'}  # localized UI screenshots where we have them
SAMPLES = json.load(open(os.path.join(os.path.dirname(__file__), 'samples.json'), encoding='utf-8'))

def strip(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
def url(L): return BASE + L['path']
CSS = open(os.path.join(os.path.dirname(__file__), 'style.css'), encoding='utf-8').read()

def jsonld(L):
    app = {
      "@type": "SoftwareApplication", "@id": BASE + "#app",
      "name": "RTL Text Fixer",
      "description": strip(L['desc']),
      "url": url(L), "sameAs": [README_REPO],
      "applicationCategory": "UtilitiesApplication",
      "applicationSubCategory": "Arabic reshaper / right-to-left text converter",
      "operatingSystem": "Windows 10 (version 1809 or later), Windows 11",
      "processorRequirements": "x64, ARM64",
      "softwareVersion": "1.0",
      "inLanguage": UI_LANGS,
      "featureList": [strip(f) for f in L['features']],
      "image": BASE + "img/icon-192.png",
      "screenshot": BASE + "img/shot-en.png",
      "author": {"@type": "Person", "name": "Murtadha Qahtan", "url": "https://github.com/MurtadhaQahtan"},
    }
    if STORE:
        app["installUrl"] = app["downloadUrl"] = STORE
        app["sameAs"].append(STORE)
        if PRICE:
            app["offers"] = {"@type": "Offer", "price": PRICE, "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": STORE}
    faq = {"@type": "FAQPage", "@id": url(L) + "#faq", "inLanguage": L['hreflang'],
           "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in L['faq']]}
    page = {"@type": "WebPage", "@id": url(L) + "#page", "url": url(L), "name": strip(L['title']),
            "description": strip(L['desc']), "inLanguage": L['hreflang'], "dateModified": TODAY,
            "about": {"@id": BASE + "#app"}, "mainEntity": {"@id": BASE + "#app"}}
    return json.dumps({"@context": "https://schema.org", "@graph": [page, app, faq]}, ensure_ascii=False, indent=1)

def page(L):
    e = html.escape
    alt = '\n'.join(f'<link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x)}">' for x in LANGS)
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    nav = ' · '.join((f'<b>{x["native"]}</b>' if x is L else f'<a href="{P}{x["path"]}" hreflang="{x["hreflang"]}" lang="{x["hreflang"]}">{x["native"]}</a>') for x in LANGS)
    cta = (f'<a class="badge" href="{STORE}" rel="noopener">Microsoft Store</a>' if STORE else f'<p class="pending">{e(L["store_note"])}</p>')
    demos = '\n'.join(f'<img class="demo" src="{P}img/demo-{k}.png" loading="lazy" alt="{e(SAMPLES[k])}">' for k in L['demos'])
    how = '\n'.join(f'<li>{s}</li>' for s in L['how'])
    feats = '\n'.join(f'<li>{s}</li>' for s in L['features'])
    lims = '\n'.join(f'<li>{s}</li>' for s in L['limits'])
    faq = '\n'.join(f'<details open><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>' for q, a in L['faq'])
    shot = SHOT.get(L['code'], 'shot-en.png')
    return f'''<!doctype html>
<html lang="{L['hreflang']}" dir="{L['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(L['title'])}</title>
<meta name="description" content="{e(L['desc'])}">
<link rel="canonical" href="{url(L)}">
{alt}
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(L['title'])}">
<meta property="og:description" content="{e(L['desc'])}">
<meta property="og:url" content="{url(L)}">
<meta property="og:image" content="{BASE}img/og.png">
<meta property="og:locale" content="{L['hreflang'].replace('-', '_')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{P}img/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="{P}img/icon-192.png">
<style>{CSS}</style>
<script type="application/ld+json">
{jsonld(L)}
</script>
</head>
<body>
<nav class="langs" aria-label="{e(L['other'])}">{nav}</nav>
<header>
<img src="{P}img/icon-192.png" width="96" height="96" alt="RTL Text Fixer">
<h1>{e(L['h1'])}</h1>
<p class="lead">{L['lead']}</p>
{cta}
</header>
<main>
<section><h2>{e(L['demo_title'])}</h2>
{demos}
<p class="note">{e(L['demo_caption'])}</p></section>
<section><h2>{e(L['how_title'])}</h2><ol>
{how}
</ol>
<img class="shot" src="{P}img/{shot}" width="1266" height="773" loading="lazy" alt="{e(L['shot_alt'])}">
</section>
<section><h2>{e(L['langs_title'])}</h2><p>{L['langs']}</p></section>
<section><h2>{e(L['features_title'])}</h2><ul>
{feats}
</ul></section>
<section><h2>{e(L['limits_title'])}</h2><ul>
{lims}
</ul></section>
<section id="faq"><h2>{e(L['faq_title'])}</h2>
{faq}
</section>
</main>
<footer>
<p><a href="{P}privacy.html">{e(L['privacy'])}</a> · {e(L['support'])}: <a href="mailto:hibari@mail.grokbot.com">hibari@mail.grokbot.com</a> · <a href="{README_REPO}">GitHub</a></p>
<p class="note">{e(L['source_note'])}</p>
<nav class="langs">{nav}</nav>
</footer>
</body>
</html>
'''

for L in LANGS:
    d = os.path.join(OUT, L['path']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(L))

items = []
for L in LANGS:
    links = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x)}"/>' for x in LANGS)
    links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    items.append(f'  <url>\n    <loc>{url(L)}</loc>\n    <lastmod>{TODAY}</lastmod>{links}\n  </url>')
for extra in ('privacy.html', 'llms.txt'):
    items.append(f'  <url>\n    <loc>{BASE}{extra}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>')
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(items) + '\n</urlset>\n')
open(os.path.join(OUT, '_src', 'urls.txt'), 'w').write('\n'.join([url(L) for L in LANGS] + [BASE + 'privacy.html', BASE + 'llms.txt', BASE + 'sitemap.xml']) + '\n')
print('ok', len(LANGS))
