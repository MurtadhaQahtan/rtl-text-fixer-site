# rtl-text-fixer-site

Static GitHub Pages site for **RTL Text Fixer** (Windows): https://murtadhaqahtan.github.io/rtl-text-fixer-site/

- `_src/` — generator: `python3 _src/demo.py && python3 _src/extras.py && python3 _src/gen.py .`
  (content in `content_*.py`; demo images are rendered with Pillow's basic layout engine, i.e. without shaping or bidi,
  to show how an app without RTL support displays the text before and after fixing; outputs come from the app's engine, `fixed.json`).
- **Store link placeholder:** the app is not published yet. Set `STORE_ID` (and optionally `PRICE`) at the top of
  `_src/gen.py` once the Microsoft Store ID exists and regenerate; until then the pages show "release pending" and the
  JSON-LD has no install URL or offer.
- `9443d8c6da851106dd0766ea9666bc49.txt` — IndexNow key (same key as the host root).
