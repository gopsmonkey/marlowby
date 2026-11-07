/* ==========================================================
   Marlowby home — 3D scenes (three.js r128)

   Two WebGL canvases share one look (same box, lights, environment):
   1. .gl-canvas   covers the hero + shelf. Draws the falling box, its
                   balloons, and the box turning on the navy promo card.
   2. .scene-canvas inside the shelf card. Draws the room: wall, framed
                   map, sideboard, books, vase, the boxes already on the
                   shelf, and the falling box's shadow (an invisible
                   stand-in that only casts shadow).
   Both canvases scroll with the page, so nothing lags behind scrolling.
   Scroll progress drives the drop; motion values live in CFG and can
   be tuned live by opening the page with ?tune.

   Also renders the product photos for the "Pick your box" grid.
   ========================================================== */
(function () {
  const root = document.documentElement;
  const zone = document.querySelector(".gl-zone");            // home page only
  const shotsWanted = document.querySelector("img[data-shot]"); // product photos (home, plans, how it works)
  if (!zone && !shotsWanted) return;
  const zoneCanvas = zone && zone.querySelector(".gl-canvas");
  const sceneCanvas = zone && zone.querySelector(".scene-canvas");
  const anchor = zone && zone.querySelector(".fly-anchor");
  const promoAnchor = zone && zone.querySelector(".promo-anchor");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const tuneMode = /[?&]tune\b/.test(location.search);

  const glOK = (() => {
    try { const c = document.createElement("canvas"); return !!(c.getContext("webgl") || c.getContext("experimental-webgl")); }
    catch (e) { return false; }
  })();
  if (!window.THREE || !THREE.RoundedBoxGeometry || !THREE.RoomEnvironment || !glOK) {
    root.classList.add("no-gl");
    return;
  }

  // Box labels use the brand fonts, so wait for them (max 3s) before drawing anything.
  const fontsReady = document.fonts
    ? Promise.race([
        Promise.all([document.fonts.load("900 80px Nunito"), document.fonts.load("700 30px Figtree")]),
        new Promise((r) => setTimeout(r, 3000))])
    : Promise.resolve();
  fontsReady.then(start).catch((err) => { console.error(err); root.classList.add("no-gl"); });

  function start() {

  /* ---------- Motion settings (tunable with ?tune) ---------- */
  const DEFAULTS = {
    follow: 0.1,        // how quickly the box catches up with the scroll (lower = floatier)
    endAt: 0.56,        // the box lands when its slot is this far down the screen
    releaseStart: 0.2,  // balloons let go at this point of the drop
    releaseLen: 0.42,   // ...and take this long to float away
    spin: 34,           // degrees of turning while falling
    roll: 8,            // degrees of side-to-side swing while falling
    float: 6,           // px of gentle bobbing while hanging in the sky
    floatSpeed: 1.1,    // bobbing speed
    pitchStart: 14,     // how much of the lid you see in the sky (deg)
    yaw: -22,           // final turn of the box on the shelf (deg)
    contactShadow: 0.6, // strength of the soft shadow under the landed box
  };
  let saved = {};
  if (tuneMode) { try { saved = JSON.parse(localStorage.getItem("marlowby-tune") || "{}"); } catch (e) {} }
  const CFG = Object.assign({}, DEFAULTS, saved);

  const DEG = Math.PI / 180;
  const ROOM_PITCH = 8;                       // camera looks slightly down on the shelf
  const BOX = { w: 150, h: 104, d: 112 };     // box size in scene units
  const DESIGN_W = 1100, DESIGN_H = 620;      // shelf scene units
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const smooth = (a, b, t) => { const x = clamp((t - a) / (b - a)); return x * x * (3 - 2 * x); };
  const srgb = (hex) => new THREE.Color(hex).convertSRGBToLinear();

  const C = { navy: "#14234F", blue: "#3F6FD1", sky: "#AFCBF3", cream: "#F8E6CF", amber: "#F7B731", slate: "#6E86B8" };
  const SAVANNAH = { city: "Savannah", state: "GA", num: "01", accent: C.amber, ink: C.navy };
  const SHELF = [
    { x: -380, yaw: -17, meta: { city: "Santa Fe", state: "NM", num: "02", accent: C.sky, ink: C.navy } },
    { x: -190, yaw: -26, meta: { city: "Detroit", state: "MI", num: "03", accent: C.blue, ink: "#ffffff" } },
    { x: 190, yaw: -28, meta: { city: "Portland", state: "ME", num: "04", accent: C.amber, ink: C.navy } },
    { x: 380, yaw: -19, meta: { city: "Asheville", state: "NC", num: "05", accent: C.navy, ink: "#ffffff" } },
  ];

  /* ==========================================================
     Textures, drawn on 2D canvases
     ========================================================== */
  const S = 6; // texture pixels per scene unit
  const texCache = new Map();
  function canvasTexture(key, w, h, draw) {
    if (!texCache.has(key)) {
      const c = document.createElement("canvas");
      c.width = Math.round(w); c.height = Math.round(h);
      draw(c.getContext("2d"), c.width, c.height);
      const t = new THREE.CanvasTexture(c);
      t.encoding = THREE.sRGBEncoding;
      t.anisotropy = 8;
      texCache.set(key, t);
    }
    return texCache.get(key);
  }

  function paper(g, w, h, base) {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 26; i++) {                     // soft mottling
      const x = Math.random() * w, y = Math.random() * h, r = (0.15 + Math.random() * 0.35) * Math.max(w, h);
      const gr = g.createRadialGradient(x, y, 0, x, y, r);
      const dark = Math.random() < 0.5;
      gr.addColorStop(0, dark ? "rgba(120,85,50,.035)" : "rgba(255,255,255,.05)");
      gr.addColorStop(1, "rgba(0,0,0,0)");
      g.fillStyle = gr; g.fillRect(0, 0, w, h);
    }
    const n = (w * h) / 110;                           // paper fibres
    for (let i = 0; i < n; i++) {
      const r = Math.random();
      g.fillStyle = r < 0.5 ? `rgba(110,80,50,${r * 0.12})` : `rgba(255,255,255,${(r - 0.5) * 0.16})`;
      g.fillRect(Math.random() * w, Math.random() * h, 1 + Math.random() * 5, 1);
    }
  }

  // The map-pin "o" from the logo. baseline = text baseline, size = font size.
  function pin(g, cx, baseline, size, color, hole) {
    const r = size * 0.25, cy = baseline - size * 0.37, tip = baseline + size * 0.07;
    g.fillStyle = color;
    g.beginPath();
    g.moveTo(cx, tip);
    g.bezierCurveTo(cx - r * 0.35, tip - r * 0.6, cx - r, cy + r * 0.75, cx - r, cy);
    g.arc(cx, cy, r, Math.PI, 0);
    g.bezierCurveTo(cx + r, cy + r * 0.75, cx + r * 0.35, tip - r * 0.6, cx, tip);
    g.fill();
    g.fillStyle = hole;
    g.beginPath(); g.arc(cx, cy, r * 0.38, 0, Math.PI * 2); g.fill();
  }

  function wordmark(g, cx, baseline, size, color, hole) {
    g.font = `900 ${size}px Nunito, "Arial Rounded MT Bold", sans-serif`;
    if ("letterSpacing" in g) g.letterSpacing = `${-0.035 * size}px`;
    g.textBaseline = "alphabetic"; g.textAlign = "left";
    const a = g.measureText("Marl").width, b = g.measureText("wby").width, pw = size * 0.52;
    let x = cx - (a + pw + b) / 2;
    g.fillStyle = color; g.fillText("Marl", x, baseline);
    pin(g, x + a + pw / 2, baseline, size, color, hole);
    g.fillStyle = color; g.fillText("wby", x + a + pw, baseline);
    if ("letterSpacing" in g) g.letterSpacing = "0px";
  }

  function lidLine(g, w, h) {
    const y = h * 0.14;
    g.fillStyle = "rgba(255,255,255,.14)"; g.fillRect(0, 0, w, y);
    g.fillStyle = "rgba(20,35,79,.16)"; g.fillRect(0, y, w, Math.max(2, S * 0.5));
    const gr = g.createLinearGradient(0, y, 0, y + S * 3);
    gr.addColorStop(0, "rgba(20,35,79,.08)"); gr.addColorStop(1, "rgba(20,35,79,0)");
    g.fillStyle = gr; g.fillRect(0, y, w, S * 3);
  }

  function frontTex(meta, dims) {
    return canvasTexture(`front-${meta.num}-${dims.w}x${dims.h}`, dims.w * S, dims.h * S, (g, w, h) => {
      paper(g, w, h, C.cream); lidLine(g, w, h);
      const size = Math.min(w * 0.17, h * 0.27);
      wordmark(g, w / 2, h * 0.52, size, C.navy, C.cream);
      // the label from the logo's box: a pin and two lines
      const s = size * 0.62, by = h * 0.83;
      pin(g, w * 0.13, by, s, C.navy, C.cream);
      g.strokeStyle = C.slate; g.lineCap = "round"; g.lineWidth = S * 1.9;
      g.beginPath(); g.moveTo(w * 0.2, by - s * 0.42); g.lineTo(w * 0.36, by - s * 0.42); g.stroke();
      g.beginPath(); g.moveTo(w * 0.2, by - s * 0.12); g.lineTo(w * 0.31, by - s * 0.12); g.stroke();
      g.fillStyle = C.navy; g.font = `700 ${size * 0.3}px Figtree, sans-serif`; g.textAlign = "right";
      if ("letterSpacing" in g) g.letterSpacing = `${size * 0.03}px`;
      g.fillText(`No. ${meta.num}`, w * 0.92, by - s * 0.1);
    });
  }

  function sideTex(meta, dims) {
    return canvasTexture(`side-${meta.num}-${dims.d}x${dims.h}`, dims.d * S, dims.h * S, (g, w, h) => {
      paper(g, w, h, C.cream); lidLine(g, w, h);
      const r = Math.min(w, h) * 0.2, cx = w / 2, cy = h * 0.5;
      g.fillStyle = meta.accent; g.beginPath(); g.arc(cx, cy, r, 0, Math.PI * 2); g.fill();
      g.strokeStyle = "rgba(255,255,255,.75)"; g.lineWidth = S * 0.9; g.setLineDash([S * 1.6, S * 1.2]);
      g.beginPath(); g.arc(cx, cy, r * 0.82, 0, Math.PI * 2); g.stroke(); g.setLineDash([]);
      g.fillStyle = meta.ink; g.textAlign = "center"; g.textBaseline = "middle";
      g.font = `900 ${r * 0.78}px Nunito, sans-serif`; g.fillText(meta.num, cx, cy + r * 0.05);
      g.fillStyle = C.navy; g.font = `700 ${r * 0.32}px Figtree, sans-serif`;
      if ("letterSpacing" in g) g.letterSpacing = `${r * 0.06}px`;
      g.fillText(`${meta.city.toUpperCase()}, ${meta.state}`, cx, h * 0.84);
      if ("letterSpacing" in g) g.letterSpacing = "0px";
    });
  }

  function topTex(dims) {
    return canvasTexture(`top-${dims.w}x${dims.d}`, dims.w * S, dims.d * S, (g, w, h) => {
      paper(g, w, h, "#FAECD9");
      g.fillStyle = "rgba(20,35,79,.14)"; g.fillRect(0, h * 0.86, w, Math.max(2, S * 0.5)); // tuck flap
      // skyline print from the logo, in light blue
      const u = Math.min(w, h) / 90, x0 = w / 2 - 34 * u, base = h * 0.66;
      g.fillStyle = "rgba(175,203,243,.95)"; g.strokeStyle = "rgba(175,203,243,.95)"; g.lineWidth = u * 1.6; g.lineCap = "round";
      g.fillRect(x0, base - 18 * u, 9 * u, 18 * u);
      g.fillRect(x0 + 10 * u, base - 30 * u, 10 * u, 30 * u);
      g.fillRect(x0 + 21 * u, base - 44 * u, 9 * u, 44 * u);
      g.beginPath(); g.moveTo(x0 + 25.5 * u, base - 44 * u); g.lineTo(x0 + 25.5 * u, base - 54 * u); g.stroke();
      g.fillRect(x0 + 32 * u, base - 24 * u, 18 * u, 24 * u);
      g.beginPath(); g.arc(x0 + 41 * u, base - 24 * u, 9 * u, Math.PI, 0); g.fill();
      g.beginPath(); g.arc(x0 + 60 * u, base - 13 * u, 11 * u, 0, Math.PI * 2); g.stroke();
      for (let i = 0; i < 4; i++) {
        const a = (i * Math.PI) / 4;
        g.beginPath(); g.moveTo(x0 + 60 * u + Math.cos(a) * 11 * u, base - 13 * u + Math.sin(a) * 11 * u);
        g.lineTo(x0 + 60 * u - Math.cos(a) * 11 * u, base - 13 * u - Math.sin(a) * 11 * u); g.stroke();
      }
      g.fillRect(x0 - 6 * u, base, 80 * u, u * 1.4);
    });
  }

  const plainTex = (dims, base) => canvasTexture(`plain-${base}-${dims.w}x${dims.h}`, dims.w * S * 0.5, dims.h * S * 0.5,
    (g, w, h) => { paper(g, w, h, base); });

  const boxGeoCache = new Map();
  function boxGeometry(dims) {
    const k = `${dims.w}x${dims.h}x${dims.d}`;
    if (!boxGeoCache.has(k)) boxGeoCache.set(k, new THREE.RoundedBoxGeometry(dims.w, dims.h, dims.d, 4, 4.5));
    return boxGeoCache.get(k);
  }
  function makeBox(meta, dims = BOX) {
    const m = (map) => new THREE.MeshStandardMaterial({ map, roughness: 0.84, metalness: 0, envMapIntensity: 0.9 });
    const side = m(sideTex(meta, dims));
    // face order: +x (right), -x (left), +y (top), -y (bottom), +z (front), -z (back)
    const mats = [side, side, m(topTex(dims)), m(plainTex(dims, "#EAD6BC")), m(frontTex(meta, dims)), m(plainTex(dims, C.cream))];
    const mesh = new THREE.Mesh(boxGeometry(dims), mats);
    mesh.castShadow = true; mesh.receiveShadow = true;
    return mesh;
  }

  function makeBalloons() {
    const group = new THREE.Group();
    const sphere = new THREE.SphereGeometry(1, 48, 32);
    const knot = new THREE.ConeGeometry(5, 9, 16);
    const tie = new THREE.Vector3(0, 58, 0);
    const mats = [];
    [ // six balloons: x, y, radius, color, depth
      [-96, 200, 34, C.amber, 8], [-40, 252, 37, "#7FA6EC", -20], [26, 286, 40, C.blue, -34],
      [90, 238, 36, "#F9CF6A", -6], [-2, 196, 33, "#FFFFFF", 24], [66, 170, 31, C.sky, 30],
    ].forEach(([x, y, r, hex, z]) => {
      const mat = new THREE.MeshStandardMaterial({ color: srgb(hex), roughness: 0.28, metalness: 0, envMapIntensity: 1.15, transparent: true });
      mats.push(mat);
      const b = new THREE.Mesh(sphere, mat);
      b.scale.set(r, r * 1.16, r * 0.96); b.position.set(x, y, z);
      const k = new THREE.Mesh(knot, mat);
      k.position.set(x, y - r * 1.16 - 2, z); k.rotation.z = Math.PI;
      const lineMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 });
      mats.push(lineMat);
      const pts = [], start = new THREE.Vector3(x, y - r * 1.16 - 6, z);
      for (let i = 0; i <= 20; i++) {
        const t = i / 20, q = start.clone().lerp(tie, t);
        q.x += Math.sin(t * Math.PI) * x * 0.06;
        pts.push(q);
      }
      group.add(b, k, new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat));
    });
    group.userData.mats = mats;
    return group;
  }

  /* ==========================================================
     Shared renderer setup
     ========================================================== */
  const KEY_DIR = new THREE.Vector3(-0.55, 0.9, 0.75).normalize();
  function makeRenderer(canvas, opts = {}) {
    const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, ...opts });
    r.outputEncoding = THREE.sRGBEncoding;
    r.toneMapping = THREE.ACESFilmicToneMapping;
    r.toneMappingExposure = 1.12;
    r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    return r;
  }
  function makeEnvironment(renderer) {
    const pm = new THREE.PMREMGenerator(renderer);
    const env = pm.fromScene(new THREE.RoomEnvironment(), 0.04).texture;
    pm.dispose();
    return env;
  }
  function keyLight(intensity = 1.25) {
    const l = new THREE.DirectionalLight(0xfff3e4, intensity);
    return l;
  }

  // Soft contact shadow texture (a blurred dark blob, strongest in the middle)
  const blobTex = canvasTexture("blob", 256, 256, (g, w, h) => {
    const gr = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    gr.addColorStop(0, "rgba(20,25,45,.75)"); gr.addColorStop(0.45, "rgba(20,25,45,.45)"); gr.addColorStop(1, "rgba(20,25,45,0)");
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  });
  blobTex.encoding = THREE.LinearEncoding;
  const PLANS = {
    postcard: { w: 128, h: 60, d: 100 },
    neighborhood: BOX,
    grandtour: { w: 178, h: 126, d: 132 },
  };
  if (!zone) {               // pages with product photos but no drop scene
    (window.requestIdleCallback || ((f) => setTimeout(f, 200)))(renderProducts);
    return;
  }

  /* ==========================================================
     1. The room (inside the shelf card)
     ========================================================== */
  const roomR = makeRenderer(sceneCanvas);
  roomR.shadowMap.enabled = true;
  roomR.shadowMap.type = THREE.PCFSoftShadowMap;
  const roomScene = new THREE.Scene();
  roomScene.environment = makeEnvironment(roomR);
  const roomCam = new THREE.OrthographicCamera(0, DESIGN_W, 0, -DESIGN_H, -4000, 4000);

  const room = new THREE.Group();
  room.position.set(DESIGN_W / 2, -DESIGN_H / 2 - 20, 0);
  room.rotation.x = ROOM_PITCH * DEG;
  roomScene.add(room);

  const roomKey = keyLight(1.35);
  roomKey.castShadow = true;
  roomKey.shadow.mapSize.set(2048, 2048);
  Object.assign(roomKey.shadow.camera, { left: -900, right: 900, top: 900, bottom: -900, near: 10, far: 4000 });
  roomKey.shadow.bias = -0.0006;
  roomKey.shadow.normalBias = 0.6;
  roomKey.target.position.set(DESIGN_W / 2, -DESIGN_H / 2, 0);
  roomKey.position.copy(roomKey.target.position).addScaledVector(KEY_DIR, 1600);
  roomScene.add(roomKey, roomKey.target);

  const std = (opts) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.8, metalness: 0 }, opts));

  // Wall: soft blue plaster
  const wallTex = canvasTexture("wall", 1400, 800, (g, w, h) => {
    paper(g, w, h, "#DCE6F5");
    const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "rgba(255,255,255,.18)"); gr.addColorStop(1, "rgba(20,35,79,.06)");
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
  });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(2600, 1500), std({ map: wallTex, roughness: 0.95 }));
  wall.position.set(0, 160, -180); wall.receiveShadow = true;
  room.add(wall);

  // Framed map of Savannah on the wall
  const mapTex = canvasTexture("map", 680, 880, (g, w, h) => {
    paper(g, w, h, "#FBF6EE");
    g.strokeStyle = "#D7E2F4"; g.lineWidth = 3;
    for (let x = 30; x < w; x += 46) { g.beginPath(); g.moveTo(x, 30); g.lineTo(x + 18, h - 150); g.stroke(); }
    for (let y = 40; y < h - 150; y += 52) { g.beginPath(); g.moveTo(20, y); g.lineTo(w - 20, y - 14); g.stroke(); }
    g.strokeStyle = C.sky; g.lineWidth = 9;
    g.beginPath(); g.moveTo(40, 160); g.lineTo(w - 40, 120); g.stroke();
    g.beginPath(); g.moveTo(220, 30); g.lineTo(260, h - 150); g.stroke();
    g.strokeStyle = "#8FB3EA"; g.lineWidth = 46; g.lineCap = "round";
    g.beginPath(); g.moveTo(-20, h - 250); g.bezierCurveTo(200, h - 330, 420, h - 200, w + 20, h - 300); g.stroke();
    pin(g, w * 0.55, h * 0.45, 120, C.navy, "#FBF6EE");
    g.fillStyle = C.navy; g.textAlign = "center";
    g.font = "900 64px Nunito, sans-serif"; g.fillText("Savannah", w / 2, h - 70);
    g.font = "700 22px Figtree, sans-serif"; if ("letterSpacing" in g) g.letterSpacing = "6px";
    g.fillText("GEORGIA · BOX NO. 01", w / 2, h - 34);
  });
  const frameMesh = new THREE.Mesh(new THREE.RoundedBoxGeometry(200, 252, 10, 2, 3), std({ color: srgb("#B98A5B"), roughness: 0.6 }));
  frameMesh.position.set(-330, 190, -172); frameMesh.castShadow = true;
  const print = new THREE.Mesh(new THREE.PlaneGeometry(172, 224), std({ map: mapTex, roughness: 0.9 }));
  print.position.set(-330, 190, -166.5);
  room.add(frameMesh, print);

  // Sideboard: oak top, navy body, brass knobs
  const oakTex = canvasTexture("oak", 1600, 320, (g, w, h) => {
    g.fillStyle = "#C99B6C"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 160; i++) {
      const y = Math.random() * h, a = Math.random() * 0.12;
      g.strokeStyle = Math.random() < 0.5 ? `rgba(120,78,40,${a})` : `rgba(255,236,210,${a})`;
      g.lineWidth = 1 + Math.random() * 3;
      g.beginPath(); g.moveTo(0, y);
      for (let x = 0; x <= w; x += 80) g.lineTo(x, y + Math.sin(x / 140 + i) * 6);
      g.stroke();
    }
  });
  oakTex.wrapS = oakTex.wrapT = THREE.RepeatWrapping;
  const top = new THREE.Mesh(new THREE.RoundedBoxGeometry(1260, 26, 252, 3, 5), std({ map: oakTex, roughness: 0.55 }));
  top.position.set(0, -113, -50); top.receiveShadow = true; top.castShadow = true;
  const body = new THREE.Mesh(new THREE.RoundedBoxGeometry(1210, 340, 232, 3, 8), std({ color: srgb("#1B2B60"), roughness: 0.5 }));
  body.position.set(0, -296, -58); body.receiveShadow = true;
  room.add(top, body);
  const grooveMat = std({ color: srgb("#0E1838"), roughness: 0.7 });
  const brass = std({ color: srgb("#D9A748"), metalness: 0.85, roughness: 0.32 });
  [-300, 0, 300].forEach((x) => {
    const gr = new THREE.Mesh(new THREE.BoxGeometry(4, 300, 2), grooveMat);
    gr.position.set(x, -300, 58.5); room.add(gr);
    [-1, 1].forEach((s) => {
      const k = new THREE.Mesh(new THREE.SphereGeometry(7, 24, 16), brass);
      k.position.set(x + s * 24, -190, 64); k.castShadow = true; room.add(k);
    });
  });

  // Books, stacked
  [["#3F6FD1", 0, 4], ["#F3E3CC", 20, -3], [C.navy, 40, 6]].forEach(([hex, dy, rot], i) => {
    const b = new THREE.Mesh(new THREE.RoundedBoxGeometry(150 - i * 8, 19, 104 - i * 4, 2, 2.5), std({ color: srgb(hex), roughness: 0.75 }));
    b.position.set(-535, -90 + dy, -20); b.rotation.y = rot * DEG; b.castShadow = b.receiveShadow = true;
    room.add(b);
  });

  // Ceramic vase with two eucalyptus stems
  const vaseProfile = [[0, 0], [30, 0], [38, 10], [42, 42], [36, 82], [22, 108], [19, 126], [24, 134]].map(([r, y]) => new THREE.Vector2(r, y));
  const vase = new THREE.Mesh(new THREE.LatheGeometry(vaseProfile, 64), std({ color: srgb("#F3EEE7"), roughness: 0.35 }));
  vase.position.set(530, -100, -30); vase.castShadow = vase.receiveShadow = true;
  room.add(vase);
  const stemMat = std({ color: srgb("#5E7A5A"), roughness: 0.7 });
  const leafMat = std({ color: srgb("#8DA889"), roughness: 0.65, side: THREE.DoubleSide });
  [[-1, 250], [1, 290]].forEach(([dir, len]) => {
    const curve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, 120, 0), new THREE.Vector3(dir * 18, 180, 6),
      new THREE.Vector3(dir * 46, len - 40, 4), new THREE.Vector3(dir * 70, len, -4)]);
    const stem = new THREE.Mesh(new THREE.TubeGeometry(curve, 40, 1.8, 8), stemMat);
    stem.position.copy(vase.position); stem.castShadow = true; room.add(stem);
    for (let i = 3; i < 12; i++) {
      const t = i / 12, p = curve.getPoint(t);
      const leaf = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), leafMat);
      leaf.scale.set(13 - t * 5, 7 - t * 2.5, 2);
      leaf.position.copy(p).add(vase.position).add(new THREE.Vector3((i % 2 ? 10 : -10), 0, 0));
      leaf.rotation.z = (i % 2 ? -0.6 : 0.6); leaf.castShadow = true;
      room.add(leaf);
    }
  });

  function contactShadow(x, yaw, opacity) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(BOX.w * 1.18, BOX.d * 1.18),
      new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, opacity, depthWrite: false }));
    m.rotation.x = -Math.PI / 2; m.rotation.z = yaw * DEG;
    m.position.set(x, -99.4, -10);
    room.add(m);
    return m;
  }

  // Boxes already on the shelf
  SHELF.forEach(({ x, yaw, meta }) => {
    const b = makeBox(meta);
    b.position.set(x, -100 + BOX.h / 2, -10);
    b.rotation.y = yaw * DEG;
    room.add(b);
    contactShadow(x, yaw, 0.55);
  });
  const slotLocal = new THREE.Vector3(0, -100 + BOX.h / 2, -10);
  const slotShadow = contactShadow(0, CFG.yaw, 0);

  // Invisible stand-in for the falling box: only casts its shadow into the room
  const ghostRig = new THREE.Group();
  const ghost = new THREE.Mesh(boxGeometry(BOX), new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false }));
  ghost.castShadow = true;
  ghostRig.add(ghost);
  roomScene.add(ghostRig);

  /* ==========================================================
     2. The overlay (falling box, balloons, promo box)
     ========================================================== */
  const zoneR = makeRenderer(zoneCanvas);
  const zoneScene = new THREE.Scene();
  zoneScene.environment = makeEnvironment(zoneR);
  const zoneCam = new THREE.OrthographicCamera(0, 1, 0, -1, -4000, 4000);
  const zoneKey = keyLight(1.35);
  zoneKey.position.copy(KEY_DIR).multiplyScalar(1000);
  zoneScene.add(zoneKey);

  const rig = new THREE.Group();
  const flyBox = makeBox(SAVANNAH);
  const balloons = makeBalloons();
  rig.add(flyBox, balloons);
  zoneScene.add(rig);

  const promoBox = makeBox(SAVANNAH);
  zoneScene.add(promoBox);

  /* ==========================================================
     Layout + per-frame update
     ========================================================== */
  let zoneRect = null;
  const rel = (el) => {
    const r = el.getBoundingClientRect();
    return { x: r.left - zoneRect.left, y: r.top - zoneRect.top, w: r.width, h: r.height };
  };

  // The overlay canvas reaches PAD px above the zone so balloons can float
  // past the top of the sky card onto the page (the sticky menu sits above it).
  const PAD = 160;
  function resize() {
    const w = zone.clientWidth, h = zone.offsetHeight;
    zoneR.setSize(w, h + PAD, true);
    zoneCanvas.style.top = -PAD + "px";
    zoneCam.right = w; zoneCam.top = PAD; zoneCam.bottom = -h; zoneCam.updateProjectionMatrix();
    roomR.setSize(sceneCanvas.clientWidth, sceneCanvas.clientHeight, false);
    roomDirty = true;
  }

  let p = null, roomDirty = true, lastP = -1;
  const slotWorld = new THREE.Vector3();

  function frame(now, snap) {
    const t = now / 1000;
    zoneRect = zone.getBoundingClientRect();
    const sc = rel(sceneCanvas);
    const k = DESIGN_W / sc.w;                       // scene units per CSS pixel

    // Where the Savannah slot lands on screen (zone pixels)
    room.updateMatrixWorld();
    slotWorld.copy(slotLocal).applyMatrix4(room.matrixWorld);
    const slot = { x: sc.x + slotWorld.x / k, y: sc.y - slotWorld.y / k, s: 1 / k };
    const a = rel(anchor);
    const start = { x: a.x + a.w / 2, y: a.y + a.h / 2, s: a.w / BOX.w };

    // Scroll progress: 0 at the top, 1 when the slot sits CFG.endAt down the screen
    let target = 1;
    if (!reduce) {
      const end = zoneRect.top + window.scrollY + slot.y - innerHeight * CFG.endAt;
      target = clamp(window.scrollY / Math.max(1, end));
    }
    if (p === null || snap || reduce) p = target;
    else { p += (target - p) * CFG.follow; if (Math.abs(target - p) < 0.0003) p = target; }

    const e = easeInOut(p), ex = easeOut(clamp(p * 1.15)), loose = 1 - e;
    const bob = reduce ? 0 : Math.sin(t * CFG.floatSpeed * 2) * CFG.float * loose;
    const roll = (reduce ? 0 : Math.sin(t * 1.3) * 2.2) * loose + Math.sin(p * Math.PI * 2.5) * CFG.roll * loose;
    const yaw = lerp(-14, CFG.yaw, e) + Math.sin(p * Math.PI * 2) * CFG.spin * loose;
    const pitch = lerp(CFG.pitchStart, ROOM_PITCH, e);

    rig.position.set(lerp(start.x, slot.x, ex), -(lerp(start.y + bob, slot.y, e)), 200);
    rig.scale.setScalar(lerp(start.s, slot.s, e));
    rig.rotation.z = -roll * DEG;
    flyBox.rotation.set(pitch * DEG, yaw * DEG, 0);

    const release = reduce ? 1 : clamp((p - CFG.releaseStart) / CFG.releaseLen);
    balloons.position.y = release * 1100;
    balloons.rotation.z = (Math.sin(t * 0.9) * 3 + roll * 0.4) * -DEG * (1 - release);
    balloons.visible = release < 1;
    balloons.userData.mats.forEach((m) => { m.opacity = 1 - release * release; });

    // Promo card box: turns slowly, a little faster when you scroll
    const pa = rel(promoAnchor);
    promoBox.position.set(pa.x + pa.w / 2, -(pa.y + pa.h / 2) + (reduce ? 0 : Math.sin(t * 1.4) * 4), 0);
    promoBox.scale.setScalar(Math.min(pa.w, pa.h * 1.3) / (BOX.w * (innerWidth < 900 ? 1.6 : 1.12)));
    promoBox.rotation.set(16 * DEG, (-30 + (reduce ? 0 : t * 12) + window.scrollY * 0.12) * DEG, 0);

    zoneR.render(zoneScene, zoneCam);

    // Room: the falling box's shadow, and the contact shadow as it lands
    if (p !== lastP || roomDirty) {
      ghostRig.position.set((rig.position.x - sc.x) * k, (rig.position.y + sc.y) * k, slotWorld.z);
      ghostRig.scale.setScalar(rig.scale.x * k);
      ghostRig.rotation.z = rig.rotation.z;
      ghost.rotation.copy(flyBox.rotation);
      ghostRig.visible = p > 0.05;
      slotShadow.material.opacity = CFG.contactShadow * smooth(0.7, 1, e);
      slotShadow.rotation.z = CFG.yaw * DEG;
      roomR.render(roomScene, roomCam);
      lastP = p; roomDirty = false;
    }
  }

  function loop(now) {
    const r = zone.getBoundingClientRect();
    if (r.bottom > -100 && r.top < innerHeight + 100) frame(now, false);
    requestAnimationFrame(loop);
  }

  /* ==========================================================
     Product photos for the grid (rendered once, then the
     temporary renderer is thrown away)
     ========================================================== */
  function renderProducts() {
    const imgs = document.querySelectorAll("img[data-shot]");
    if (!imgs.length) return;
    const W = 960, H = 800;
    const c = document.createElement("canvas"); c.width = W; c.height = H;
    const r = makeRenderer(c, { preserveDrawingBuffer: true });
    r.setPixelRatio(1); r.setSize(W, H, false);
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
    const s = new THREE.Scene();
    s.environment = makeEnvironment(r);
    const cam = new THREE.PerspectiveCamera(26, W / H, 10, 5000);
    cam.position.set(0, 210, 820); cam.lookAt(0, 58, 0);
    const key = keyLight(1.3);
    key.position.copy(KEY_DIR).multiplyScalar(900); key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -400, right: 400, top: 400, bottom: -400, near: 10, far: 3000 });
    key.shadow.bias = -0.0005; key.shadow.radius = 6;
    s.add(key);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.ShadowMaterial({ opacity: 0.16 }));
    ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; s.add(ground);
    const blob = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, opacity: 0.5, depthWrite: false }));
    blob.rotation.x = -Math.PI / 2; blob.position.y = 0.5; s.add(blob);

    const shots = {};
    const shoot = (dims, yaw, extra) => {
      const b = makeBox(SAVANNAH, dims);
      b.position.y = dims.h / 2; b.rotation.y = yaw * DEG; s.add(b);
      const dist = 4.1 * Math.max(dims.w, dims.d);           // every box fills its photo the same way
      cam.position.set(0, dist * 0.3, dist); cam.lookAt(0, dims.h * 0.42, 0);
      blob.scale.set(dims.w * 1.25, dims.d * 1.25, 1); blob.rotation.z = yaw * DEG;
      if (extra) extra.forEach((o) => s.add(o));
      r.render(s, cam);
      const url = c.toDataURL("image/png");
      s.remove(b); if (extra) extra.forEach((o) => s.remove(o));
      return url;
    };
    Object.entries(PLANS).forEach(([name, dims]) => {
      shots[name] = shoot(dims, -30);
      shots[`${name}-b`] = shoot(dims, 52);
    });
    // A small stack of three boxes, for the tiles
    const a = makeBox(SAVANNAH, PLANS.grandtour); a.position.set(-40, PLANS.grandtour.h / 2, 0); a.rotation.y = -20 * DEG;
    const b2 = makeBox(SHELF[1].meta, PLANS.neighborhood); b2.position.set(-30, PLANS.grandtour.h + BOX.h / 2, 6); b2.rotation.y = -36 * DEG;
    const c3 = makeBox(SHELF[0].meta, PLANS.postcard); c3.position.set(150, PLANS.postcard.h / 2, 40); c3.rotation.y = -48 * DEG;
    blob.scale.set(420, 220, 1); blob.rotation.z = 0;
    [a, b2, c3].forEach((o) => s.add(o));
    cam.position.set(0, 260, 980); cam.lookAt(10, 110, 0);
    r.render(s, cam);
    shots.stack = c.toDataURL("image/png");

    [a, b2, c3].forEach((o) => s.remove(o));

    // One box per route city (home page carousel), each with that city's sticker
    imgs.forEach((img) => {
      if (img.dataset.shot !== "city") return;
      const d = img.dataset, key = `city-${d.num}`;
      if (!shots[key]) {
        const box = makeBox({ city: d.city, state: d.state, num: d.num, accent: d.accent, ink: d.ink || C.navy }, BOX);
        box.position.y = BOX.h / 2; box.rotation.y = -36 * DEG; s.add(box);
        blob.scale.set(BOX.w * 1.25, BOX.d * 1.25, 1); blob.rotation.z = -36 * DEG;
        const dist = 3.1 * BOX.w; cam.position.set(0, dist * 0.3, dist); cam.lookAt(0, BOX.h * 0.42, 0);
        r.render(s, cam); shots[key] = c.toDataURL("image/png"); s.remove(box);
      }
      img.src = shots[key];
    });
    imgs.forEach((img) => { if (shots[img.dataset.shot]) img.src = shots[img.dataset.shot]; });
    r.dispose(); r.forceContextLoss();
  }

  /* ==========================================================
     Live tuning panel (open the page with ?tune)
     ========================================================== */
  function tunePanel() {
    const ranges = {
      follow: [0.02, 0.4, 0.01], endAt: [0.3, 0.8, 0.01], releaseStart: [0, 0.6, 0.01], releaseLen: [0.1, 0.8, 0.01],
      spin: [0, 90, 1], roll: [0, 25, 1], float: [0, 20, 1], floatSpeed: [0.2, 3, 0.1],
      pitchStart: [0, 30, 1], yaw: [-45, 0, 1], contactShadow: [0, 1, 0.05],
    };
    const el = document.createElement("div");
    el.className = "tune";
    el.innerHTML = "<h4>Box drop — motion values</h4>" + Object.entries(ranges).map(([k, [min, max, step]]) =>
      `<label><span>${k}</span><input type="range" name="${k}" min="${min}" max="${max}" step="${step}" value="${CFG[k]}"><output>${CFG[k]}</output></label>`
    ).join("") + '<button type="button" data-copy>Copy values as JSON</button><button type="button" data-reset style="background:#fff;margin-top:6px">Reset</button>';
    document.body.appendChild(el);
    el.addEventListener("input", (ev) => {
      const i = ev.target; if (!i.name) return;
      CFG[i.name] = Number(i.value); i.nextElementSibling.value = i.value;
      roomDirty = true;
      try { localStorage.setItem("marlowby-tune", JSON.stringify(CFG)); } catch (e) {}
    });
    el.querySelector("[data-copy]").addEventListener("click", (ev) => {
      const json = JSON.stringify(CFG, null, 2);
      (navigator.clipboard ? navigator.clipboard.writeText(json) : Promise.reject()).then(
        () => { ev.target.textContent = "Copied!"; }, () => { prompt("Copy these values:", json); });
      setTimeout(() => { ev.target.textContent = "Copy values as JSON"; }, 1500);
    });
    el.querySelector("[data-reset]").addEventListener("click", () => {
      try { localStorage.removeItem("marlowby-tune"); } catch (e) {}
      location.reload();
    });
  }

  /* ---------- Go ---------- */
  new ResizeObserver(resize).observe(zone);
  resize();
  root.classList.add("gl-on");
  frame(performance.now(), true);
  requestAnimationFrame(loop);
  (window.requestIdleCallback || ((f) => setTimeout(f, 300)))(renderProducts);
  if (tuneMode) tunePanel();

  // Testing hook: render the current scroll position immediately.
  window.marlowbySnap = () => { roomDirty = true; frame(performance.now(), true); };
  } // end start()
})();
