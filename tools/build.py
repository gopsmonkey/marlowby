"""Builds the Marlowby site (v2, logo-matched design). Usage: python3 build2.py <site folder>"""
import sys, pathlib, html as H

OUT = pathlib.Path(sys.argv[1])
VER = "24"  # bump to make browsers reload css/js

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
                "Skip or pause any month", "Every item from an independent local shop", "Gift plans never auto-renew"]
_dot = '<svg viewBox="0 0 50 64" aria-hidden="true"><path fill="currentColor" d="M25 63S5 41 5 24a20 20 0 0 1 40 0c0 17-20 39-20 39z"/></svg>'
_run = "".join(f"<span>{_dot}{t}</span>" for t in TICKER_ITEMS)
TICKER = f'''  <div class="ticker">
    <p class="visually-hidden">{". ".join(TICKER_ITEMS)}.</p>
    <div class="ticker-track" aria-hidden="true"><div>{_run}</div><div>{_run}</div></div>
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
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="faq.html#contact">Contact</a></li>
            <li><a href="about.html#makers">For makers</a></li>
            <li><a href="credits.html">Credits</a></li>
          </ul>
        </div>
      </div>
      <span class="footer-wm" aria-hidden="true">{wm()}</span>
      <div class="footer-bottom">
        <span>&copy; 2026 Marlowby. A concept site made for a student web design competition.</span>
        <a href="credits.html">Sources &amp; AI use</a>
      </div>
    </div>
  </footer>'''

FONTS = "https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Nunito:wght@700;800;900&family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&display=swap"
MOTION_JS = '''
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>'''
THREE_JS = '''
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/geometries/RoundedBoxGeometry.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/environments/RoomEnvironment.js"></script>
  <script src="js/scene.js?v={VER}"></script>'''

def page(filename, title, desc, body, extra_css="", three=False):
    doc = f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#14234F">
  <link rel="icon" href="img/mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css?v={VER}">{extra_css}
  <link rel="stylesheet" href="css/type.css?v={VER}">
</head>
<body>
{header(filename)}
  <main id="main">
{body}
  </main>
{FOOTER}{MOTION_JS}
  <script src="js/main.js?v={VER}"></script>{THREE_JS if three else ""}
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

def shot(name, alt, cls=""):
    """A rendered product photo (filled in by scene.js); the logo mark shows until it is ready."""
    c = f' class="{cls}"' if cls else ""
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
]
VOTES = [("nola", 549, 371, "New Orleans, Louisiana", 412), ("kc", 479, 206, "Kansas City, Missouri", 318),
         ("btv", 811, 109, "Burlington, Vermont", 264), ("sat", 418, 381, "San Antonio, Texas", 351)]

def us_map():
    pins = []
    for k, x, y, city, mo, yr, status, desc in CITIES:
        color = "#F7B731" if status == "now" else "#3F6FD1"
        pins.append(f'''          <g class="pin{" active" if status == "now" else ""}" data-key="{k}" tabindex="0" role="button" aria-label="{city}, {mo} {yr} box" data-city="{city}" data-month="{mo}" data-year="{yr}" data-desc="{H.escape(desc)}">
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

STYLE = {  # route card: tile color, sticker color, sticker text color
  "sav": ("amber", "#F7B731", "#14234F"), "sf": ("sky", "#AFCBF3", "#14234F"), "det": ("cream", "#3F6FD1", "#ffffff"),
  "pme": ("sky", "#F7B731", "#14234F"), "ash": ("amber", "#14234F", "#ffffff"), "tuc": ("cream", "#F7B731", "#14234F"),
  "msp": ("sky", "#3F6FD1", "#ffffff"), "boi": ("cream", "#14234F", "#ffffff")}
def route_card(i, c):
    k, x, y, city, mo, yr, status, desc = c
    tone, acc, ink = STYLE[k]
    name, state = city.split(", ")
    abbr = {"Georgia": "GA", "New Mexico": "NM", "Michigan": "MI", "Maine": "ME", "North Carolina": "NC",
            "Arizona": "AZ", "Minnesota": "MN", "Idaho": "ID"}[state]
    return f'''          <article class="route-card tile--{tone}">
            <span class="r-pill">{mo} {yr}</span>
            <button class="r-plus" type="button" aria-expanded="false" aria-controls="rc-{k}" aria-label="What is in the {name} box"><span aria-hidden="true"></span></button>
            <img data-shot="city" data-city="{name}" data-state="{abbr}" data-num="{i + 1:02d}" data-accent="{acc}" data-ink="{ink}" src="img/mark.svg" alt="The {name} box" width="960" height="800" loading="lazy">
            <h3>{name}</h3>
            <div class="r-more" id="rc-{k}"><p class="r-state">{state}</p><p>{desc}</p></div>
          </article>'''

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
     home, '\n  <link rel="stylesheet" href="css/home.css?v={VER}">', three=True)

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
     "How Marlowby works: choose a plan, we curate goods from local makers, and your box ships on the 1st of every month.", hiw, three=True)

# ================================================================== PLANS
def plan_card(name, price, desc, items, tone, shot_name, featured=False):
    lis = "".join(f"<li>{i}</li>" for i in items)
    flag = '<span class="plan-flag">Most picked</span>' if featured else ""
    btn = "btn--light" if tone == "navy" else "btn--primary"
    return f'''          <article class="tile tile--{tone} plan" id="{shot_name}" data-monthly="{price}">
            {flag}
            <div class="plan-img">{shot(shot_name, "")}</div>
            <h2>The {name}</h2>
            <p class="plan-desc">{desc}</p>
            <div class="price"><span class="amount">${price}</span><span>/ month</span></div>
            <p class="price-note" aria-live="polite"></p>
            <ul class="rule-list">{lis}</ul>
            <a class="btn {btn} btn--block" href="join.html?plan={name.replace(" ", "%20")}">Choose {name}</a>
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
{plan_card("Postcard", 29, "A small taste of each city. Good for trying us out, or as a gift.", ["4&ndash;5 local goods", "Field guide and map", "Maker cards"], "cream", "postcard")}
{plan_card("Neighborhood", 49, "Our main box, with room for food, a craft and something to do.", ["7&ndash;9 local goods", "Field guide and map", "At-home experience", "Swaps for allergies and diets"], "navy", "neighborhood", True)}
{plan_card("Grand Tour", 79, "The whole city, for big households and people who want it all.", ["10&ndash;12 local goods", "Everything in Neighborhood", "Live online maker workshop", "One limited-edition item"], "sky", "grandtour")}
        </div>
        <p class="note-small" style="margin-top:28px">Reserve before January 1, 2027 and you keep these prices for as long as you stay subscribed.</p>
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
        <ul class="rule-list gift-list" data-rise-group>
          <li><span><strong>3 months</strong><small>A season of cities</small></span><b>from $87</b></li>
          <li><span><strong>6 months</strong><small>Half a year</small></span><b>from $162</b></li>
          <li><span><strong>12 months</strong><small>All 12 cities, plus a map poster</small></span><b>from $296</b></li>
        </ul>
      </div>
    </section>

{CTA}'''
page("plans.html", "Plans & Pricing | Marlowby",
     "Compare the Marlowby Postcard, Neighborhood and Grand Tour boxes, with monthly, yearly and gift options.", plans, three=True)

# ================================================================== CITIES
ABBR = {"Georgia": "GA", "New Mexico": "NM", "Michigan": "MI", "Maine": "ME", "North Carolina": "NC",
        "Arizona": "AZ", "Minnesota": "MN", "Idaho": "ID"}

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
    return (f'<img data-shot="city" data-city="{name}" data-state="{ABBR[state]}" data-num="{i + 1:02d}" data-accent="{acc}" '
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
            <div class="cal-city"><h3>{c[3].split(", ")[0]}</h3><p>{c[3].split(", ")[1]} &middot; Box No. {i + 1:02d}{" &middot; <b>First box</b>" if c[6] == "now" else ""}</p></div>
            {chips(c[7])}
            <div class="cal-img">{city_shot(i, c, ' loading="lazy"')}</div>
          </li>''' for i, c in enumerate(CITIES))

votes = "\n".join(f'''          <div class="vote-item" data-city="{city}" data-votes="{n}">
            <span><strong>{city}</strong> <span class="pct"></span></span>
            <button type="button" aria-pressed="false">Vote</button>
            <div class="vote-bar" aria-hidden="true"><span></span></div>
          </div>''' for _, _, _, city, n in VOTES)

cities = f'''    <section class="c-hero">
      <div class="container c-hero-grid">
        <div class="c-hero-copy">
          <h1 data-lines>{lines("Eight cities.", "Eight boxes.", "One <em>a month.</em>")}</h1>
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
     f'\n  <link rel="stylesheet" href="css/pages.css?v={VER}">', three=True)

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
     f'\n  <link rel="stylesheet" href="css/pages.css?v={VER}">', three=True)

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
          <form id="contact-form" novalidate onsubmit="event.preventDefault(); var m=this.querySelector('.form-msg'); if(this.checkValidity()){{m.textContent='Thanks! We will reply within one business day.'; this.reset();}} else {{m.textContent='Please add your name, a valid email and a message.';}}">
            <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div>
            <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
            <div class="field"><label for="c-topic">Topic</label>
              <select id="c-topic" name="topic"><option>A question</option><option>Nominate a city</option><option>Become a maker partner</option><option>Help with an order</option></select></div>
            <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="5" required></textarea></div>
            <button class="btn btn--primary btn--block" type="submit">Send</button>
            <p class="form-msg" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>'''
page("faq.html", "FAQ & Contact | Marlowby",
     "Answers about Marlowby boxes, shipping, skipping, canceling and gift subscriptions, plus how to contact us.", faq)

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
              <fieldset class="field">
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
                <label for="terms" style="font-weight:500;flex:1">I understand reserving is free and I can cancel any time before my first box ships.</label>
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
     "Reserve your Marlowby subscription box in three short steps.", join)

# ================================================================== CREDITS
credits = f'''{page_head(("Credits and", "sources."), "Every outside resource used to build this site, following the competition&rsquo;s copyright, fair use and AI usage rules.")}

    <section class="section section--tight" aria-labelledby="credits-title">
      <h2 id="credits-title" class="visually-hidden">Sources and credits</h2>
      <div class="container" style="max-width:880px">
        <ul class="rule-list credits">
          <li><h3>About this site</h3><p>Marlowby is a fictional company. This site is a concept made for a student web design competition. The test-box quotes, makers, products and vote counts are illustrative, not real people or businesses.</p></li>
          <li><h3>Logo</h3><p>The Marlowby logo was designed by our team. The SVG version on this site was redrawn from it.</p></li>
          <li><h3>3D scenes and product images</h3><p>The falling box, the shelf room and the box photos are drawn live in the browser with code written for this project. No stock photos, 3D models or third-party images are used. The U.S. map outline is a simplified shape plotted from public latitude and longitude points.</p></li>
          <li><h3>Design reference</h3><p>The layout style (rounded color blocks, floating menu, a product dropping into a scene on scroll) was inspired by the Bella Kitchenware website. No text, images, code or branding from that site were copied.</p></li>
          <li><h3>Shop layout research</h3><p>General shop patterns (a trust ticker, a shrinking menu bar, product tags on photos, a carousel with a progress bar) were studied on Mobbin screenshots of the Hims, Graza, Oura and Seed websites, and on the Graza, Olipop and Omsom websites. Only general layout ideas were used. No text, images, code or branding from those sites were copied.</p></li>
          <li><h3>Fonts</h3><p><strong>Nunito</strong> by Vernon Adams, <strong>Figtree</strong> by Erik Kennedy, <strong>Instrument Serif</strong> by Rodrigo Fuenzalida and Jordan Egstad, and <strong>DM Mono</strong> by Colophon Foundry, all under the SIL Open Font License, served by Google Fonts.</p></li>
          <li><h3>Code libraries</h3><p><strong>three.js</strong> r128 (MIT License) for 3D, <strong>GSAP</strong> 3.12 with ScrollTrigger (GreenSock standard no-charge license) for scroll animation, and <strong>Lenis</strong> 1.1 (MIT License) for smooth scrolling. Everything else is hand-written HTML, CSS and JavaScript.</p></li>
          <li><h3>Artificial intelligence use</h3><p><em>[Team: complete this section following the event&rsquo;s AI Usage and Citation Policy. List each AI tool, what it was used for, and the dates.]</em></p>
            <p>Example citation: Anthropic. (2026). <em>Claude</em> [Large language model]. Used to help write the HTML, CSS and JavaScript and to draft copy, which the team reviewed and edited. https://claude.ai</p></li>
        </ul>
      </div>
    </section>'''
page("credits.html", "Credits & Sources | Marlowby",
     "Credits, sources, licenses and AI usage citation for the Marlowby concept website.", credits)

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
     "That page could not be found. Here are the main pages of the Marlowby site.", notfound)

(OUT / "img" / "favicon.svg").write_text((OUT / "img" / "mark.svg").read_text())
print("built", sorted(p.name for p in OUT.glob("*.html")))
