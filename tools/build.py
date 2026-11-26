"""Builds the Marlowby site (v2, logo-matched design). Usage: python3 build2.py <site folder>"""
import sys, pathlib, html as H

OUT = pathlib.Path(sys.argv[1])
VER = "57"  # bump to make browsers reload css/js

# ------------------------------------------------------------------ helpers
PIN = ('<svg class="wm-o" viewBox="0 0 50 64" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" '
       'd="M25 63S5 41 5 24a20 20 0 0 1 40 0c0 17-20 39-20 39zm0-46.5a7.5 7.5 0 1 0 0 15 7.5 7.5 0 0 0 0-15z"/></svg>')

def wm(cls=""):
    """The Marlowby wordmark, with the map-pin "o" from the logo."""
    return (f'<span class="wm {cls}"><span class="visually-hidden">Marlowby</span>'
            f'<span aria-hidden="true">Marl{PIN}wby</span></span>')

def lines(*parts):
    """Heading text split into lines that slide up one at a time."""
    return "".join(f'<span class="line"><span>{p}</span></span>' for p in parts)

NAV = [("how-it-works.html", "How it works"), ("plans.html", "Plans"), ("cities.html", "Cities"),
       ("about.html", "About"), ("faq.html", "FAQ")]
CUR = ' aria-current="page"'

TICKER_ITEMS = ["Free shipping in the lower 48", "Box No. 01 ships January 1 from Savannah, GA",
                "Skip or pause any month", "Every item from an independent local shop", "Gift plans never auto-renew",
                "Love your first box or your money back"]
_dot = '<svg viewBox="0 0 50 64" aria-hidden="true"><path fill="currentColor" d="M25 63S5 41 5 24a20 20 0 0 1 40 0c0 17-20 39-20 39z"/></svg>'
_run = "".join(f"<span>{_dot}{t}</span>" for t in TICKER_ITEMS)
TICKER = f'''  <div class="ticker">
    <p class="visually-hidden">{". ".join(TICKER_ITEMS)}.</p>
    <div class="ticker-track" aria-hidden="true"><div>{_run}</div><div>{_run}</div></div>
    <button class="ticker-toggle" type="button" aria-pressed="false" aria-label="Pause the scrolling messages">
      <svg class="tt-pause" viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="3" width="3" height="10" rx="1"/><rect x="9.5" y="3" width="3" height="10" rx="1"/></svg>
      <svg class="tt-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.2v9.6a.6.6 0 0 0 .9.5l7.4-4.8a.6.6 0 0 0 0-1L5.9 2.7a.6.6 0 0 0-.9.5z"/></svg>
    </button>
  </div>'''

def header(active):
    items = "\n".join(f'          <li><a href="{h}"{CUR if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to main content</a>
{TICKER}
  <header class="site-header">
    <div class="container">
      <nav class="nav" aria-label="Main">
        <a class="logo" href="index.html"><img src="img/mark.svg" alt="" width="40" height="43">{wm()}</a>
        <ul class="nav-links" id="nav-links">
{items}
          <li class="drawer-promo"><a href="join.html"><small>Box No. 01 &middot; ships Jan 1</small><strong>Savannah, Georgia</strong><span class="link">Reserve a box</span></a></li>
        </ul>
        <div class="nav-end">
          <a class="nav-search" href="search.html" aria-label="Search Marlowby"{CUR if active == "search.html" else ""}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5 21 21"/></svg>
          </a>
          <a class="btn btn--primary btn--sm" href="join.html"{CUR if active == "join.html" else ""}>Join</a>
          <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path class="t1" d="M4 9h16"/><path class="t2" d="M4 15h16"/></svg>
          </button>
        </div>
      </nav>
    </div>
  </header>'''

FOOTER = f'''  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div>
          <p style="color:#fff;font-family:var(--display);font-weight:800;font-size:1.5rem;line-height:1.2;max-width:18ch">Explore your city, one box at a time.</p>
          <p>First box ships January 1, 2027.</p>
        </div>
        <div>
          <h3>Shop</h3>
          <ul>
            <li><a href="plans.html">Plans</a></li>
            <li><a href="plans.html#gifts">Gifts</a></li>
            <li><a href="join.html">Reserve a box</a></li>
          </ul>
        </div>
        <div>
          <h3>Learn</h3>
          <ul>
            <li><a href="how-it-works.html">How it works</a></li>
            <li><a href="cities.html">2027 route</a></li>
            <li><a href="about.html">About us</a></li>
          </ul>
        </div>
        <div>
          <h3>Help</h3>
          <ul>
            <li><a href="search.html">Search</a></li>
            <li><a href="accessibility.html">Accessibility</a></li>
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="faq.html#contact">Contact</a></li>
            <li><a href="about.html#makers">For makers</a></li>
            <li><a href="credits.html">Works cited</a></li>
          </ul>
        </div>
      </div>
      <span class="footer-wm" aria-hidden="true">{wm()}</span>
      <div class="footer-bottom">
        <span>&copy; 2026 Marlowby. A concept site made for a student web design competition.</span>
        <a href="credits.html">Works cited &amp; AI use</a>
      </div>
    </div>
  </footer>'''

# Fonts and libraries are served from this repo, not a CDN. NLC provides no
# internet on site, and a dropped CDN would take the 3D scenes, every product
# image and all motion with it.
FONTS = "vendor/fonts/fonts.css"
MOTION_JS = '''
  <script src="vendor/js/gsap.min.js"></script>
  <script src="vendor/js/ScrollTrigger.min.js"></script>
  <script src="vendor/js/lenis.min.js"></script>'''
THREE_JS = '''
  <script defer src="vendor/js/three.min.js"></script>
  <script defer src="vendor/js/RoundedBoxGeometry.js"></script>
  <script defer src="vendor/js/RoomEnvironment.js"></script>
  <script defer src="js/skylines.js?v={VER}"></script>
  <script defer src="js/scene.js?v={VER}"></script>'''


SITE = "https://gopsmonkey.github.io/marlowby/"

def _esc(t):
    return H.escape(t, quote=True)

def seo_tags(filename, title, desc, jsonld="", robots="index, follow"):
    """Canonical URL, social cards and structured data for one page."""
    url = SITE + ("" if filename == "index.html" else filename)
    img = SITE + "img/social-card.png"
    block = f"""
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Marlowby">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{_esc(title)}">
  <meta property="og:description" content="{_esc(desc)}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="The Marlowby logo on a blue sky, with the line: a new U.S. city in a box, every month.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{_esc(title)}">
  <meta name="twitter:description" content="{_esc(desc)}">
  <meta name="twitter:image" content="{img}">
  <meta name="robots" content="{robots}">"""
    return block + (jsonld or "")

def jsonld(obj):
    import json
    return '\n  <script type="application/ld+json">' + json.dumps(obj, separators=(",", ":")) + "</script>"

def crumbs(*pairs):
    """BreadcrumbList: pass (name, filename) in order, Home first."""
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
            "item": SITE + ("" if fn == "index.html" else fn)} for i, (n, fn) in enumerate(pairs)]})

def page(filename, title, desc, body, extra_css="", three=False, seo="", robots="index, follow"):
    doc = f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; worker-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#14234F">
  <link rel="icon" href="img/mark.svg" type="image/svg+xml">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="apple-touch-icon" href="img/apple-touch-icon.png">{seo_tags(filename, title, desc, seo, robots)}
  <link rel="preload" href="vendor/fonts/Nunito-latin-11.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="vendor/fonts/Figtree-latin-5.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="vendor/fonts/InstrumentSerifi-latin-7.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{FONTS}">
  <link rel="stylesheet" href="css/styles.css?v={VER}">{extra_css}
  <link rel="stylesheet" href="css/type.css?v={VER}">
</head>
<body>
{header(filename)}
  <main id="main">
{body}
  </main>
{FOOTER}{MOTION_JS}
  <script src="js/main.js?v={VER}"></script>{THREE_JS if (three and any(m in body for m in ('class="gl-zone"', 'class="open-zone"', 'data-shot='))) else ""}
</body>
</html>
'''
    (OUT / filename).write_text(doc.replace("{VER}", VER))

def page_head(title_lines, lead):
    return f'''    <section class="page-head">
      <div class="container grid12">
        <h1 data-lines>{lines(*title_lines)}</h1>
        <p class="lead" data-rise>{lead}</p>
      </div>
    </section>'''

import os as _os
# Product photos are rendered by our own three.js code. tools/render-shots.sh
# runs that code once in a headless browser and saves the results to img/shots/,
# so visitors get ordinary image files: faster, and they still appear on
# devices without WebGL. Set MARLOWBY_LIVE_SHOTS=1 to emit the live version
# (which is what the render script reads).
LIVE_SHOTS = _os.environ.get("MARLOWBY_LIVE_SHOTS") == "1"

def _baked(key):
    return not LIVE_SHOTS and (OUT / "img" / "shots" / f"{key}.webp").exists()

def shot(name, alt, cls=""):
    """A product photo of one of our boxes. Baked file if present, live render otherwise."""
    c = f' class="{cls}"' if cls else ""
    if _baked(name):
        return f'<img{c} src="img/shots/{name}.webp" alt="{alt}" width="960" height="800" loading="lazy" decoding="async">'
    return f'<img{c} data-shot="{name}" src="img/mark.svg" alt="{alt}" width="960" height="800">'

CTA = '''    <section class="section section--tight">
      <div class="container">
        <div class="tile tile--navy cta" data-rise>
          <h2 data-lines><span class="line"><span>Savannah ships</span></span><span class="line"><span>January 1.</span></span></h2>
          <div>
            <p class="lead">Reserve now and keep the launch price for as long as you stay. Nothing is charged until your first box ships.</p>
            <a class="btn btn--light" href="join.html">Reserve a box</a>
          </div>
        </div>
      </div>
    </section>'''

# ------------------------------------------------------------------ data
US_PATH = "12,39 42,28 470,28 476,21 556,46 631,73 651,82 666,136 721,131 755,125 783,100 837,100 873,57 894,62 907,104 857,125 849,143 860,158 837,167 800,179 784,210 775,219 767,244 775,275 738,300 718,312 691,334 684,363 705,429 699,456 677,442 663,408 649,372 622,375 581,363 556,366 560,388 544,384 491,375 473,384 439,410 436,444 403,415 374,374 349,388 326,377 294,338 268,338 225,347 166,325 130,325 108,298 76,287 56,251 46,230 26,194 20,156 16,136 23,78"

CITIES = [  # key, x, y, city, month, year, status, desc
  ("sav", 688, 332, "Savannah, Georgia", "Jan", "2027", "now", "Lowcountry pralines, a candle poured by a shop on Broughton Street, small-batch hot sauce and a walking map of the historic squares."),
  ("sf", 304, 267, "Santa Fe, New Mexico", "Feb", "2027", "soon", "Red and green chile blends, a hand-thrown mug from a local studio, piñon coffee and a pass to an online gallery walk on Canyon Road."),
  ("det", 659, 149, "Detroit, Michigan", "Mar", "2027", "soon", "A screen-printed tote, small-batch coffee, a soul-food spice rub and a playlist picked by neighborhood musicians."),
  ("pme", 856, 123, "Portland, Maine", "Apr", "2027", "soon", "Sea-salt caramels, wild blueberry jam, hand-dyed wool coasters and a lighthouse trail guide."),
  ("ash", 665, 269, "Asheville, North Carolina", "May", "2027", "soon", "Wildflower honey, a hand-forged bottle opener, herbal tea from a mountain farm and a trail map."),
  ("tuc", 226, 330, "Tucson, Arizona", "Jun", "2027", "soon", "Mesquite cookie mix, prickly-pear syrup, a beaded keychain by a local artist and a stargazing guide."),
  ("msp", 499, 100, "Minneapolis, Minnesota", "Jul", "2027", "soon", "Wild rice soup mix, a lake-life enamel pin, cardamom cookies and a Chain of Lakes bike map."),
  ("boi", 144, 125, "Boise, Idaho", "Aug", "2027", "soon", "Huckleberry chocolate, a river-float field guide, locally roasted coffee and a leather bookmark."),
  ("hdr", 55, 89, "Hood River, Oregon", "Oct", "2027", "soon", "Pear butter from a Columbia Gorge orchard, dried-apple chips, a hand-turned maple spoon and a fruit-loop trail map."),
  ("lou", 616, 222, "Louisville, Kentucky", "Nov", "2027", "soon", "Modjeska caramels from a candy maker on Frankfort Avenue, a Benedictine spread mix, a stoneware mug and a shotgun-house postcard set."),
  ("lan", 765, 190, "Lancaster, Pennsylvania", "Dec", "2027", "soon", "Hand-twisted pretzels from a Lititz bakery, apple butter, a quilt-block pot holder and a winter market map."),
]
VOTES = [("nola", 549, 371, "New Orleans, Louisiana", 412), ("kc", 479, 206, "Kansas City, Missouri", 318),
         ("btv", 811, 109, "Burlington, Vermont", 264), ("sat", 418, 381, "San Antonio, Texas", 351)]

def us_map():
    pins = []
    for k, x, y, city, mo, yr, status, desc in CITIES:
        color = "#F7B731" if status == "now" else "#3F6FD1"
        pins.append(f'''          <g class="pin{" active" if status == "now" else ""}" data-key="{k}" tabindex="0" role="button" aria-label="{city}, {mo} {yr} box" data-city="{city}" data-month="{mo}" data-year="{yr}" data-desc="{H.escape(desc)}" data-href="{city_url(city)}">
            <circle class="dot" cx="{x}" cy="{y}" r="10" fill="{color}" stroke="#14234F" stroke-width="3"/>
            <text x="{x}" y="{y - 20}" text-anchor="middle" font-family="Figtree, sans-serif" font-size="15" font-weight="600" fill="#14234F">{city.split(",")[0]}</text>
          </g>''')
    for k, x, y, city, _ in VOTES:
        pins.append(f'          <circle cx="{x}" cy="{y}" r="8" fill="#fff" stroke="#5B6585" stroke-width="2.5" stroke-dasharray="4 3" aria-hidden="true"/>')
    return f'''<svg class="us-map" viewBox="0 0 930 470" role="group" aria-label="Map of the United States with the 2027 box cities. Select a city to see what is in its box.">
          <polygon points="{US_PATH}" fill="#E4EDFB" stroke="#AFCBF3" stroke-width="3" stroke-linejoin="round"/>
{chr(10).join(pins)}
        </svg>'''

def mini_map():
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{16 if s == "now" else 12}" fill="{"#F7B731" if s == "now" else "#3F6FD1"}" stroke="#14234F" stroke-width="5"/>'
                   for _, x, y, _, _, _, s, _ in CITIES)
    return (f'<svg viewBox="0 0 930 470" aria-hidden="true"><polygon points="{US_PATH}" fill="#fff" stroke="#14234F" '
            f'stroke-width="7" stroke-linejoin="round"/>{dots}</svg>')

# Cloud layer for the sky: soft shapes roughened with SVG noise, so they read as clouds, not blobs
CLOUDS = '''<svg class="clouds" viewBox="0 0 1000 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true" data-parallax="-8">
          <defs>
            <filter id="cloud" x="-50%" y="-150%" width="200%" height="400%">
              <feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="5" seed="7" result="noise"/>
              <feDisplacementMap in="SourceGraphic" in2="noise" scale="90"/>
              <feGaussianBlur stdDeviation="7"/>
            </filter>
            <filter id="cloud-soft" x="-50%" y="-150%" width="200%" height="400%">
              <feTurbulence type="fractalNoise" baseFrequency=".008" numOctaves="4" seed="3" result="noise-soft"/>
              <feDisplacementMap in="SourceGraphic" in2="noise-soft" scale="120"/>
              <feGaussianBlur stdDeviation="14"/>
            </filter>
          </defs>
          <g filter="url(#cloud-soft)" fill="#fff" opacity=".55">
            <ellipse cx="160" cy="150" rx="190" ry="34"/>
            <ellipse cx="840" cy="110" rx="150" ry="26"/>
          </g>
          <g filter="url(#cloud)" fill="#fff">
            <ellipse cx="120" cy="540" rx="240" ry="70" opacity=".95"/>
            <ellipse cx="300" cy="590" rx="210" ry="60" opacity=".9"/>
            <ellipse cx="760" cy="470" rx="170" ry="46" opacity=".85"/>
            <ellipse cx="900" cy="560" rx="200" ry="66" opacity=".95"/>
            <ellipse cx="560" cy="660" rx="380" ry="70"/>
          </g>
        </svg>'''

# ================================================================== HOME
ROT = "".join(f'<span class="rot-word{" is-on" if i == 0 else ""}">{c[3].split(",")[0]}.</span>' for i, c in enumerate(CITIES))

def product(slug, name, tag, price, kicker, meta):
    return f'''          <a class="product" href="plans.html#{slug}">
            <div class="product-img">
              <span class="p-tag">{tag}</span><span class="p-price">${price}/mo</span>
              {shot(slug, f"The {name} box", "main")}{shot(slug + "-b", "", "alt")}
            </div>
            <p class="p-kicker">{kicker}</p>
            <h3 class="p-name">The {name}</h3>
            <p class="meta">{meta}</p>
          </a>'''


# ---------------------------------------------------------------- box items
# Each item in Box No. 01, drawn here as flat SVG in the logo's palette so the
# site still ships zero stock photography.
ITEM_SVG = {
 # class names hook the animations in home.css ("ani-*"); --k staggers repeats
 "praline": """<path d="M34 46h52l-5 44a8 8 0 0 1-8 7H47a8 8 0 0 1-8-7z" fill="#FCEAD6"/>
   <circle class="ani-drop" style="--k:2" cx="52" cy="66" r="7" fill="#F7B731"/><circle class="ani-drop" style="--k:0" cx="70" cy="78" r="7" fill="#F7B731"/>
   <circle class="ani-drop" style="--k:1" cx="68" cy="60" r="5" fill="#F7B731"/>
   <path class="ani-lid" d="M30 34h60v12H30z" fill="#F7B731"/>""",
 "candle": """<circle class="ani-glow" cx="60" cy="34" r="18" fill="#F7B731" stroke="none" opacity="0"/>
   <path d="M38 56h44v38a6 6 0 0 1-6 6H44a6 6 0 0 1-6-6z" fill="#AFCBF3"/>
   <path d="M38 56h44" /><path d="M60 56V40" />
   <path class="ani-flame" d="M60 22c7 7 10 12 10 17a10 10 0 0 1-20 0c0-5 3-10 10-17z" fill="#F7B731"/>""",
 "sauce": """<g class="ani-shake"><path d="M50 30h20v12l8 12v44a6 6 0 0 1-6 6H48a6 6 0 0 1-6-6V54l8-12z" fill="#FCEAD6"/>
   <path d="M52 20h16v10H52z" fill="#3F6FD1"/>
   <rect x="46" y="64" width="28" height="24" rx="3" fill="#F7B731"/></g>""",
 "grits": """<path d="M36 44h48v52a6 6 0 0 1-6 6H42a6 6 0 0 1-6-6z" fill="#FCEAD6"/>
   <path d="M36 44l6-16h36l6 16" fill="#E4EDFB"/>
   <path class="ani-write" style="--k:0" d="M48 62h24"/><path class="ani-write" style="--k:1" d="M48 74h24"/><path class="ani-write" style="--k:2" d="M48 86h16"/>""",
 "coaster": """<g class="ani-wind"><circle class="ani-ring" style="--k:2" cx="60" cy="64" r="34" fill="#FDE9BC"/>
   <circle class="ani-ring" style="--k:1" cx="60" cy="64" r="23" fill="none"/><circle class="ani-ring" style="--k:0" cx="60" cy="64" r="12" fill="#F7B731"/>
   <path d="M26 64h68M60 30v68" stroke-width="2.2" opacity=".55"/></g>""",
 "map": """<g class="ani-unfold"><path d="M24 38l24-10 24 10 24-10v56l-24 10-24-10-24 10z" fill="#E4EDFB"/>
   <path d="M48 28v56M72 38v56" /></g>
   <path class="ani-pin" d="M78 46c6 0 10 4 10 9 0 7-10 17-10 17S68 62 68 55c0-5 4-9 10-9z" fill="#F7B731"/>""",
}

BOX_ITEMS = [
 ("praline", "Benne praline jar", "Tybee Sugarworks", "Sweets"),
 ("candle", "Saltmarsh candle", "Broughton Candle Co.", "Home"),
 ("sauce", "Pepper sauce, small batch", "Ogeechee Pepper Co.", "Pantry"),
 ("grits", "Stone-ground grits", "Red Mill Stoneground", "Pantry"),
 ("coaster", "Sweetgrass coaster", "Harbor Light Weavers", "Craft"),
 ("map", "Walking map of the squares", "Drawn for Marlowby", "In every box"),
]

def box_item(i, key, name, maker, cat):
    return f'''          <li class="bx-item" style="--i:{i}">
            <div class="bx-art">
              <svg viewBox="0 0 120 120" role="img" aria-label="{H.escape(name)}">
                <g fill="none" stroke="#14234F" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">
                  {ITEM_SVG[key]}
                </g>
              </svg>
            </div>
            <p class="bx-cat">{cat}</p>
            <h3 class="bx-name">{name}</h3>
            <p class="bx-maker">{maker}</p>
          </li>'''

BOX_GRID = "\n".join(box_item(n, *it) for n, it in enumerate(BOX_ITEMS))

ABBR = {"Georgia": "GA", "New Mexico": "NM", "Michigan": "MI", "Maine": "ME", "North Carolina": "NC",
        "Arizona": "AZ", "Minnesota": "MN", "Idaho": "ID", "Oregon": "OR", "Kentucky": "KY",
        "Pennsylvania": "PA"}
STYLE = {  # route card: tile color, sticker color, sticker text color
  "sav": ("amber", "#F7B731", "#14234F"), "sf": ("sky", "#AFCBF3", "#14234F"), "det": ("cream", "#3F6FD1", "#ffffff"),
  "pme": ("sky", "#F7B731", "#14234F"), "ash": ("amber", "#14234F", "#ffffff"), "tuc": ("cream", "#F7B731", "#14234F"),
  "msp": ("sky", "#3F6FD1", "#ffffff"), "boi": ("cream", "#14234F", "#ffffff"),
  "hdr": ("amber", "#3F6FD1", "#ffffff"), "lou": ("sky", "#F7B731", "#14234F"), "lan": ("cream", "#AFCBF3", "#14234F")}

# A box's number is its month (Jan = 01), so September's members'-pick box
# keeps No. 09 even though it has no city yet.
_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
def box_no(c):
    return f"{_MONTHS.index(c[4]) + 1:02d}"

def city_url(city):
    """city-savannah.html for "Savannah, Georgia"."""
    return "city-" + city.split(", ")[0].lower().replace(" ", "-") + ".html"
def route_card(i, c):
    k, x, y, city, mo, yr, status, desc = c
    tone, acc, ink = STYLE[k]
    name, state = city.split(", ")
    key = f"city-{box_no(c)}"
    img = (f'<img src="img/shots/{key}.webp" alt="The {name} box" width="960" height="800" loading="lazy" decoding="async">'
           if _baked(key) else
           f'<img data-shot="city" data-city="{name}" data-state="{ABBR[state]}" data-num="{box_no(c)}" data-accent="{acc}" '
           f'data-ink="{ink}" src="img/mark.svg" alt="The {name} box" width="960" height="800" loading="lazy">')
    return f'''          <article class="route-card tile--{tone}">
            <span class="r-pill">{mo} {yr}</span>
            <button class="r-plus" type="button" aria-expanded="false" aria-controls="rc-{k}" aria-label="What is in the {name} box"><span aria-hidden="true"></span></button>
            {img}
            <h3><a class="r-link" href="{city_url(city)}">{name}</a></h3>
            <div class="r-more" id="rc-{k}"><p class="r-state">{state}</p><p>{desc}</p></div>
          </article>'''

import json as _json

def _meta(c):
    k, *_ = c
    tone, acc, ink = STYLE[k]
    name, state = c[3].split(", ")
    return {"city": name, "state": ABBR[state], "num": box_no(c), "accent": acc, "ink": ink}

def open_zone(c, title_html, lead, ask, hid="open-title"):
    """The box-opening scene for one city: skyline, caption and falling boxes."""
    i = CITIES.index(c)
    rain = [_meta(n) for n in (CITIES[i + 1:] + CITIES[:i])[:5]]
    m = _meta(c)
    attrs = (f' data-city="{c[0]}" data-num="{m["num"]}" data-name="{m["city"]}" data-state="{m["state"]}"'
             f' data-accent="{m["accent"]}" data-ink="{m["ink"]}" data-rain="{H.escape(_json.dumps(rain), quote=True)}"')
    return f'''    <section class="open-zone" aria-labelledby="{hid}"{attrs}>
      <div class="container">
        <div class="open-head">
          <h2 id="{hid}" data-lines>{title_html}</h2>
          <p class="lead" data-rise>{lead}</p>
        </div>
      </div>
      <div class="open-stage">
        <canvas class="open-canvas" aria-hidden="true"></canvas>
        <div class="open-caption">
          <p class="open-reveal">
            <span class="or-ask">{ask}<span class="or-dots" aria-hidden="true"><i></i><i></i><i></i></span></span>
            <span class="or-city">{c[3]}</span>
          </p>
        </div>
        <p class="open-fallback">A Marlowby box opening, with the skyline of {c[3].split(", ")[0]} rising out of it and the next months&rsquo; boxes tumbling off the rooftops.</p>
      </div>
    </section>'''


home = f'''    <div class="gl-zone">
      <canvas class="gl-canvas" aria-hidden="true"></canvas>

      <section class="hero" aria-labelledby="hero-title">
        <div class="container hero-grid">
          <div class="sky">
        {CLOUDS}
            <h1 class="sky-title" id="hero-title" data-lines><span class="visually-hidden">A new U.S. city at your door, every month.</span><span aria-hidden="true">{lines("A new city", "at your door:")}<span class="line"><span class="rotator">{ROT}</span></span></span></h1>
            <p class="sky-wm" aria-hidden="true" data-parallax="22">{wm()}</p>
            <div class="fly-anchor" aria-hidden="true"></div>
          </div>
          <aside class="promo" aria-label="First box">
            <span class="pill pill--amber">Ships Jan 1, 2027</span>
            <p class="promo-title">Box No. 01 is Savannah, Georgia.</p>
            <div class="promo-anchor" aria-hidden="true"></div>
            <a class="btn btn--light btn--block" href="join.html">Reserve a box</a>
            <a class="promo-gift link" href="join.html?gift=1">or send one as a gift</a>
          </aside>
        </div>
      </section>

      <section class="scene-sec" aria-labelledby="scene-title">
        <div class="container">
          <div class="scene">
            <canvas class="scene-canvas" aria-hidden="true"></canvas>
            <div class="scene-caption">
              <h2 id="scene-title" data-lines>{lines("One city <em>a month.</em>")}</h2>
              <p data-rise>Every box is filled by shops, bakers and makers from that month&rsquo;s city. Keep the boxes. They stack.</p>
            </div>
            <img class="scene-fallback" src="img/mark.svg" alt="">
          </div>
        </div>
      </section>
    </div>

{open_zone(CITIES[0], lines("Open it, and the", "<em>city comes out.</em>"), "Lift the flaps and Savannah is in there: the shops, the squares, the people who made everything inside. Next month another city takes its place.", "This month&rsquo;s city is")}

    <section class="section" aria-labelledby="pick-title">
      <div class="container">
        <div class="section-title">
          <h2 id="pick-title" data-lines>{lines("Pick your box.")}</h2>
          <p class="lead" style="margin-inline:auto" data-rise>Same city, three sizes. Free shipping on all of them.</p>
        </div>
        <div class="products" data-rise-group>
{product("postcard", "Postcard", "Good for gifts", 29, "Small &middot; 4&ndash;5 goods", "A taste of each city.")}
{product("neighborhood", "Neighborhood", "Most picked", 49, "Medium &middot; 7&ndash;9 goods", "Plus an at-home experience.")}
{product("grandtour", "Grand Tour", "For families", 79, "Large &middot; 10&ndash;12 goods", "Plus a live maker workshop.")}
        </div>
        <a class="btn-mega" href="plans.html" data-rise>Compare all three <span aria-hidden="true">&rarr;</span></a>
      </div>
    </section>

    <section class="section boxed" aria-labelledby="inside-title">
      <div class="container">
        <div class="inside-head">
          <div>
            <span class="pill pill--amber">Box No. 01 &middot; Savannah, Georgia</span>
            <h2 id="inside-title" data-lines>{lines("What&rsquo;s <em>inside.</em>")}</h2>
          </div>
          <p class="lead" data-rise>Six things from six Savannah businesses, plus the field guide and a map. Every maker is paid up front and named on a card in the box.</p>
        </div>
        <ul class="bx-grid" data-rise-group>
{BOX_GRID}
        </ul>
        <p class="bx-note note-small"><a class="link" href="city-savannah.html">Meet the Savannah makers and open the box</a>. Makers and products shown are illustrative for this concept site; see <a class="link" href="credits.html">works cited</a>.</p>
      </div>
    </section>

    <section class="section statement" aria-labelledby="stmt-title">
      <div class="container">
        <h2 id="stmt-title" class="stmt" data-rise>Local goods, the way they should be:
          <span class="nw"><span class="term-wrap"><button type="button" class="term" aria-describedby="tip1">made in town</button><span class="tip" role="tooltip" id="tip1">Every item is made or sold by an independent business in that month&rsquo;s city. No national brands.</span></span>,</span>
          <span class="nw"><span class="term-wrap"><button type="button" class="term" aria-describedby="tip2">paid up front</button><span class="tip" role="tooltip" id="tip2">We pay makers a fair wholesale price before the box ships, so a small shop never waits on us.</span></span>,</span>
          <span class="nw"><span class="term-wrap"><button type="button" class="term" aria-describedby="tip3">told by locals</button><span class="tip" role="tooltip" id="tip3">The field guide and maker cards are written with people who live there, not copied from travel sites.</span></span>.</span>
        </h2>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="how-title">
      <div class="container feature-grid">
        <div class="tile tile--sky big" data-rise>
          <h2 id="how-title" data-lines>{lines("How it works")}</h2>
          <ol class="steps-big">
            <li><div><strong>Pick a size</strong>Postcard, Neighborhood or Grand Tour. Pay monthly, or yearly for 15% off.</div></li>
            <li><div><strong>We go to the city</strong>Our team spends weeks with local shops and buys their goods at fair prices, paid up front.</div></li>
            <li><div><strong>Your box ships on the 1st</strong>The city is revealed on the 20th of the month before. Skip any month by the 15th.</div></li>
            <li><div><strong>Open it up</strong>Each box comes with a field guide, a fold-out map and the story behind every item.</div></li>
          </ol>
          <a class="btn btn--primary" href="how-it-works.html">More about the box</a>
        </div>
        <div class="stack" data-rise-group>
          <a class="tile tile--amber mini" href="plans.html#gifts">
            <div><h3>Give it as a gift</h3><p>3, 6 or 12 months, paid once. Gift plans never renew on their own.</p><span class="link">Gift plans</span></div>
            {shot("stack", "")}
          </a>
          <a class="tile tile--cream mini" href="cities.html">
            <div><h3>See the 2027 route</h3><p>Savannah first, then Santa Fe, Detroit and Portland, Maine.</p><span class="link">Box calendar</span></div>
            {mini_map()}
          </a>
        </div>
      </div>
    </section>

    <section class="section route" aria-labelledby="route-title" data-carousel>
      <div class="container route-head">
        <h2 id="route-title" data-lines>{lines("The 2027 route")}</h2>
        <div class="route-arrows">
          <button type="button" aria-label="Previous cities"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
          <button type="button" aria-label="More cities"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
        </div>
      </div>
      <div class="route-track" role="group" tabindex="0" aria-label="Box cities, January to August 2027">
{chr(10).join(route_card(i, c) for i, c in enumerate(CITIES))}
      </div>
      <div class="container route-foot">
        <div class="route-progress" aria-hidden="true"><span></span></div>
        <a class="link" href="cities.html">See the map</a>
      </div>
    </section>

    <section class="section" aria-labelledby="quotes-title">
      <div class="container">
        <div class="section-title">
          <h2 id="quotes-title" data-lines>{lines("From our test boxes")}</h2>
          <p class="lead" style="margin-inline:auto" data-rise>Forty families tried a sample Savannah box this fall. A few of the notes they sent back:</p>
        </div>
        <div class="quotes" data-rise-group>
          <figure><blockquote>&ldquo;My daughter now wants to visit Savannah because of a jar of pralines.&rdquo;</blockquote><figcaption>Dana, Columbus, OH</figcaption></figure>
          <figure><blockquote>&ldquo;I looked up every shop on the cards. Two of them already shipped me a second order.&rdquo;</blockquote><figcaption>Marcus, Fresno, CA</figcaption></figure>
          <figure><blockquote>&ldquo;The walking map is on our fridge. We&rsquo;re going in April.&rdquo;</blockquote><figcaption>Priya, Raleigh, NC</figcaption></figure>
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="news-title">
      <div class="container">
        <div class="tile tile--navy news" data-rise>
          <div>
            <h2 id="news-title" data-lines>{lines("Hear the next city <em>first.</em>")}</h2>
            <p class="lead">One email a month: the city reveal, a maker we met, and nothing else.</p>
          </div>
          <form class="newsletter inline-form" novalidate>
            <label class="visually-hidden" for="nl-email">Email address</label>
            <input id="nl-email" type="email" placeholder="you@example.com" required autocomplete="email">
            <button class="btn btn--light" type="submit">Sign up</button>
          </form>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </div>
      </div>
    </section>'''
page("index.html", "Marlowby | A new U.S. city in a box, every month",
     "Marlowby is a monthly subscription box of local goods, small businesses and experiences from a different U.S. city each month.",
     home, '\n  <link rel="stylesheet" href="css/home.css?v={VER}">', three=True,
     seo=jsonld({"@context": "https://schema.org", "@graph": [
       {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Marlowby",
        "inLanguage": "en-US",
        "description": "A monthly subscription box of local goods, small businesses and experiences from a different U.S. city each month.",
        "publisher": {"@id": SITE + "#org"},
        "potentialAction": {"@type": "SearchAction",
          "target": {"@type": "EntryPoint", "urlTemplate": SITE + "search.html?q={search_term_string}"},
          "query-input": "required name=search_term_string"}},
       {"@type": "Organization", "@id": SITE + "#org", "name": "Marlowby", "url": SITE,
        "logo": SITE + "img/mark.svg", "image": SITE + "img/social-card.png",
        "slogan": "Explore your city, one box at a time.",
        "description": "Marlowby ships a monthly box of local products from a different U.S. city, bought at fair prices from independent businesses."}]}))

# ================================================================== HOW IT WORKS
hiw = f'''{page_head(("A city, packed", "into a box."), "Here is what happens between a city and your front door, and what you will find when you open the lid.")}

    <section class="section section--tight" aria-labelledby="steps-title">
      <h2 id="steps-title" class="visually-hidden">Four steps</h2>
      <div class="container cards cards--4" data-rise-group>
        <div class="tile tile--sky"><span class="num">1</span><h3>Pick a size</h3><p>Postcard, Neighborhood or Grand Tour. Pay monthly, or yearly and save 15%.</p></div>
        <div class="tile tile--cream"><span class="num">2</span><h3>We go to the city</h3><p>We spend weeks meeting shop owners and buy their goods at fair prices, paid up front.</p></div>
        <div class="tile tile--amber"><span class="num">3</span><h3>It ships on the 1st</h3><p>Free shipping in the lower 48. Arrives in 3 to 6 business days, with tracking.</p></div>
        <div class="tile tile--navy"><span class="num">4</span><h3>Open it up</h3><p>Taste it, use it, read the stories, then plan a trip if you fall for the place.</p></div>
      </div>
    </section>

    <section class="section" aria-labelledby="inside-title">
      <div class="container split">
        <div>
          <h2 id="inside-title" data-lines>{lines("What&rsquo;s inside")}</h2>
          <p class="lead" data-rise>The goods change every month. These five things are in every box.</p>
          <div class="frame" data-rise style="background:#fff;margin-top:28px">{shot("neighborhood", "A Marlowby box from Savannah")}</div>
        </div>
        <ul class="rule-list" data-rise-group>
          <li><h3>Local goods</h3><p class="muted">4 to 12 items made or sold by independent businesses in that city: food, home goods, art.</p></li>
          <li><h3>The field guide</h3><p class="muted">A small booklet on the city&rsquo;s history, neighborhoods and food, written with locals.</p></li>
          <li><h3>A fold-out map</h3><p class="muted">Every shop in the box is marked, plus the places locals say not to miss.</p></li>
          <li><h3>Maker cards</h3><p class="muted">One card per item: who made it, how, and where to reorder.</p></li>
          <li><h3>An experience</h3><p class="muted">In Neighborhood and Grand Tour: a recipe, playlist, craft or live workshop from the city.</p></li>
        </ul>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="dates-title">
      <div class="container">
        <div class="section-title">
          <h2 id="dates-title" data-lines>{lines("Three dates to know")}</h2>
        </div>
        <div class="cards cards--3" data-rise-group>
          <div class="tile"><span class="num">15th</span><h3>Skip or change</h3><p class="muted">Skip a month, pause, switch plans or cancel by the 15th to change the next box.</p></div>
          <div class="tile"><span class="num">20th</span><h3>City reveal</h3><p class="muted">We email next month&rsquo;s city and a first look at the makers.</p></div>
          <div class="tile"><span class="num">1st</span><h3>Box ships</h3><p class="muted">Your box leaves our warehouse and a tracking link lands in your inbox.</p></div>
        </div>
      </div>
    </section>

{CTA}'''
page("how-it-works.html", "How It Works | Marlowby",
     "How Marlowby works: choose a plan, we curate goods from local makers, and your box ships on the 1st of every month.", hiw, three=True,
     seo=crumbs(("Home", "index.html"), ("How it works", "how-it-works.html")))

# ================================================================== PLANS
def plan_card(name, price, desc, items, tone, shot_name, goods, featured=False):
    lis = "".join(f"<li>{i}</li>" for i in items)
    flag = '<span class="plan-flag">Most picked</span>' if featured else ""
    btn = "btn--light" if tone == "navy" else "btn--primary"
    slug = name.replace(" ", "%20")
    return f'''          <article class="tile tile--{tone} plan" id="{shot_name}" data-monthly="{price}">
            {flag}
            <div class="plan-img">{shot(shot_name, "")}</div>
            <h2>The {name}</h2>
            <p class="plan-desc">{desc}</p>
            <div class="plan-stats">
              <div class="plan-stat"><span class="ps-num">{goods}</span><span class="ps-lab">local goods</span></div>
              <div class="plan-stat"><span class="ps-num"><span class="amount">${price}</span></span><span class="ps-lab">per month</span></div>
            </div>
            <p class="price-note" aria-live="polite"></p>
            <ul class="rule-list">{lis}</ul>
            <div class="plan-cta">
              <a class="btn {btn} btn--block" href="join.html?plan={slug}">Choose {name}</a>
              <a class="btn btn--outline btn--block" href="join.html?plan={slug}&amp;gift=1">Gift it</a>
            </div>
          </article>'''

YES = '<td class="yes">Yes</td>'
NO = '<td class="no"><span aria-hidden="true">&ndash;</span><span class="visually-hidden">No</span></td>'
plans = f'''{page_head(("Three sizes.", "Same city."), "Every plan has free shipping in the lower 48, the field guide and map, and can be skipped, paused or canceled any month.")}

    <section class="section section--tight center" aria-label="Plans">
      <div class="container">
        <div class="billing-toggle" role="group" aria-label="Billing">
          <button type="button" data-billing="monthly" aria-pressed="true">Monthly</button>
          <button type="button" data-billing="annual" aria-pressed="false">Yearly <span class="save">save 15%</span></button>
        </div>
        <div class="plans" data-rise-group>
{plan_card("Postcard", 29, "A small taste of each city. Good for trying us out, or as a gift.", ["Field guide and fold-out map", "Maker cards", "Free shipping"], "cream", "postcard", "4&ndash;5")}
{plan_card("Neighborhood", 49, "Our main box, with room for food, a craft and something to do.", ["Everything in Postcard", "An at-home experience", "Swaps for allergies and diets"], "navy", "neighborhood", "7&ndash;9", True)}
{plan_card("Grand Tour", 79, "The whole city, for big households and people who want it all.", ["Everything in Neighborhood", "Live online maker workshop", "One limited-edition item"], "sky", "grandtour", "10&ndash;12")}
        </div>
        <p class="note-small" style="margin-top:28px">Reserve before January 1, 2027 and you keep these prices for as long as you stay subscribed. Every plan can ship every month or every other month, and if you don&rsquo;t love your first box we refund it.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="compare-title">
      <div class="container">
        <div class="section-title"><h2 id="compare-title" data-lines>{lines("Side by side")}</h2></div>
        <div class="table-wrap" data-rise>
          <table class="compare">
            <caption class="visually-hidden">What each Marlowby plan includes</caption>
            <thead><tr><th scope="col">Included</th><th scope="col">Postcard</th><th scope="col">Neighborhood</th><th scope="col">Grand Tour</th></tr></thead>
            <tbody>
              <tr><th scope="row">Local goods per box</th><td>4&ndash;5</td><td>7&ndash;9</td><td>10&ndash;12</td></tr>
              <tr><th scope="row">Field guide and map</th>{YES}{YES}{YES}</tr>
              <tr><th scope="row">Free shipping (lower 48)</th>{YES}{YES}{YES}</tr>
              <tr><th scope="row">Skip or pause any month</th>{YES}{YES}{YES}</tr>
              <tr><th scope="row">At-home experience</th>{NO}{YES}{YES}</tr>
              <tr><th scope="row">Allergy and diet swaps</th>{NO}{YES}{YES}</tr>
              <tr><th scope="row">Live maker workshop</th>{NO}{NO}{YES}</tr>
              <tr><th scope="row">Limited-edition item</th>{NO}{NO}{YES}</tr>
              <tr><th scope="row">Discount on reorders from makers</th><td>5%</td><td>10%</td><td>15%</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="quiz-title">
      <div class="container">
        <div class="tile tile--cream split">
          <div>
            <h2 id="quiz-title" data-lines>{lines("Not sure which?")}</h2>
            <p class="lead">Two questions and we&rsquo;ll suggest one.</p>
          </div>
          <form id="plan-quiz">
            <fieldset class="field">
              <legend>Who is it for?</legend>
              <div class="pill-choices">
                <label><input type="radio" name="who" value="me"><span>Just me</span></label>
                <label><input type="radio" name="who" value="two"><span>Two of us</span></label>
                <label><input type="radio" name="who" value="family"><span>A family</span></label>
              </div>
            </fieldset>
            <fieldset class="field">
              <legend>How much do you want?</legend>
              <div class="pill-choices">
                <label><input type="radio" name="how" value="taste"><span>A little taste</span></label>
                <label><input type="radio" name="how" value="explore"><span>A good mix</span></label>
                <label><input type="radio" name="how" value="deep"><span>All of it</span></label>
              </div>
            </fieldset>
            <p id="quiz-result" class="quiz-out" role="status" aria-live="polite">Pick one answer in each row.</p>
          </form>
        </div>
      </div>
    </section>

    <section class="section" id="gifts" aria-labelledby="gift-title">
      <div class="container split">
        <div>
          <h2 id="gift-title" data-lines>{lines("Gift a few months.")}</h2>
          <p class="lead" data-rise>Pay once. The first box arrives gift-wrapped with your note inside, and gift plans never renew on their own.</p>
          <a class="btn btn--primary" href="join.html?gift=1" data-rise>Send a gift</a>
        </div>
        <div>
        <ul class="rule-list gift-list" data-rise-group>
          <li><span><strong>3 months</strong><small>A season of cities</small></span><b>from $87</b></li>
          <li><span><strong>6 months</strong><small>Half a year</small></span><b>from $162</b></li>
          <li><span><strong>12 months</strong><small>All 12 cities, plus a map poster</small></span><b>from $296</b></li>
        </ul>
        <p class="note-small gift-team">Sending boxes to a whole team or client list? <a class="link" href="faq.html#contact">Ask about group pricing</a>.</p>
        </div>
      </div>
    </section>

{CTA}'''
PLAN_LD = jsonld({"@context": "https://schema.org", "@type": "ItemList",
  "name": "Marlowby subscription plans",
  "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
      "@type": "Product", "name": f"The {n}", "description": d,
      "brand": {"@type": "Brand", "name": "Marlowby"},
      "image": SITE + "img/social-card.png",
      "offers": {"@type": "Offer", "price": f"{p}.00", "priceCurrency": "USD",
                 "availability": "https://schema.org/PreOrder",
                 "url": SITE + "join.html", "category": "Subscription"}}}
    for i, (n, p, d) in enumerate([
      ("Postcard", 29, "A small taste of each city. Four to five local goods, the field guide and map."),
      ("Neighborhood", 49, "Seven to nine local goods, the field guide and map, plus an at-home experience."),
      ("Grand Tour", 79, "Ten to twelve local goods, everything in Neighborhood, plus a live maker workshop.")])]})

page("plans.html", "Plans & Pricing | Marlowby",
     "Compare the Marlowby Postcard, Neighborhood and Grand Tour boxes, with monthly, yearly and gift options.", plans, three=True,
     seo=PLAN_LD + crumbs(("Home", "index.html"), ("Plans", "plans.html")))

# ================================================================== CITIES

def city_items(desc):
    d = desc.rstrip(".")
    head, _, last = d.rpartition(" and ")
    parts = head.split(", ") + [last]
    return [p[0].upper() + p[1:] for p in parts]

def chips(desc, cls="chips"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in city_items(desc)) + "</ul>"

def city_shot(i, c, extra=""):
    k, x, y, city, mo, yr, status, desc = c
    tone, acc, ink = STYLE[k]
    name, state = city.split(", ")
    key = f"city-{box_no(c)}"
    if _baked(key):
        lazy = "" if "loading=" in extra else ' loading="lazy"'
        return f'<img src="img/shots/{key}.webp" alt="The {name} box" width="960" height="800"{lazy} decoding="async"{extra}>'
    return (f'<img data-shot="city" data-city="{name}" data-state="{ABBR[state]}" data-num="{box_no(c)}" data-accent="{acc}" '
            f'data-ink="{ink}" src="img/mark.svg" alt="The {name} box" width="960" height="800"{extra}>')

def route_arcs():
    out = []
    for (k1, x1, y1, *_), (k2, x2, y2, *_) in zip(CITIES, CITIES[1:]):
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        cx, cy = (x1 + x2) / 2, min(y1, y2) - dist * 0.22
        out.append(f'<path d="M{x1} {y1} Q{cx:.0f} {cy:.0f} {x2} {y2}"/>')
    return f'<g class="arcs" fill="none" stroke="#14234F" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" opacity=".55">{"".join(out)}</g>'

def big_map():
    svg = us_map()
    svg = svg.replace('stroke-linejoin="round"/>\n', 'stroke-linejoin="round"/>\n          ' + route_arcs() + "\n", 1)
    for k, *_ in CITIES:
        pass
    return svg

sav = CITIES[0]
detail_imgs = "".join(city_shot(i, c, f' data-key="{c[0]}"' + ("" if i == 0 else " hidden")) for i, c in enumerate(CITIES))

cal_rows = "\n".join(f'''          <li class="cal-row{" is-now" if c[6] == "now" else ""}">
            <div class="cal-when"><span class="cal-mo">{c[4]}</span><span class="cal-yr">{c[5]}</span></div>
            <div class="cal-city"><h3><a href="{city_url(c[3])}">{c[3].split(", ")[0]}</a></h3><p>{c[3].split(", ")[1]} &middot; Box No. {box_no(c)}{" &middot; <b>First box</b>" if c[6] == "now" else ""}</p></div>
            {chips(c[7])}
            <div class="cal-img">{city_shot(i, c, ' loading="lazy"')}</div>
          </li>''' for i, c in enumerate(CITIES))
_vote_row = '''          <li class="cal-row cal-row--vote">
            <div class="cal-when"><span class="cal-mo">Sep</span><span class="cal-yr">2027</span></div>
            <div class="cal-city"><h3>Your pick</h3><p>Members&rsquo; vote &middot; Box No. 09</p></div>
            <ul class="chips"><li>New Orleans</li><li>Kansas City</li><li>Burlington</li><li>San Antonio</li></ul>
            <div class="cal-img"><a class="cal-vote" href="#vote-title" aria-label="Vote for September&rsquo;s city"><span aria-hidden="true">?</span></a></div>
          </li>'''
_rows = cal_rows.split("\n          <li ")
# insert before October's row so the calendar reads straight through the year
_oct = next(i for i, r in enumerate(_rows) if '<span class="cal-mo">Oct</span>' in r)
cal_rows = "\n          <li ".join(_rows[:_oct]) + "\n" + _vote_row + "\n          <li " + "\n          <li ".join(_rows[_oct:])

votes = "\n".join(f'''          <div class="vote-item" data-city="{city}" data-votes="{n}">
            <span><strong>{city}</strong> <span class="pct"></span></span>
            <button type="button" aria-pressed="false">Vote</button>
            <div class="vote-bar" aria-hidden="true"><span></span></div>
          </div>''' for _, _, _, city, n in VOTES)

cities = f'''    <section class="c-hero">
      <div class="container c-hero-grid">
        <div class="c-hero-copy">
          <h1 data-lines>{lines("Twelve cities.", "Twelve boxes.", "One <em>a month.</em>")}</h1>
          <p class="lead" data-rise>This is where Marlowby goes in 2027. Each box is filled by shops from one city and ships on the 1st.</p>
          <div class="c-actions" data-rise><a class="btn btn--primary" href="join.html">Reserve a box</a><a class="link" href="#calendar">See every month</a></div>
        </div>
        <article class="tile tile--navy c-now" data-rise aria-labelledby="now-title">
          <div class="c-now-top"><span class="pill pill--amber">Box No. 01 &middot; January</span><span class="c-count">Ships in <strong id="countdown" data-launch="2027-01-01T00:00:00">soon</strong></span></div>
          <div class="c-now-img">{city_shot(0, sav)}<span class="burst" aria-hidden="true">First<br>box!</span></div>
          <h2 id="now-title">Savannah, Georgia</h2>
          {chips(sav[7], "chips chips--dark")}
        </article>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="map-title">
      <div class="container map-layout">
        <div class="map-card" data-rise>
          <div class="map-top"><h2 id="map-title">Follow the route</h2><p class="muted">Select a pin to see that box.</p></div>
          {big_map()}
          <div class="map-legend"><span class="l-now">First box</span><span class="l-soon">Coming in 2027</span><span class="l-vote">Up for a vote</span></div>
        </div>
        <aside class="map-detail" id="map-detail" aria-live="polite" data-rise>
          <div class="md-img">{detail_imgs}</div>
          <div class="month"><strong class="m-mo">{sav[4]}</strong> <small class="m-yr">{sav[5]}</small></div>
          <h3>{sav[3]}</h3>
          <p>{sav[7]}</p>
          <a class="link md-more" href="{city_url(sav[3])}">Open the {sav[3].split(", ")[0]} box</a>
          <a class="btn btn--light btn--sm" href="join.html">Reserve a box</a>
        </aside>
      </div>
    </section>

    <section class="section" id="calendar" aria-labelledby="cal-title">
      <div class="container">
        <div class="cal-head">
          <h2 id="cal-title" data-lines>{lines("Month by month")}</h2>
          <p class="lead" data-rise>Item lists are early previews. They may change as we sign on makers.</p>
        </div>
        <ol class="cal" data-rise-group>
{cal_rows}
        </ol>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="vote-title">
      <div class="container">
        <div class="tile tile--navy vote-tile">
          <div>
            <span class="pill pill--amber">Members vote</span>
            <h2 id="vote-title" data-lines>{lines("You pick", "<em>September.</em>")}</h2>
            <p class="lead">Members choose one city each year. Voting closes June 30 and we announce the winner in the July email.</p>
            <p class="note-small">Your city isn&rsquo;t here? <a class="link" href="faq.html#contact">Nominate it</a>.</p>
          </div>
          <div class="vote-list">
{votes}
          </div>
          <p class="visually-hidden" id="vote-status" role="status" aria-live="polite"></p>
        </div>
      </div>
    </section>

{CTA}'''
page("cities.html", "2027 Route & Box Calendar | Marlowby",
     "See Marlowby's 2027 city route on an interactive map, preview each month's box and vote for September's city.", cities,
     f'\n  <link rel="stylesheet" href="css/pages.css?v={VER}">', three=True,
     seo=crumbs(("Home", "index.html"), ("Cities", "cities.html")))

# ================================================================== ABOUT
SPLIT = [("Makers", 22, "#F7B731", "Paid to the shops in the box, before it ships"),
         ("Shipping", 8, "#3F6FD1", "Free to you, anywhere in the lower 48"),
         ("Team &amp; scouting", 9, "#14234F", "Weeks on the ground in every city"),
         ("Box, guide &amp; map", 6, "#AFCBF3", "Printed by a shop in that city when we can"),
         ("Kept to grow", 4, "#E7DFD2", "New cities, better boxes")]
bar = "".join(f'<span style="flex:{v};background:{c}" title="{n}: ${v}"></span>' for n, v, c, _ in SPLIT)
legend = "".join(f'<li><i style="background:{c}"></i><div><strong>${v}</strong> {n}<small>{d}</small></div></li>' for n, v, c, d in SPLIT)

JOURNEY = [("Summer 2025", "The trunk", "A road trip through 11 states. We came home with a trunk full of things we couldn&rsquo;t buy anywhere else."),
           ("Spring 2026", "Forty test boxes", "We packed Savannah boxes by hand and mailed them to friends of friends in 19 states."),
           ("Fall 2026", "First makers", "Twelve Savannah shops said yes. Every one was paid before a single box was sold."),
           ("Jan 1, 2027", "Box No. 01 ships", "The first city goes out to founding members. Santa Fe follows in February.")]
journey = "".join(f'<li><span class="j-pin" aria-hidden="true">{PIN}</span><p class="j-when">{w}</p><h3>{t}</h3><p>{d}</p></li>' for w, t, d in JOURNEY)

about = f'''    <section class="a-hero">
      <div class="container a-hero-grid">
        <div>
          <h1 data-lines>{lines("It started with", "a <em>full trunk.</em>")}</h1>
          <p class="lead" data-rise>On a long road trip we kept buying things from small shops: pralines, a mug, a jar of chile. Back home, friends kept asking where to get them. Marlowby is our answer.</p>
        </div>
        <figure class="tile tile--amber a-hero-art" data-rise>
          <span class="burst burst--blue" aria-hidden="true">8 cities<br>in 2027</span>
          {shot("stack", "Three Marlowby boxes stacked")}
          <figcaption>Every box is from one city, and every item in it is from a shop in that city.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section" aria-labelledby="journey-title">
      <div class="container">
        <h2 id="journey-title" data-lines>{lines("How we got here")}</h2>
        <ol class="journey" data-rise-group>{journey}</ol>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="split-title">
      <div class="container">
        <div class="tile split-tile">
          <div class="split-head">
            <h2 id="split-title" data-lines>{lines("Where your $49 goes")}</h2>
            <p class="lead" data-rise>Our planned split for one Neighborhood box. The biggest share goes to the makers.</p>
          </div>
          <div class="money-bar" role="img" aria-label="Of $49: $22 to makers, $8 shipping, $9 team and scouting, $6 box, guide and map, $4 kept to grow.">{bar}</div>
          <ul class="money-legend" data-rise-group>{legend}</ul>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="values">
      <div class="container promise">
        <div class="promise-head">
          <h2 id="values" data-lines>{lines("Four promises")}</h2>
          <p class="lead" data-rise>To the people who make the goods, and to the people who open the box.</p>
        </div>
        <ol class="promise-list" data-rise-group>
          <li><h3>Truly local</h3><p>Every item is made or sold by an independent business in that month&rsquo;s city. No national brands, ever.</p></li>
          <li><h3>Paid before we ship</h3><p>Makers get a fair wholesale price up front, with no exclusive contracts. They keep selling however they like.</p></li>
          <li><h3>The story comes too</h3><p>Every item has a card with who made it and how, written with the maker, plus a link to reorder from them directly.</p></li>
          <li><h3>Light on packaging</h3><p>Recyclable boxes, paper fill, no plastic tape and carbon-offset shipping.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section--tight" id="makers" aria-labelledby="makers-title">
      <div class="container">
        <div class="tile tile--blue maker-tile" data-rise>
          <div>
            <h2 id="makers-title" data-lines>{lines("Run a shop?", "Let&rsquo;s talk.")}</h2>
            <p class="lead">We are choosing partners for 2027 and 2028.</p>
            <a class="btn btn--light" href="faq.html#contact">Become a partner</a>
          </div>
          <ol class="maker-list">
            <li><strong>You&rsquo;re independent</strong>Locally owned, in the city we&rsquo;re featuring.</li>
            <li><strong>You make it, or pick it carefully</strong>Your own goods, or a shop known for what it stocks.</li>
            <li><strong>You can make a batch</strong>Roughly 500 to 3,000 units, with our help planning.</li>
          </ol>
        </div>
      </div>
    </section>'''
page("about.html", "About | Marlowby",
     "How Marlowby started, where your money goes, and what we promise makers and members.", about,
     f'\n  <link rel="stylesheet" href="css/pages.css?v={VER}">', three=True,
     seo=crumbs(("Home", "index.html"), ("About", "about.html")))

# ================================================================== FAQ
FAQS = [
  ("boxes", "What is Marlowby?", "A monthly subscription box. Each month features a different U.S. city, with goods from its independent businesses, a field guide, a fold-out map and, on larger plans, an at-home experience."),
  ("boxes", "Do I get to choose the city?", "Everyone gets the same city each month, so the whole community explores together. Members vote on one city a year, and you can skip any month."),
  ("boxes", "What if I have allergies or a special diet?", "On Neighborhood and Grand Tour you can set a taste profile (vegan, vegetarian, gluten-free, nut-free, dairy-free or no caffeine). We swap food items for something suitable from the same city."),
  ("boxes", "Will I ever get the same item twice?", "No. Every month is a new city with new makers."),
  ("shipping", "When will my box arrive?", "Boxes ship on the 1st and arrive in 3 to 6 business days. We email a tracking link when yours leaves the warehouse."),
  ("shipping", "Where do you ship?", "Free to every address in the lower 48 states. Alaska and Hawaii are a flat $9. International shipping is not available yet."),
  ("shipping", "What if something arrives broken?", "Send us a photo within 14 days and we will replace or refund that item."),
  ("account", "How do I skip a month or pause?", "Choose Skip or Pause in your account before the 15th. You can pause for up to three months at a time, and it never costs anything."),
  ("account", "What if I don't love my first box?", "Tell us within 30 days of it arriving and we refund the whole box. You do not need to send anything back."),
  ("account", "Can I get a box every other month?", "Yes. Choose every other month when you reserve, or switch any time before the 15th. You get six cities a year instead of twelve, and the price per box is the same."),
  ("account", "Can I cancel anytime?", "Yes. Cancel a monthly plan before the 15th to stop the next box. Yearly plans are refunded for any boxes that have not shipped."),
  ("account", "Can I change my plan?", "Yes. Upgrade or downgrade before the 15th and the change starts with your next box."),
  ("gifts", "How do gift subscriptions work?", "Choose 3, 6 or 12 months and pay once. The first box arrives gift-wrapped with your note. Gift plans never renew on their own."),
  ("gifts", "Can a gift start on a certain date?", "Yes. Pick a start month at checkout and we will email the person a digital gift card on the day you choose."),
]
faq_html = "\n".join(f'''          <details data-cat="{c}">
            <summary>{q}</summary>
            <div class="answer"><p>{a}</p></div>
          </details>''' for c, q, a in FAQS)

faq = f'''{page_head(("Questions,", "answered."), "Boxes, shipping, your account and gifts. If your question isn&rsquo;t here, write to us below.")}

    <section class="section section--tight" aria-labelledby="faq-title">
      <div class="container" style="max-width:880px">
        <h2 id="faq-title" class="visually-hidden">Frequently asked questions</h2>
        <div class="faq-tools">
          <label class="visually-hidden" for="faq-search">Search questions</label>
          <input class="faq-search" id="faq-search" type="search" placeholder="Search, e.g. skip, allergies, shipping">
          <div class="faq-filters" role="group" aria-label="Filter by topic">
            <button type="button" data-cat="all" aria-pressed="true">All</button>
            <button type="button" data-cat="boxes" aria-pressed="false">Boxes</button>
            <button type="button" data-cat="shipping" aria-pressed="false">Shipping</button>
            <button type="button" data-cat="account" aria-pressed="false">Account</button>
            <button type="button" data-cat="gifts" aria-pressed="false">Gifts</button>
          </div>
        </div>
        <div class="faq">
{faq_html}
        </div>
        <p class="faq-empty">Nothing matches that. Try another word, or write to us below.</p>
        <p class="visually-hidden" id="faq-count" role="status" aria-live="polite"></p>
      </div>
    </section>

    <section class="section" id="contact" aria-labelledby="contact-title">
      <div class="container">
        <div class="tile tile--sky split">
          <div>
            <h2 id="contact-title" data-lines>{lines("Write to us.")}</h2>
            <p class="lead">Questions, city ideas or maker partnerships. We answer within one business day.</p>
            <p><strong>hello@marlowby.example</strong><br>Monday to Friday, 9 a.m. to 6 p.m. Eastern</p>
          </div>
          <form id="contact-form" novalidate>
            <div class="field" data-required><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name" aria-describedby="e-c-name"><p class="error" id="e-c-name">Please enter your name.</p></div>
            <div class="field" data-required><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email" aria-describedby="e-c-email"><p class="error" id="e-c-email">Please enter a valid email.</p></div>
            <div class="field"><label for="c-topic">Topic</label>
              <select id="c-topic" name="topic"><option>A question</option><option>Nominate a city</option><option>Become a maker partner</option><option>Help with an order</option></select></div>
            <div class="field" data-required><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="5" required aria-describedby="e-c-msg"></textarea><p class="error" id="e-c-msg">Please write a message.</p></div>
            <button class="btn btn--primary btn--block" type="submit">Send</button>
            <p class="form-msg" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>'''
FAQ_LD = jsonld({"@context": "https://schema.org", "@type": "FAQPage",
  "mainEntity": [{"@type": "Question", "name": q,
                  "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in FAQS]})

page("faq.html", "FAQ & Contact | Marlowby",
     "Answers about Marlowby boxes, shipping, skipping, canceling and gift subscriptions, plus how to contact us.", faq,
     seo=FAQ_LD + crumbs(("Home", "index.html"), ("FAQ", "faq.html")))

# ================================================================== JOIN
STATES = "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
state_opts = "".join(f"<option>{s}</option>" for s in STATES)
interests = ["Sweets", "Savory snacks", "Coffee & tea", "Home goods", "Art & prints", "Music", "History", "Outdoors"]
interest_html = "".join(f'<label><input type="checkbox" name="interests" value="{i}"><span>{i.replace("&", "&amp;")}</span></label>' for i in interests)

join = f'''{page_head(("Reserve your", "first box."), "Takes about two minutes. Nothing is charged until launch, and we email you before your first box ships.")}

    <section class="section section--tight">
      <div class="container">
        <div class="tile form-card" id="join-wrap">
          <ol class="form-progress" aria-label="Steps">
            <li class="current" aria-current="step">1. Plan</li><li>2. Address</li><li>3. Review</li>
          </ol>
          <form id="join-form" novalidate>
            <div class="form-step active">
              <h2>Choose a plan</h2>
              <fieldset class="field" data-required aria-describedby="e-plan">
                <legend>Box size</legend>
                <div class="choice-grid">
                  <label class="choice"><input type="radio" name="plan" value="Postcard"><span class="choice-body"><strong>Postcard</strong><small>4&ndash;5 goods &middot; $29/mo</small></span></label>
                  <label class="choice"><input type="radio" name="plan" value="Neighborhood" checked><span class="choice-body"><strong>Neighborhood</strong><small>7&ndash;9 goods &middot; $49/mo</small></span></label>
                  <label class="choice"><input type="radio" name="plan" value="Grand Tour"><span class="choice-body"><strong>Grand Tour</strong><small>10&ndash;12 goods &middot; $79/mo</small></span></label>
                </div>
                <p class="error" id="e-plan">Please choose a plan.</p>
              </fieldset>
              <fieldset class="field" id="f-freq">
                <legend>How often</legend>
                <div class="pill-choices">
                  <label><input type="radio" name="freq" value="monthly" checked><span>Every month</span></label>
                  <label><input type="radio" name="freq" value="bimonthly"><span>Every other month</span></label>
                </div>
              </fieldset>
              <fieldset class="field" id="f-billing">
                <legend>Billing</legend>
                <div class="pill-choices">
                  <label><input type="radio" name="billing" value="monthly" checked><span>Monthly</span></label>
                  <label><input type="radio" name="billing" value="annual"><span>Yearly, save 15%</span></label>
                </div>
              </fieldset>
              <fieldset class="field">
                <legend>What do you like? <span class="note-small">(optional)</span></legend>
                <div class="pill-choices">{interest_html}</div>
              </fieldset>
              <div class="field" style="display:flex;gap:10px;align-items:center">
                <input type="checkbox" id="gift" name="gift" value="yes" style="width:auto">
                <label for="gift" style="margin:0;font-weight:500">This is a gift</label>
              </div>
              <fieldset class="field" id="f-giftlen" hidden>
                <legend>Gift length</legend>
                <div class="pill-choices">
                  <label><input type="radio" name="giftlen" value="3" checked><span>3 months</span></label>
                  <label><input type="radio" name="giftlen" value="6"><span>6 months</span></label>
                  <label><input type="radio" name="giftlen" value="12"><span>12 months</span></label>
                </div>
                <p class="note-small" style="margin:8px 0 0">Paid once. A gift ends after its last box and never renews.</p>
              </fieldset>
              <div class="form-nav"><span></span><button type="button" class="btn btn--primary" data-next>Continue</button></div>
            </div>

            <div class="form-step">
              <h2>Where should it go?</h2>
              <div class="field" data-required><label for="j-name">Full name</label><input id="j-name" name="name" required autocomplete="name" aria-describedby="e-name"><p class="error" id="e-name">Please enter your name.</p></div>
              <div class="field" data-required><label for="j-email">Email</label><input id="j-email" name="email" type="email" required autocomplete="email" aria-describedby="e-email"><p class="error" id="e-email">Please enter a valid email.</p></div>
              <div class="field" data-required><label for="j-street">Street address</label><input id="j-street" name="street" required autocomplete="address-line1" aria-describedby="e-street"><p class="error" id="e-street">Please enter a street address.</p></div>
              <div class="field-row">
                <div class="field" data-required><label for="j-city">City</label><input id="j-city" name="city" required autocomplete="address-level2" aria-describedby="e-city"><p class="error" id="e-city">Please enter a city.</p></div>
                <div class="field-row">
                  <div class="field" data-required><label for="j-state">State</label><select id="j-state" name="state" required aria-describedby="e-state"><option value="">Pick</option>{state_opts}</select><p class="error" id="e-state">Pick a state.</p></div>
                  <div class="field" data-required><label for="j-zip">ZIP</label><input id="j-zip" name="zip" required pattern="[0-9]{{5}}" inputmode="numeric" maxlength="5" autocomplete="postal-code" aria-describedby="e-zip"><p class="error" id="e-zip">5-digit ZIP.</p></div>
                </div>
              </div>
              <div class="form-nav"><button type="button" class="btn btn--outline" data-prev>Back</button><button type="button" class="btn btn--primary" data-next>Review</button></div>
            </div>

            <div class="form-step">
              <h2>Check and reserve</h2>
              <div class="summary-box" id="summary"></div>
              <div class="field" data-required style="margin-top:20px;display:flex;gap:10px;align-items:flex-start;flex-wrap:wrap">
                <input type="checkbox" id="terms" name="terms" required aria-describedby="e-terms" style="width:auto;margin-top:5px">
                <label for="terms" id="terms-label" style="font-weight:500;flex:1">I understand my plan renews until I cancel, and nothing is charged until my first box ships.</label>
                <p class="error" id="e-terms" style="flex-basis:100%">Please tick this box to continue.</p>
              </div>
              <div class="form-nav"><button type="button" class="btn btn--outline" data-prev>Back</button><button type="submit" class="btn btn--primary">Reserve my box</button></div>
            </div>
          </form>
        </div>

        <div class="tile form-card success" id="join-success" hidden>
          <img src="img/mark.svg" alt="" width="120" height="130">
          <h2 tabindex="-1">You&rsquo;re in, <span class="success-name"></span>!</h2>
          <p class="lead" style="margin-inline:auto">Your spot is saved. Look for the Savannah reveal in your inbox on December 20.</p>
          <a class="btn btn--primary" href="cities.html">See the 2027 route</a>
        </div>
      </div>
    </section>'''
page("join.html", "Reserve a Box | Marlowby",
     "Reserve your Marlowby subscription box in three short steps.", join,
     seo=crumbs(("Home", "index.html"), ("Reserve a box", "join.html")))

import json as _json
# ---------------------------------------------------------------- city pages
# Facts are real and checkable; makers are illustrative (see Works Cited).
CITY_INFO = {
 "sav": dict(
   blurb="Georgia&rsquo;s oldest city was laid out in 1733 around a grid of public squares, and most of them still stand, shaded by live oaks hung with Spanish moss. Box No. 01 is a walk through them.",
   facts=["Founded in 1733, Savannah is Georgia&rsquo;s oldest city.",
          "Twenty-two of the squares in James Oglethorpe&rsquo;s original town plan survive today.",
          "Benne, the West African name for sesame, has flavoured Lowcountry baking for centuries."],
   makers=[("Tybee Sugarworks", "Benne praline jar", "Tybee Island"), ("Broughton Candle Co.", "Saltmarsh candle", "Broughton Street"),
           ("Ogeechee Pepper Co.", "Small-batch pepper sauce", "Starland District")]),
 "sf": dict(
   blurb="Santa Fe was founded in 1610, which makes it the oldest state capital in the country, and at about 7,000 feet it is the highest too. Every fall the city smells of green chile roasting in steel drums.",
   facts=["Founded in 1610, Santa Fe is the oldest state capital in the United States.",
          "At about 7,000 feet, it is also the highest state capital.",
          "New Mexico&rsquo;s official state question is &ldquo;Red or green?&rdquo; It is asking which chile you want."],
   makers=[("Alto Mesa Chile Mill", "Red and green chile blends", "Southside"), ("Two Ravens Clayworks", "Hand-thrown mug", "Canyon Road"),
           ("Piñon Hollow Roasters", "Piñon coffee", "Railyard District")]),
 "det": dict(
   blurb="Detroit built the cars, then the sound: Motown started in a house on West Grand Boulevard. Box No. 03 comes from the printers, roasters and cooks bringing its neighborhoods back.",
   facts=["The Renaissance Center&rsquo;s central tower is the tallest building in Michigan.",
          "The Guardian Building, finished in 1929, is known as the &ldquo;Cathedral of Finance&rdquo; for its tiled interior.",
          "Berry Gordy founded Motown Records in Detroit in 1959."],
   makers=[("Corktown Inkworks", "Screen-printed tote", "Corktown"), ("Second Shift Roasting", "Small-batch coffee", "Midtown"),
           ("Grand River Spice Kitchen", "Soul-food spice rub", "Grandmont Rosedale")]),
 "pme": dict(
   blurb="Portland is a working harbor first: fishing boats, ferries to the islands and brick warehouses rebuilt after the fire of 1866. The coast road south leads to the oldest lighthouse in Maine.",
   facts=["Portland Head Light was first lit in 1791 and is the oldest lighthouse in Maine.",
          "Most of the Old Port&rsquo;s brick buildings went up after the Great Fire of 1866.",
          "Maine grows nearly all of the wild blueberries harvested in the United States."],
   makers=[("Casco Bay Confections", "Sea-salt caramels", "Old Port"), ("Back Cove Preserves", "Wild blueberry jam", "Back Cove"),
           ("Munjoy Hill Fiber Co.", "Hand-dyed wool coasters", "Munjoy Hill")]),
 "ash": dict(
   blurb="Asheville sits where the Blue Ridge meets the Smokies, a mountain town of potters, blacksmiths and herb farmers. Box No. 05 brings the honey and the tea from the hollows above it.",
   facts=["The Blue Ridge Parkway, 469 miles long, passes along the edge of the city.",
          "The Jackson Building, finished in 1924, was the first skyscraper in western North Carolina.",
          "The Basilica of St. Lawrence was built with Guastavino tile and has a large freestanding elliptical dome."],
   makers=[("French Broad Apiary", "Wildflower honey", "River Arts District"), ("Lexington Lane Forge", "Hand-forged bottle opener", "Downtown"),
           ("High Gap Herb Farm", "Mountain herbal tea", "Madison County")]),
 "tuc": dict(
   blurb="Tucson has been farmed for more than 4,000 years, and its food still comes from the desert: mesquite flour, prickly pear and tepary beans. The skies are dark enough that the city limits its lights for the observatories.",
   facts=["In 2015 Tucson became the first city in the United States named a UNESCO City of Gastronomy.",
          "Mission San Xavier del Bac was finished in 1797; its east tower never received a dome.",
          "The saguaro cactus grows wild only in the Sonoran Desert, which surrounds the city."],
   makers=[("Mesquite &amp; Mano", "Mesquite cookie mix", "Barrio Viejo"), ("Bajada Syrup Co.", "Prickly-pear syrup", "Fourth Avenue"),
           ("Sonoran Bead Studio", "Beaded keychain", "Mercado District")]),
 "msp": dict(
   blurb="Minneapolis is a city of lakes and long winters, with Scandinavian bakeries, a riverfront of old flour mills and trails that circle the water. July is when everyone is outside.",
   facts=["The IDS Center has been the tallest building in Minnesota since it opened in the 1970s.",
          "The Foshay Tower, finished in 1929, was designed as a tribute to the Washington Monument.",
          "The Chain of Lakes is linked by paved trails for walking and biking."],
   makers=[("Northwoods Pantry Co.", "Wild rice soup mix", "Northeast"), ("Loring Pin Works", "Lake-life enamel pin", "Loring Park"),
           ("Cedar Avenue Bakehouse", "Cardamom cookies", "Cedar-Riverside")]),
 "boi": dict(
   blurb="Boise is a river town under sagebrush foothills, with a greenbelt path along the water and a Basque quarter downtown. In August half the city floats the Boise River on inner tubes.",
   facts=["The Idaho State Capitol is the only state capitol in the country heated with geothermal water.",
          "The Boise River Greenbelt is a tree-lined path of more than 25 miles.",
          "Floating the river through downtown is a summer tradition."],
   makers=[("Owyhee Chocolate Works", "Huckleberry chocolate", "Hyde Park"), ("Table Rock Roasters", "Locally roasted coffee", "Downtown"),
           ("Basque Block Leather", "Leather bookmark", "Basque Block")]),
 "hdr": dict(
   blurb="Hood River sits in the Columbia River Gorge with Mount Hood to the south and orchards in between. October is harvest: pears, apples and farm stands open along the Fruit Loop.",
   facts=["Mount Hood, Oregon&rsquo;s highest peak at 11,249 feet, rises south of town.",
          "The Hood River County Fruit Loop is a 35-mile drive past orchards and farm stands.",
          "Steady winds through the Gorge have made the town a center for windsurfing and kiteboarding."],
   makers=[("Gorge Light Orchard", "Pear butter", "Upper Valley"), ("Odell Valley Drying Co.", "Dried-apple chips", "Odell"),
           ("Oak Street Woodshop", "Hand-turned maple spoon", "Downtown")]),
 "lou": dict(
   blurb="Louisville is a river city of shotgun houses, front porches and its own sweets. November is the quiet season between Derbies, and the best time to eat your way down Frankfort Avenue.",
   facts=["The Kentucky Derby has been run at Churchill Downs every year since 1875.",
          "A 120-foot steel bat leans against the Louisville Slugger Museum &amp; Factory downtown.",
          "Benedictine spread was created by Louisville caterer Jennie Benedict around 1900."],
   makers=[("Crescent Hill Candy Co.", "Modjeska caramels", "Frankfort Avenue"), ("Highlands Pantry", "Benedictine spread mix", "The Highlands"),
           ("Butchertown Pottery", "Stoneware mug", "Butchertown")]),
 "lan": dict(
   blurb="Lancaster County is farm country: red barns, covered bridges and a downtown market that has sold local food since colonial times. December brings the winter markets and fresh pretzels.",
   facts=["Lancaster Central Market dates to the 1730s and is one of the oldest farmers markets in the country.",
          "The Julius Sturgis bakery in nearby Lititz, opened in 1861, was the first commercial pretzel bakery in America.",
          "Lancaster County is home to one of the largest Amish communities in the United States."],
   makers=[("Lititz Twist Bakery", "Hand-twisted pretzels", "Lititz"), ("Conestoga Kitchen", "Apple butter", "Strasburg"),
           ("Paradise Lane Quilters", "Quilt-block pot holder", "Paradise")]),
}
_MONTH_NAME = dict(zip(_MONTHS, "January February March April May June July August September October November December".split()))

CITY_PAGES = []
for _i, _c in enumerate(CITIES):
    _k, _x, _y, _city, _mo, _yr, _status, _desc = _c
    _name, _state = _city.split(", ")
    _info = CITY_INFO[_k]
    _url = city_url(_city)
    _prev, _next = CITIES[_i - 1], CITIES[(_i + 1) % len(CITIES)]
    _items = "".join(f"<li>{it}</li>" for it in city_items(_desc))
    _makers = "\n".join(f'''          <li class="maker"><span class="mk-pin" aria-hidden="true">{PIN}</span><div><h3>{mn}</h3><p>{what} &middot; <span class="muted">{where}</span></p></div></li>'''
                        for mn, what, where in _info["makers"])
    _facts = "\n".join(f"          <li>{f}</li>" for f in _info["facts"])
    _body = f'''    <section class="c-hero city-hero">
      <div class="container c-hero-grid">
        <div class="c-hero-copy">
          <span class="pill pill--amber">Box No. {box_no(_c)} &middot; {_MONTH_NAME[_mo]} {_yr}</span>
          <h1 data-lines>{lines(_name + ",", "<em>" + _state + ".</em>")}</h1>
          <p class="lead" data-rise>{_info["blurb"]}</p>
          <div class="c-actions" data-rise><a class="btn btn--primary" href="join.html">Reserve a box</a><a class="link" href="cities.html#calendar">See all twelve</a></div>
        </div>
        <div class="tile tile--navy c-now city-box">
          <div class="c-now-img">{city_shot(_i, _c, ' loading="eager" fetchpriority="high"')}</div>
          <p class="c-count">Ships {_MONTH_NAME[_mo]} 1, {_yr}</p>
        </div>
      </div>
    </section>

{open_zone(_c, lines("Open the box.", "<em>" + _name + " comes out.</em>"), f"Scroll to lift the flaps. Every Marlowby box is a city you can open: this one is {_name}, Box No. {box_no(_c)}.", f"Box No. {box_no(_c)} is")}

    <section class="section" aria-labelledby="inbox-title">
      <div class="container split">
        <div>
          <h2 id="inbox-title" data-lines>{lines("In the box")}</h2>
          <p class="lead" data-rise>Every item comes from an independent business in {_name}, bought at a fair price before the box ships. Previews may change as we sign on makers.</p>
        </div>
        <ul class="chips chips--big" data-rise-group>{_items}</ul>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="makers-title">
      <div class="container">
        <div class="tile tile--sky">
          <h2 id="makers-title" class="wc-note-h">The makers</h2>
          <ul class="makers">
{_makers}
          </ul>
          <p class="note-small" style="margin:18px 0 0">Makers shown are illustrative for this concept site. See <a class="link" href="credits.html">works cited</a>.</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="why-title">
      <div class="container split">
        <h2 id="why-title" data-lines>{lines("Why " + _name)}</h2>
        <ul class="rule-list city-facts" data-rise-group>
{_facts}
        </ul>
      </div>
    </section>

    <nav class="section section--tight city-nav" aria-label="Other boxes on the route">
      <div class="container city-nav-row">
        <a class="city-step" href="{city_url(_prev[3])}"><small>&larr; Box No. {box_no(_prev)} &middot; {_prev[4]}</small><strong>{_prev[3].split(", ")[0]}</strong></a>
        <a class="city-step city-step--next" href="{city_url(_next[3])}"><small>Box No. {box_no(_next)} &middot; {_next[4]} &rarr;</small><strong>{_next[3].split(", ")[0]}</strong></a>
      </div>
    </nav>

{CTA}'''
    _ld = jsonld({"@context": "https://schema.org", "@type": "Product",
                  "name": f"Marlowby Box No. {box_no(_c)}: {_city}",
                  "description": _desc, "brand": {"@type": "Brand", "name": "Marlowby"},
                  "image": SITE + f"img/shots/city-{box_no(_c)}.webp",
                  "offers": {"@type": "Offer", "price": "49.00", "priceCurrency": "USD",
                             "availability": "https://schema.org/PreOrder", "url": SITE + "join.html"}})
    page(_url, f"{_name}, {_state} | Box No. {box_no(_c)} | Marlowby",
         f"Marlowby Box No. {box_no(_c)}, {_MONTH_NAME[_mo]} {_yr}: what is in the {_name} box, the local makers behind it, and why {_name}.",
         _body, '\n  <link rel="stylesheet" href="css/pages.css?v={VER}">\n  <link rel="stylesheet" href="css/home.css?v={VER}">', three=True,
         seo=_ld + crumbs(("Home", "index.html"), ("Cities", "cities.html"), (_name, _url)))
    CITY_PAGES.append((_url, _name))


# ================================================================== SEARCH
search_body = f'''{page_head(("Search", "Marlowby."), "Find a plan, a city, a maker or an answer. Results come from every page on this site.")}

    <section class="section section--tight">
      <div class="container" style="max-width:860px">
        <form class="search-form" role="search" action="search.html" method="get">
          <label for="q" class="visually-hidden">Search Marlowby</label>
          <input id="q" name="q" type="search" class="faq-search" autocomplete="off" autofocus
                 placeholder="Try Savannah, gift, allergies or shipping">
          <button class="btn btn--primary" type="submit">Search</button>
        </form>
        <h2 class="visually-hidden">Results</h2>
        <p class="search-count" id="search-count" role="status" aria-live="polite"></p>
        <ol class="search-results" id="search-results"></ol>
        <div class="search-empty" id="search-empty" hidden>
          <h2>Nothing matched that.</h2>
          <p class="muted">Try a shorter word, or start from one of these:</p>
          <ul class="rule-list">
            <li><a class="link" href="plans.html">Compare the three box sizes</a></li>
            <li><a class="link" href="cities.html">See the 2027 city route</a></li>
            <li><a class="link" href="faq.html">Read the FAQ</a></li>
          </ul>
        </div>
      </div>
    </section>'''
page("search.html", "Search | Marlowby",
     "Search every page of the Marlowby site: plans, cities, makers, shipping and gift answers.", search_body,
     seo=crumbs(("Home", "index.html"), ("Search", "search.html")))

# ================================================================== WORKS CITED
# MLA 9, as the BPA Style & Reference Manual requires: alphabetical by first
# significant word, hanging indent, double spaced, "---" for a repeated author.
# AI prompts follow the BPA AI Usage & Citation Policy (2026-27, Level 2):
#   "Prompt description" prompt. Tool, Version, Developer, Date, URL.
TEAM_NAME = "Marlowby Web Design Team"   # team: replace with your team's name
TEAM = []   # team: fill in to show a roles table, e.g. [("Page layout", "Jane Doe"), ...]
CC = "<em>Claude Code</em>, {v} version, Anthropic, {d}, claude.com/claude-code."
WORKS = [
  # generative AI, in the BPA policy's format
  "“Improve the Marlowby site’s UI, accessibility and functionality to better match the competition prompt” prompt. " + CC.format(v="Claude Opus 5", d="7 Nov. 2026"),
  "“Compare the site with the WSAP rubric, fix validation errors, and add site search, SEO and self-hosted fonts and libraries” prompt. " + CC.format(v="Claude Opus 5", d="14 Nov. 2026"),
  "“Make the box open and show the month’s city skyline popping out, with boxes falling from the skyline” prompt. " + CC.format(v="Claude Opus 5", d="15 Nov. 2026"),
  "“Find sites similar to Marlowby, take their best ideas and fix their worst habits where Marlowby has them” prompt. " + CC.format(v="Claude Opus 5.5", d="25 Nov. 2026"),
  "“Rate the site against the official rubric, fix what is lacking and find ways to exceed it” prompt. " + CC.format(v="Claude Opus 5.5", d="25 Nov. 2026"),
  "“Execute everything needed to take the site above and beyond the rubric” prompt. " + CC.format(v="Claude Opus 5.5", d="26 Nov. 2026"),
  # design and market research
  "<em>Atlas Coffee Club</em>, atlascoffeeclub.com. Accessed 25 Nov. 2026.",
  "<em>Bella Kitchenware</em>, bellakitchenware.com. Accessed 7 Nov. 2026.",
  "<em>Bokksu</em>, www.bokksu.com. Accessed 25 Nov. 2026.",
  "<em>Explore Local Box</em>, www.explorelocalbox.com. Accessed 25 Nov. 2026.",
  "<em>Graza</em>, www.graza.co. Accessed 7 Nov. 2026.",
  "“Know the Good and Bad of Subscription Boxes Before Signing Up.” <em>The Penny Hoarder</em>, www.thepennyhoarder.com/save-money/good-and-bad-of-subscription-boxes/. Accessed 25 Nov. 2026.",
  "<em>Mobbin</em>, mobbin.com. Screenshots of the Hims, Graza, Oura and Seed websites. Accessed 7 Nov. 2026.",
  "<em>Olipop</em>, drinkolipop.com. Accessed 7 Nov. 2026.",
  "<em>Omsom</em>, omsom.com. Accessed 7 Nov. 2026.",
  "“10 Costly Secrets Subscription Box Companies Hide.” <em>Billshark</em>, www.billshark.com/blogs/10-dirty-secrets-subscription-boxes-dont-want-you-to-know. Accessed 25 Nov. 2026.",
  "<em>Universal Yums</em>, www.universalyums.com. Accessed 14 Nov. 2026.",
  # typefaces and code libraries
  "Adams, Vernon, et al. <em>Nunito</em>. SIL Open Font License, Google Fonts, fonts.google.com/specimen/Nunito. Accessed 7 Nov. 2026.",
  "Colophon Foundry. <em>DM Mono</em>. SIL Open Font License, Google Fonts, fonts.google.com/specimen/DM+Mono. Accessed 7 Nov. 2026.",
  "Fuenzalida, Rodrigo, and Jordan Egstad. <em>Instrument Serif</em>. SIL Open Font License, Google Fonts, fonts.google.com/specimen/Instrument+Serif. Accessed 7 Nov. 2026.",
  "GreenSock. <em>GSAP and ScrollTrigger</em>. Version 3.12.5, GreenSock Standard License, gsap.com. Accessed 7 Nov. 2026.",
  "Kennedy, Erik. <em>Figtree</em>. SIL Open Font License, Google Fonts, fonts.google.com/specimen/Figtree. Accessed 7 Nov. 2026.",
  "darkroom.engineering. <em>Lenis</em>. Version 1.1.13, MIT License, github.com/darkroomengineering/lenis. Accessed 7 Nov. 2026.",
  "three.js authors. <em>three.js</em>. Release r128, MIT License, threejs.org. Accessed 7 Nov. 2026.",
]
# Self-created work: one author, so every entry after the first uses "---".
SELF = [
  "“Box-Opening Scene with the Savannah Skyline.” Self-created 3D animation, coded with three.js, with AI assistance as cited. 15 Nov. 2026.",
  "“City Skylines of the 2027 Route.” Self-created 3D models of eleven city skylines from their public landmarks, coded with three.js, with AI assistance as cited. 26 Nov. 2026.",
  "“Box Photographs, Shelf Room and Falling-Box Hero.” Self-created 3D graphics, coded with three.js and rendered to WebP files at build time, with AI assistance as cited. 2026.",
  "“Map of the 2027 Route.” Self-created SVG map plotted from public latitude and longitude points. 2026.",
  "<em>Marlowby</em>. Self-created website: page layout, written content, navigation and code, with AI assistance as cited. 2026, gopsmonkey.github.io/marlowby.",
  "“Marlowby Logo.” Self-created digital design, redrawn as SVG. 2026.",
  "“Social Sharing Card.” Self-created digital image. 25 Nov. 2026.",
  "“What’s Inside Illustrations.” Self-created SVG illustrations, with AI assistance as cited. 15 Nov. 2026.",
]

import re as _wre
def _sort_key(entry):
    t = _wre.sub(r"<[^>]+>", "", entry).lstrip("“\"'")
    t = _wre.sub(r"^(the|a|an) ", "", t, flags=_wre.I)
    t = _wre.sub(r"^10\b", "ten", t)          # numbers sort as if spelled out
    return t.lower()

_self_sorted = sorted(SELF, key=_sort_key)
_self_html = [f"{TEAM_NAME}. {_self_sorted[0]}"] + [f"---. {e}" for e in _self_sorted[1:]]
_all = sorted([(TEAM_NAME.lower() + f" {i:02d}", e) for i, e in enumerate(_self_html)]
              + [(_sort_key(e), e) for e in WORKS])
works_html = "\n".join(f"          <li>{e}</li>" for _, e in _all)
roles_html = ("" if not TEAM else
  '\n\n    <section class="section section--tight" aria-labelledby="roles-title">\n      <div class="container" style="max-width:880px">\n'
  '        <h2 id="roles-title">Team roles</h2>\n        <dl class="roles">'
  + "".join(f"<dt>{r}</dt><dd>{n}</dd>" for r, n in TEAM) + "</dl>\n      </div>\n    </section>")

credits = f'''{page_head(("Works", "cited."), "Every source, tool and AI assistant used to make this site, cited in MLA format as the BPA Style &amp; Reference Manual and AI Usage &amp; Citation Policy require.")}

    <section class="section section--tight" aria-labelledby="note-title">
      <div class="container" style="max-width:880px">
        <div class="tile tile--sky">
          <h2 id="note-title" class="wc-note-h">About this site</h2>
          <p>Marlowby is a fictional company, and this website was made for the Business Professionals of America (BPA) 365 Website Design and Development Team event, 2026&ndash;2027. The makers, products, test-box quotes and vote counts are illustrative, not real people or businesses. No stock photography or third-party images are used: every picture, map, illustration and 3D scene is drawn by code written for this project. The websites listed were studied for layout and market research only; no text, images, code or branding from them was copied.</p>
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="wc-title">
      <div class="container" style="max-width:880px">
        <h2 id="wc-title">Works Cited</h2>
        <ol class="works-cited">
{works_html}
        </ol>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="ai-title">
      <div class="container" style="max-width:880px">
        <div class="tile tile--cream">
          <h2 id="ai-title" class="wc-note-h">Generative AI use</h2>
          <p>This event is AI Policy Level 2: generative AI may support the entry, and every use is disclosed and cited. Claude, made by Anthropic, was used through Claude Code to audit the site against the rubric and the Style &amp; Reference Manual; to write and edit HTML, CSS, JavaScript and the Python build script; to code the 3D box-opening scene and the What&rsquo;s Inside illustrations; to research comparable subscription-box websites; and to draft and edit copy. Each AI-assisted change is recorded with its date in the site&rsquo;s public Git history. The same uses are listed on the team&rsquo;s AI Usage &amp; Documentation Form.</p>
        </div>
      </div>
    </section>{roles_html}'''
page("credits.html", "Works Cited | Marlowby",
     "Works cited in MLA format for the Marlowby website: research sources, typefaces, code libraries, self-created graphics and generative AI use.", credits,
     seo=crumbs(("Home", "index.html"), ("Works cited", "credits.html")))

# ================================================================== ACCESSIBILITY
A11Y = [
  ("Readable for low vision", "Text meets WCAG 2.2 AA contrast. Every colour pair was measured, including text over the hero sky, where a scrim keeps the headline readable as clouds drift behind it. Pages reflow at 400% zoom without sideways scrolling."),
  ("Usable without a mouse", "Every link, button, map pin and form control works from the keyboard, with a visible focus ring. A skip link jumps past the menu. Buttons and links are at least 44 by 44 pixels for touch."),
  ("Clear to screen readers", "Headings follow in order on every page. Images have text alternatives, and the 3D scenes, which are decorative, are hidden from screen readers with a written description in their place. Search results, FAQ filters, votes and form errors are announced as they change."),
  ("Calm motion", "If your device asks for reduced motion, the scroll effects, the rotating city name and the box animations stay still. The scrolling announcement bar has a pause button."),
  ("Forms that explain themselves", "Every field has a visible label. Errors appear next to the field and are linked to it, and checkout states every charge and renewal before you agree to it."),
  ("Works on more devices", "Box photos are ordinary image files, so they appear without WebGL. The site is tested in Chrome and in Safari&rsquo;s WebKit engine, and keeps working offline after your first visit."),
]
a11y_items = "\n".join(f'''          <li><h3>{t}</h3><p>{d}</p></li>''' for t, d in A11Y)
a11y = f'''{page_head(("Built for", "everyone."), "Marlowby aims to meet WCAG 2.2 Level AA, the standard behind the ADA guidance for websites. Here is what that means on this site and how we checked it.")}

    <section class="section section--tight" aria-labelledby="a11y-title">
      <h2 id="a11y-title" class="visually-hidden">What we did</h2>
      <div class="container" style="max-width:880px">
        <ul class="rule-list credits">
{a11y_items}
        </ul>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="test-title">
      <div class="container" style="max-width:880px">
        <div class="tile tile--sky">
          <h2 id="test-title" class="wc-note-h">How we checked</h2>
          <p>Every page passes the W3C HTML validator with no errors and scores 100 for accessibility in Google Lighthouse. We tested keyboard use by hand, measured contrast for each colour pair, and checked the site in Chrome and Safari&rsquo;s WebKit engine, with motion on and off.</p>
          <p>Automated tools catch only part of the picture. The site has not yet been reviewed by a person who uses a screen reader every day. If anything gets in your way, <a class="link" href="faq.html#contact">tell us</a> and we will fix it.</p>
        </div>
      </div>
    </section>'''
page("accessibility.html", "Accessibility | Marlowby",
     "How the Marlowby website meets WCAG 2.2 AA: contrast, keyboard use, screen readers, reduced motion, forms and testing.", a11y,
     seo=crumbs(("Home", "index.html"), ("Accessibility", "accessibility.html")))

# ================================================================== 404
notfound = f'''{page_head(("That page took", "a wrong turn."), "We could not find that page. It may have moved, or the link may have a typo.")}

    <section class="section section--tight">
      <div class="container">
        <div class="tile tile--sky split">
          <div>
            <h2>Try one of these</h2>
            <p class="muted">Everything on the site is a click away from here.</p>
          </div>
          <ul class="rule-list">
            <li><a class="link" href="index.html">Home</a> &mdash; the first box and the three sizes</li>
            <li><a class="link" href="how-it-works.html">How it works</a> &mdash; city to doorstep, step by step</li>
            <li><a class="link" href="plans.html">Plans</a> &mdash; compare Postcard, Neighborhood and Grand Tour</li>
            <li><a class="link" href="cities.html">Cities</a> &mdash; the 2027 route and box calendar</li>
            <li><a class="link" href="faq.html">FAQ</a> &mdash; skipping, allergies, shipping and gifts</li>
          </ul>
        </div>
        <a class="btn-mega" href="index.html">Back to the home page <span aria-hidden="true">&rarr;</span></a>
      </div>
    </section>'''
page("404.html", "Page not found | Marlowby",
     "That page could not be found. Here are the main pages of the Marlowby site.", notfound,
     robots="noindex, follow")

# A small search index built from the pages just written, so it can never
# drift from the copy. Shipped as JSON and queried in the browser.
import json as _json, re as _re
_INDEX_PAGES = ["index.html", "how-it-works.html", "plans.html", "cities.html",
                "about.html", "faq.html", "join.html", "credits.html", "accessibility.html"]
_LABEL = {"index.html": "Home", "how-it-works.html": "How it works", "plans.html": "Plans",
          "cities.html": "Cities", "about.html": "About", "faq.html": "FAQ",
          "join.html": "Reserve a box", "credits.html": "Works cited", "accessibility.html": "Accessibility"}
_INDEX_PAGES += [u for u, _ in CITY_PAGES]
_LABEL.update({u: n for u, n in CITY_PAGES})
_records = []
for _fn in _INDEX_PAGES:
    _html = (OUT / _fn).read_text()
    _main = _re.search(r"<main id=\"main\">(.*?)</main>", _html, _re.S)
    _body = _main.group(1) if _main else _html
    _body = _re.sub(r"<(script|style|svg)\b.*?</\1>", " ", _body, flags=_re.S | _re.I)
    # split on headings so a hit can point at the right part of the page
    _parts = _re.split(r"<h([23])\b[^>]*>(.*?)</h\1>", _body)
    _lead, _rest = _parts[0], _parts[1:]
    def _clean(t):
        t = _re.sub(r"<[^>]+>", " ", t)
        return " ".join(H.unescape(t).split())
    _intro = _clean(_lead)
    if _intro:
        _records.append({"p": _fn, "s": _LABEL[_fn], "h": _LABEL[_fn], "t": _intro[:420]})
    for _i in range(0, len(_rest), 3):
        _head, _chunk = _clean(_rest[_i + 1]), _clean(_rest[_i + 2] if _i + 2 < len(_rest) else "")
        if not _head and not _chunk: continue
        _records.append({"p": _fn, "s": _LABEL[_fn], "h": _head or _LABEL[_fn], "t": _chunk[:420]})
(OUT / "search-index.json").write_text(_json.dumps(_records, separators=(",", ":")))
print("search index:", len(_records), "records")

PUBLIC = [("index.html", "1.0"), ("how-it-works.html", "0.8"), ("plans.html", "0.9"),
          ("cities.html", "0.8"), ("about.html", "0.7"), ("faq.html", "0.7"),
          ("join.html", "0.9"), ("search.html", "0.5"), ("credits.html", "0.3"), ("accessibility.html", "0.3")] + [(u, "0.7") for u, _ in CITY_PAGES]
_today = __import__("datetime").date.today().isoformat()
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{'' if fn == 'index.html' else fn}</loc>"
              f"<lastmod>{_today}</lastmod><priority>{pr}</priority></url>\n"
              for fn, pr in PUBLIC)
    + "</urlset>\n")
(OUT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\n\n"
    f"Sitemap: {SITE}sitemap.xml\n")

(OUT / "img" / "favicon.svg").write_text((OUT / "img" / "mark.svg").read_text())

# ================================================================== OFFLINE
# NLC provides no internet. Everything is already self-hosted; this service
# worker also keeps the site working from its live URL if the connection
# drops after the first visit, and lets it be installed like an app.
(OUT / "manifest.webmanifest").write_text(_json.dumps({
    "name": "Marlowby", "short_name": "Marlowby",
    "description": "A new U.S. city in a box, every month.",
    "start_url": "./", "scope": "./", "display": "standalone",
    "background_color": "#F7F2EA", "theme_color": "#14234F",
    "icons": [
        {"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        {"src": "img/mark.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2))

_assets = set()
for _p in sorted(OUT.glob("*.html")):
    _assets.add(_p.name)
    for _ref in _re.findall(r'(?:src|href)="([^"#:]+)"', _p.read_text()):
        if not _ref.startswith(("mailto", "tel", "//")) and not _ref.endswith(".html"):
            _assets.add(_ref)
_fonts_css = (OUT / "vendor" / "fonts" / "fonts.css").read_text()
_assets |= {"vendor/fonts/" + u for u in _re.findall(r"url\(([^)]+\.woff2)\)", _fonts_css)}
_assets |= {"search-index.json", "manifest.webmanifest", "./"}
_missing = [a for a in _assets if a != "./" and not (OUT / a.split("?")[0]).exists()]
if _missing:
    raise SystemExit(f"service worker would precache missing files: {_missing}")
_sw = (OUT / "tools" / "sw.template.js").read_text()
(OUT / "sw.js").write_text(_sw.replace("__VERSION__", VER)
                              .replace("__PRECACHE__", _json.dumps(sorted(_assets), indent=2)))
print("service worker:", len(_assets), "files precached")
print("built", sorted(p.name for p in OUT.glob("*.html")))
