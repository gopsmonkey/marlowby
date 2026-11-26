/* Marlowby skylines: what rises out of each month's box.
   Each city is drawn from the landmarks it is known for, using the kit that
   js/scene.js passes in (K). Base of the skyline is y = 0; everything must stay
   inside the carton's footprint (x within about +-112) and below the logo's
   sparks (y < 240). Keys match the route in tools/build.py. */
window.MarlowbySkylines = {

  /* Savannah: a live oak, the twin spires of the Cathedral of St. John the
     Baptist, City Hall's gilded dome, rowhouses on the squares. */
  sav(K) {
    const { M } = K;
    const liveOak = (x, s) => {
      K.add(K.box(10 * s, 86 * s, 10 * s, M.TRUNK), x, 43 * s, 6);
      [[0, 104, 34], [-26, 94, 26], [27, 96, 27], [3, 122, 23]].forEach(([dx, dy, r]) => {
        K.add(K.sphere(Math.round(r * s), M.LEAF), x + dx * s, dy * s, 6).scale.y = 0.66;
      });
    };
    liveOak(-96, 0.8);
    // cathedral
    K.add(K.box(54, 82, 40, M.STONE), -48, 41);
    [-17, 17].forEach((dx) => {
      K.add(K.box(19, 150, 19, M.STONE), -48 + dx, 75, 2);
      K.add(K.cone(13, 54, M.DEEP), -48 + dx, 177, 2).rotation.y = Math.PI / 4;
      K.add(K.box(2.6, 15, 2.6, M.INK), -48 + dx, 211, 2);
      K.add(K.box(9, 2.6, 2.6, M.INK), -48 + dx, 207, 2);
    });
    K.add(K.box(16, 18, 2, M.INK), -48, 62, 20.5);
    // City Hall
    K.add(K.box(58, 62, 46, M.STONE), 10, 31);
    K.add(K.box(40, 20, 40, M.STONE), 10, 72);
    K.add(K.cyl(19, 19, 26, M.STONE), 10, 95);
    K.add(K.dome(19, M.GOLD), 10, 108);
    K.add(K.box(3, 20, 3, M.GOLD), 10, 128);
    // rowhouses
    [[0, 30, 56], [32, 26, 48], [60, 30, 64], [92, 24, 44]].forEach(([dx, w, h], i) => {
      K.add(K.box(w, h, 34, i % 2 ? M.BRICK : M.DEEP), 48 + dx, h / 2, -4);
      K.windows(48 + dx, w, h, 13.2);
    });
    liveOak(100, 0.66);
  },

  /* Santa Fe: the Sangre de Cristo range behind, the Cathedral Basilica of
     St. Francis with its flat-topped towers, and stepped adobe with vigas. */
  sf(K) {
    const { M } = K;
    const ridge = K.mat("#8EA8DD", 0.95);
    K.mountain(-56, 230, 120, -66, ridge, 7);
    K.mountain(64, 230, 100, -70, K.mat("#A6BBE5", 0.95), 7);
    // Cathedral Basilica of St. Francis: towers that were never given spires
    const A = K.mat("#DDB48C", 0.92), CLAY = K.mat("#C9845C", 0.9);
    K.add(K.box(66, 84, 40, A), -4, 42, 2);
    [-30, 22].forEach((dx) => {
      K.add(K.box(24, 140, 24, A), dx, 70, 6);
      K.add(K.box(27, 6, 27, CLAY), dx, 142, 6);
      [104, 74].forEach((y) => K.add(K.box(8, 16, 1.6, M.INK), dx, y, 18.6));      // belfry openings
    });
    K.add(K.cyl(10, 10, 2, M.INK, 20), -4, 70, 22.6).rotation.x = Math.PI / 2;  // rose window
    K.add(K.box(16, 30, 1.6, M.INK), -4, 15, 22.6);
    // stepped adobe with viga beams, and red chile ristras by the doors
    const adobe = (x, w, h, z) => {
      K.add(K.box(w, h, 34, A), x, h / 2, z);
      for (let vx = x - w / 2 + 6; vx < x + w / 2 - 3; vx += 9) K.add(K.cyl(2, 2, 10, CLAY, 8), vx, h - 6, z + 19).rotation.x = Math.PI / 2;
      K.add(K.box(10, 18, 1.6, M.NAVY), x - w / 5, 9, z + 17.5);
    };
    const ristra = (x, y, z) => { for (let i = 0; i < 6; i++) K.add(K.sphere(3, K.mat("#C2453A", 0.6), 8), x + (i % 2) * 2, y - i * 5, z); };
    adobe(-88, 44, 56, 12); adobe(-90, 26, 82, -6); ristra(-74, 50, 31);
    adobe(68, 46, 62, 10);  adobe(96, 30, 40, 20);  adobe(72, 26, 92, -10); ristra(52, 56, 29);
  },

  /* Detroit: the Renaissance Center (one tall glass cylinder ringed by four)
     and the stepped Guardian Building in its orange brick. */
  det(K) {
    const { M } = K;
    K.add(K.cyl(22, 22, 214, M.GLASS, 32), 34, 107, -10);
    [[-26, -26], [26, -26], [-26, 26], [26, 26]].forEach(([dx, dz]) => K.add(K.cyl(12, 12, 150, M.DEEP, 24), 34 + dx * 0.95, 75, -10 + dz * 0.7));
    K.add(K.cyl(23, 23, 6, M.INK, 32), 34, 214, -10);
    // Guardian Building
    const G = K.mat("#E39B57", 0.8);
    K.add(K.box(40, 120, 34, G), -54, 60, 6);
    K.add(K.box(28, 30, 24, G), -54, 135, 6);
    K.add(K.box(18, 22, 16, G), -54, 161, 6);
    K.add(K.cone(10, 18, M.GOLD), -54, 181, 6).rotation.y = Math.PI / 4;
    K.windows(-54, 40, 120, 23.2, { step: 18 });
    // riverfront blocks
    K.add(K.box(34, 54, 30, M.BRICK), -96, 27, 18); K.windows(-96, 34, 54, 33.2);
    K.add(K.box(30, 40, 30, M.STONE), 96, 20, 22); K.windows(96, 30, 40, 37.2);
  },

  /* Portland, Maine: Portland Head Light on its rocks, the keeper's house, and
     brick warehouses on the Old Port waterfront. */
  pme(K) {
    const { M } = K;
    [[-78, 18, 16], [-56, 12, 20], [-96, 10, 26]].forEach(([x, r, z]) => K.add(K.sphere(r, M.ROCK, 10), x, 2, z).scale.y = 0.6);
    K.add(K.cyl(10, 15, 150, M.WHITE, 24), -76, 75, 4);                  // tower
    K.add(K.cyl(17, 17, 4, M.INK, 24), -76, 152, 4);                      // gallery
    K.add(K.cyl(9, 9, 16, M.GOLD, 16), -76, 162, 4);                      // lantern
    K.add(K.cone(11, 16, M.INK, 16), -76, 178, 4);
    K.add(K.box(3, 12, 3, M.INK), -76, 190, 4);
    K.gable(-30, 42, 58, 30, M.WHITE, M.NAVY, 10);                     // keeper's house (tall enough to clear the carton lip)
    [[-38, 40], [-22, 40], [-38, 22], [-22, 22]].forEach(([x, y]) => K.add(K.box(8, 12, 1.6, M.INK), x, y, 25.6));
    [[26, 34, 70], [60, 30, 54], [92, 30, 80]].forEach(([x, w, h], i) => {    // Old Port
      K.add(K.box(w, h, 34, i % 2 ? M.BRICK : K.mat("#B8836E", 0.85)), x, h / 2, -2);
      K.windows(x, w, h, 15.2);
    });
  },

  /* Asheville: layered Blue Ridge ridgelines (they really are blue), the
     Gothic-topped Jackson Building, and the dome of the Basilica of St. Lawrence. */
  ash(K) {
    const { M } = K;
    // three Blue Ridge ridgelines, lighter as they recede, kept low behind the town
    K.mountain(-70, 230, 116, -76, K.mat("#A3BCE8", 0.95), 7);
    K.mountain(54, 250, 100, -66, K.mat("#7E9FDC", 0.95), 7);
    K.mountain(-8, 280, 66, -52, K.mat("#5F86D2", 0.95), 8);
    // Jackson Building, Gothic top and corner pinnacles
    K.add(K.box(30, 168, 28, M.STONE), -42, 84, 8); K.windows(-42, 30, 168, 22.2, { step: 18 });
    K.add(K.cone(19, 44, M.NAVY), -42, 190, 8).rotation.y = Math.PI / 4;
    [[-15, -14], [15, -14], [-15, 14], [15, 14]].forEach(([dx, dz]) => K.add(K.cone(3.5, 20, M.NAVY, 4), -42 + dx, 178, 8 + dz));
    // Basilica of St. Lawrence: buff brick and a tiled dome
    const B = K.mat("#D7AE84", 0.9);
    K.add(K.box(66, 58, 44, B), 42, 29, 12);
    K.add(K.box(14, 24, 1.6, M.INK), 42, 12, 34.6);
    [26, 58].forEach((x) => K.add(K.box(8, 14, 1.6, M.INK), x, 36, 34.6));
    K.add(K.cyl(24, 24, 16, B), 42, 66, 12);
    K.add(K.dome(25, M.DEEP), 42, 74, 12);
    K.add(K.cyl(5, 5, 10, B, 12), 42, 103, 12); K.add(K.box(3, 18, 3, M.GOLD), 42, 116, 12);
    K.pine(-94, 1.05, 22); K.pine(98, 1.0, 24);
  },

  /* Tucson: the Santa Catalina Mountains, the white Mission San Xavier del Bac
     (whose east tower famously has no dome), and saguaros. */
  tuc(K) {
    const { M } = K;
    // the Santa Catalinas, kept low and broad behind the mission
    K.mountain(-64, 210, 104, -74, K.mat("#A99CD3", 0.95), 8);
    K.mountain(30, 240, 126, -78, K.mat("#8E82C4", 0.95), 8);
    K.mountain(96, 180, 84, -68, K.mat("#B6AADA", 0.95), 8);
    // Mission San Xavier del Bac: two towers, the east one never finished
    const W = M.STONE, P = K.mat("#D6A36A", 0.85);
    K.add(K.box(74, 66, 44, W), 4, 33, 4);
    K.add(K.box(24, 128, 24, W), -34, 64, 8);
    K.add(K.box(24, 112, 24, W), 42, 56, 8);
    K.add(K.cyl(10, 10, 16, W), -34, 136, 8); K.add(K.dome(10, W), -34, 144, 8);
    K.add(K.box(3, 14, 3, M.INK), -34, 160, 8);
    [[-34, 108], [-34, 82], [42, 92]].forEach(([x, y]) => K.add(K.box(9, 16, 1.6, M.INK), x, y, 20.6));   // bell arches
    K.add(K.dome(22, W), 4, 66, -2);
    K.add(K.box(22, 40, 1.6, P), 4, 34, 26.6);                                   // carved portal
    K.add(K.box(10, 20, 1.6, M.INK), 4, 10, 27.2);
    // saguaros, the Sonoran Desert's signature
    const G = K.mat("#5E8FB5", 0.85);
    const saguaro = (x, s, z) => {
      K.add(K.cyl(7 * s, 7.5 * s, 112 * s, G, 12), x, 56 * s, z);
      K.add(K.sphere(Math.round(7 * s), G, 12), x, 112 * s, z);
      [[-1, 40, 34], [1, 58, 26]].forEach(([dir, y, h]) => {
        K.add(K.cyl(5 * s, 5 * s, 20 * s, G, 10), x + dir * 11 * s, y * s, z).rotation.z = dir * Math.PI / 2;
        K.add(K.cyl(5 * s, 5 * s, h * s, G, 10), x + dir * 21 * s, (y + h / 2) * s, z);
        K.add(K.sphere(Math.round(5 * s), G, 10), x + dir * 21 * s, (y + h) * s, z);
      });
    };
    saguaro(-92, 1.0, 20); saguaro(90, 0.9, 24);
  },

  /* Minneapolis: the IDS Center with its stepped "zogs", Capella Tower's
     crown, and the Foshay Tower, built as a tribute to the Washington Monument. */
  msp(K) {
    const { M } = K;
    // IDS Center: a glass slab with notched corners
    K.add(K.box(34, 212, 30, M.GLASS), 6, 106, -8);
    [[-19, -17], [19, -17], [-19, 17], [19, 17]].forEach(([dx, dz]) => K.add(K.box(8, 198, 8, M.DEEP), 6 + dx * 0.8, 99, -8 + dz * 0.8));
    // Capella Tower
    K.add(K.box(30, 176, 28, M.STONE), 58, 88, -4); K.windows(58, 30, 176, 10.2, { step: 20 });
    K.add(K.cyl(17, 17, 10, M.WHITE, 28), 58, 182, -4);
    K.add(K.cyl(15, 17, 2, M.GOLD, 28), 58, 188, -4);
    // Foshay Tower: an obelisk with a pyramid cap
    K.add(K.cyl(10, 15, 150, K.mat("#D7DCE6", 0.85), 4), -50, 75, 6).rotation.y = Math.PI / 4;
    K.add(K.cone(10.5, 18, K.mat("#D7DCE6", 0.85), 4), -50, 159, 6).rotation.y = Math.PI / 4;
    K.add(K.box(30, 8, 1.6, M.INK), -50, 132, 13);
    K.add(K.box(34, 46, 30, M.BRICK), -92, 23, 16); K.windows(-92, 34, 46, 31.2);
    K.add(K.box(28, 60, 28, M.BRICK), 98, 30, 18); K.windows(98, 28, 60, 32.2);
  },

  /* Boise: the Idaho State Capitol (heated by the city's geothermal water),
     the foothills behind it, and the pines of the Boise River greenbelt. */
  boi(K) {
    const { M } = K;
    // sagebrush foothills behind the capitol
    [[-62, 74, -66, "#9FB7E2"], [34, 96, -72, "#88A6DD"], [98, 62, -60, "#A8BEE6"]].forEach(([x, r, z, c]) => {
      K.add(K.sphere(r, K.mat(c, 0.95), 18), x, 0, z).scale.set(1.35, 0.7, 0.7);
    });
    // Idaho State Capitol: wings, portico, colonnaded drum, dome and eagle-topped lantern
    K.add(K.box(156, 52, 46, M.STONE), 0, 26, 6);
    for (let x = -66; x <= 66; x += 12) if (Math.abs(x) > 26) K.add(K.box(6, 12, 1.6, M.INK), x, 30, 29.6);
    K.add(K.box(60, 30, 50, M.STONE), 0, 67, 8);
    for (let x = -24; x <= 24; x += 8) K.add(K.cyl(2.2, 2.2, 40, M.WHITE, 10), x, 32, 34);
    K.add(K.prism([[-32, 0], [32, 0], [0, 14]], 52, M.STONE), 0, 82, 8);          // pediment
    K.add(K.cyl(27, 27, 40, M.STONE), 0, 116, 4);
    for (let a = 0; a < 14; a++) K.add(K.cyl(1.8, 1.8, 34, M.WHITE, 8), Math.cos(a / 14 * Math.PI * 2) * 28.5, 116, 4 + Math.sin(a / 14 * Math.PI * 2) * 28.5);
    K.add(K.dome(29, M.WHITE), 0, 136, 4);
    K.add(K.cyl(7, 7, 18, M.WHITE, 16), 0, 172, 4);
    K.add(K.cone(7, 12, M.GOLD, 16), 0, 187, 4);
    K.pine(-104, 1.15, 26); K.pine(104, 1.05, 28);
  },

  /* Hood River: Mount Hood under snow, the orchards of the Fruit Loop, and a
     packing-house barn. */
  hdr(K) {
    const { M } = K;
    K.mountain(0, 236, 204, -74, K.mat("#8FB0E2", 0.92), 7, 0.38);      // Mount Hood
    K.mountain(-96, 120, 66, -56, K.mat("#7397D8", 0.95), 6);
    K.mountain(98, 128, 60, -56, K.mat("#7397D8", 0.95), 6);
    K.gable(66, 48, 36, 34, M.BARN, M.WHITE, 14, 0.7);                  // packing-house barn
    K.add(K.box(16, 22, 1.6, M.WHITE), 66, 11, 31.6);
    K.add(K.box(8, 2, 1.6, M.WHITE), 66, 30, 31.6);
    const G = K.mat("#5E8FB5", 0.88);
    for (let row = 0; row < 2; row++) {                                  // orchard rows with pears
      for (let x = -98; x <= 24; x += 27) {
        const z = 18 + row * 22, s = 0.72, xx = x + row * 13;
        K.add(K.box(6 * s, 30 * s, 6 * s, M.TRUNK), xx, 15 * s, z);
        K.add(K.sphere(Math.round(17 * s), G, 14), xx, 36 * s, z);
        K.add(K.sphere(2.4, M.GOLD, 8), xx + 6, 38 * s, z + 10);
        K.add(K.sphere(2.4, M.GOLD, 8), xx - 5, 32 * s, z + 10);
      }
    }
  },

  /* Louisville: the Twin Spires of Churchill Downs over the grandstand, the
     giant bat outside the Louisville Slugger Museum, and shotgun houses. */
  lou(K) {
    const { M } = K;
    K.add(K.box(130, 40, 40, M.WHITE), -20, 20, -6);                     // grandstand
    K.add(K.box(130, 6, 44, M.DEEP), -20, 42, -6);
    [-44, 4].forEach((x) => {                                            // the twin spires
      K.add(K.box(22, 36, 22, M.WHITE), x, 63, -4);
      K.add(K.cyl(12, 12, 4, M.DEEP, 6), x, 83, -4);
      K.add(K.cone(12, 70, M.WHITE, 6), x, 120, -4);
      K.add(K.sphere(3, M.GOLD, 10), x, 157, -4);
      K.add(K.box(8, 12, 1.6, M.INK), x, 66, 7.5);
    });
    // the bat, leaning on the museum
    K.add(K.box(34, 70, 30, M.BRICK), 82, 35, -2); K.windows(82, 34, 70, 13.2);
    const bat = K.add(K.cyl(9, 4, 170, K.mat("#D9A46B", 0.7), 18), 56, 84, 18);
    bat.rotation.z = -0.2;
    K.add(K.sphere(5, K.mat("#D9A46B", 0.7), 12), 39, 0, 18);
    // shotgun houses
    [[-96, M.BRICK], [-76, M.STONE]].forEach(([x, m]) => K.gable(x, 16, 26, 40, m, M.DEEP, 24, 0.8));
  },

  /* Lancaster: a red bank barn with a quilt square, its silo, a farmhouse and
     a white church steeple. */
  lan(K) {
    const { M } = K;
    // barn: gambrel roof
    K.add(K.box(76, 46, 50, M.BARN), -36, 23, 0);
    K.add(K.prism([[-41, 0], [41, 0], [30, 22], [0, 36], [-30, 22]], 54, M.NAVY), -36, 46, 0);
    K.add(K.box(22, 22, 1.6, M.WHITE), -36, 52, 26);                     // the barn quilt
    K.add(K.box(14, 14, 1.8, M.GOLD), -36, 52, 26.4).rotation.z = Math.PI / 4;
    K.add(K.box(16, 28, 1.6, M.WHITE), -36, 14, 25.5);
    K.add(K.cyl(14, 14, 110, M.STONE, 24), 14, 55, -6);                  // silo
    K.add(K.dome(14, M.NAVY), 14, 110, -6);
    K.gable(56, 34, 40, 30, M.WHITE, M.DEEP, 12);                        // farmhouse
    K.add(K.box(8, 12, 1.6, M.INK), 48, 22, 27.5); K.add(K.box(8, 12, 1.6, M.INK), 64, 22, 27.5);
    K.add(K.box(20, 70, 20, M.WHITE), 98, 35, -10);                      // church
    K.add(K.box(14, 22, 14, M.WHITE), 98, 81, -10);
    K.add(K.cone(10, 52, M.WHITE, 8), 98, 118, -10);
    K.add(K.box(2.4, 12, 2.4, M.INK), 98, 150, -10); K.add(K.box(8, 2.4, 2.4, M.INK), 98, 152, -10);
    K.tree(-96, 0.8, 22);
  },
};
