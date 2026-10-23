# rtl-text-fixer-site

Static GitHub Pages site for **RTL Text Fixer** (Windows): https://murtadhaqahtan.github.io/rtl-text-fixer-site/

- `_src/` — generator: `python3 _src/demo.py && python3 _src/extras.py && python3 _src/gen.py .`
  (content in `content_*.py`; demo images are rendered with Pillow's basic layout engine, i.e. without shaping or bidi,
  to show how an app without RTL support displays the text before and after fixing; outputs come from the app's engine, `fixed.json`).
- Store: `STORE_ID = '9NQC161JJM09'`, `PRICE = '2.99'` at the top of `_src/gen.py` (Store badges, installUrl and offer
  in the JSON-LD). Set `STORE_ID = None` to fall back to the "release pending" wording.
- `9443d8c6da851106dd0766ea9666bc49.txt` — IndexNow key (same key as the host root).
