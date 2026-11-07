# Marlowby design system

Every color, shape and motion on the site comes from the Marlowby logo. The layout patterns were studied from bellakitchenware.com, but none of its content was copied.

## Brand (from the logo)

| Token | Hex | Where it comes from | Use |
|---|---|---|---|
| `--navy` | #14234F | Wordmark and outlines | Text, primary buttons, dark tiles, footer |
| `--blue` | #3F6FD1 | Skyline buildings | Numbers, tags, sky top |
| `--sky` / `--sky-soft` | #AFCBF3 / #E4EDFB | Dome building | Light tiles, map fill |
| `--cream` | #FCEAD6 | The open box | Box material, warm tiles |
| `--amber` | #F7B731 | The sparks | Accent only: pills, link underlines, "first box" pin |
| `--bg` | #F7F2EA | Paper | Page background |

The wordmark's "o" is the map pin from the logo, used everywhere the name appears (`.wm` / `.wm-o`).

## Type
Four fonts, each with one job. Rules live in `css/type.css` and the mono list in `css/styles.css`.
- **Nunito** 800–900: every heading, card title, big number and button. It is rounded like the logo lettering.
- **Figtree** 400–700: all running text, the nav, chips and form labels.
- **Instrument Serif** italic, used sparingly: one accent phrase in the page h1s and a few home/cities headings (blue gradient, amber on dark tiles), the rotating hero city, and customer quotes.
- **DM Mono**: only tiny tags (pills, the ticker, product tag and price, calendar year, countdown, journey dates).
- Gradients: navy tiles use two soft radial glows; blue, amber, sky and cream tiles use gentle linear blends. Page heroes get a faint sky/amber glow. A slow starburst sticker marks the key fact on the Cities and About heroes.
- No uppercase eyebrow labels and no letter-spaced kickers.

## Layout rules (what makes it look designed, not generated)
1. **A 12-column grid** (`.grid12`, 6 columns on phones). Headings take 8 columns and the lead takes 4, aligned to the bottom.
2. **Big rounded color blocks** (`.tile`, 24px radius) instead of white cards with icons. Each section uses one or two brand colors, never all of them.
3. **Real objects instead of icons.** The boxes are rendered 3D objects with paper texture, soft shadows and the logo printed on them. No icon badges, check-circle lists, stat counters or letter avatars.
4. **Short, specific copy.** Real dates, prices and places. Few em dashes and no slogans stacked on slogans.
5. **A floating white menu bar** with the current page shown as a navy pill.
6. **Centered section titles** above product grids. Small blue tags above product names.

## 3D scenes (js/scene.js, three.js r128)
- Boxes: rounded boxes with canvas-drawn paper texture, the wordmark, a numbered city sticker on the side and a skyline print on the lid.
- Lighting: a studio environment map (RoomEnvironment) plus one warm key light, with ACES tone mapping and soft shadows.
- Shelf room: plaster wall, framed city map, oak top on a navy sideboard with brass knobs, books and a vase.
- Product photos are rendered once on page load from the same box model, so they always match the hero.

## Motion
| What | Spec |
|---|---|
| Box drop | Tied to scroll. Eases in and out on the vertical and out on the horizontal. Follows the scroll with damping (`follow` 0.1). |
| Idle | A 6px bob plus a gentle sway while hanging in the sky. Both fade out as it falls. |
| Balloons | Let go between 20% and 62% of the drop, then float up and fade. |
| Landing | The falling box casts a real shadow into the room, and a soft contact shadow fades in under it. |
| Headings | Slide up line by line (`[data-lines]`), 1.05s, power4.out, 0.09s stagger. |
| Blocks | Fade up 48px (`[data-rise]`, `[data-rise-group]`). |
| Scrolling | Lenis smooth scroll on desktop. Phones keep native scrolling. |
| Reduced motion | No smooth scroll and no reveals. The box sits on the shelf and the balloons are gone. |

Open `index.html?tune` to get a live panel with sliders for every drop value, plus a "Copy values as JSON" button. Paste the result into `DEFAULTS` in `js/scene.js` to keep it.

## Shop patterns (studied on Mobbin: Hims, Graza, Oura, Seed)
Only the ideas below were borrowed. No content or assets from those sites were copied.
- **Trust bar**: a slow navy ticker above the menu (free shipping, ship date, skip any month). It pauses on hover and stops when the device asks for reduced motion.
- **Shrinking menu bar**: once you scroll, the white bar narrows to 1040px and gets a deeper shadow.
- **Cycling hero word**: "A new city at your door:" then the 2027 route cities slide through in amber, one every 2.2 seconds.
- **Product cards**: an outlined tag and the price sit on the photo. Below them are a small size line and the name, which gets an amber underline on hover.
- **Big pill button**: a full-width amber "Compare all three" button with a hard navy offset shadow that presses down on hover and click.
- **Explained phrases**: a large statement with dotted-underline phrases. Hovering or focusing one shows a short navy tooltip.
- **Route carousel**: city cards with a month pill, the city's own rendered box, and a "+" that opens the details with a circle wipe. Below them are a progress line and arrow buttons.
- **Phone menu**: a right-side drawer with large rows and arrows, a navy "Reserve" card at the bottom, and the menu icon turning into an X.
