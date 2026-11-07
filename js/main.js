/* Marlowby — shared site scripts (no libraries, works without a server) */
(function () {
  document.documentElement.classList.remove("no-js");

  /* ---------- Mobile navigation ---------- */
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.documentElement.classList.toggle("menu-open", open);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && links.classList.contains("open")) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        document.documentElement.classList.remove("menu-open");
        toggle.focus();
      }
    });
  }

  /* ---------- Launch countdown (home banner) ---------- */
  const cd = document.getElementById("countdown");
  if (cd) {
    const launch = new Date(cd.dataset.launch);
    const tick = () => {
      const diff = launch - new Date();
      if (diff <= 0) { cd.textContent = "We're live!"; return; }
      const d = Math.floor(diff / 864e5);
      const h = Math.floor((diff % 864e5) / 36e5);
      const m = Math.floor((diff % 36e5) / 6e4);
      cd.textContent = `${d}d ${h}h ${m}m`;
    };
    tick(); setInterval(tick, 30000);
  }

  /* ---------- Newsletter (footer) ---------- */
  document.querySelectorAll("form.newsletter").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = form.querySelector("input[type=email]");
      const msg = form.parentElement.querySelector(".form-msg");
      if (!input.checkValidity() || !input.value) {
        msg.textContent = "Please enter a valid email address.";
        input.focus();
        return;
      }
      msg.textContent = "You're on the list! Watch your inbox for our launch postcard.";
      form.reset();
    });
  });

  /* ---------- Pricing: monthly / annual toggle ---------- */
  const billingBtns = document.querySelectorAll("[data-billing]");
  if (billingBtns.length) {
    const setBilling = (mode) => {
      billingBtns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.billing === mode)));
      document.querySelectorAll(".plan").forEach((plan) => {
        const monthly = Number(plan.dataset.monthly);
        const amt = plan.querySelector(".amount");
        const note = plan.querySelector(".price-note");
        if (mode === "annual") {
          const perMonth = Math.round(monthly * 0.85);
          amt.textContent = "$" + perMonth;
          note.textContent = `Billed $${perMonth * 12} yearly, you save $${(monthly - perMonth) * 12}`;
        } else {
          amt.textContent = "$" + monthly;
          note.textContent = "Billed monthly · skip or cancel anytime";
        }
      });
    };
    billingBtns.forEach((b) => b.addEventListener("click", () => setBilling(b.dataset.billing)));
    setBilling("monthly");
  }

  /* ---------- Plan quiz (plans page) ---------- */
  const quiz = document.getElementById("plan-quiz");
  if (quiz) {
    quiz.addEventListener("change", () => {
      const data = new FormData(quiz);
      if (!data.get("who") || !data.get("how")) return;
      let score = 0;
      score += { me: 0, two: 1, family: 2 }[data.get("who")];
      score += { taste: 0, explore: 1, deep: 2 }[data.get("how")];
      const plan = score <= 1 ? "Postcard" : score <= 3 ? "Neighborhood" : "Grand Tour";
      const out = document.getElementById("quiz-result");
      out.innerHTML = `We recommend <strong>The ${plan}</strong>. <a href="join.html?plan=${encodeURIComponent(plan)}">Start with this plan →</a>`;
    });
  }

  /* ---------- Cities map ---------- */
  const map = document.querySelector(".us-map");
  if (map) {
    const detail = document.getElementById("map-detail");
    const pins = map.querySelectorAll(".pin");
    const show = (pin) => {
      pins.forEach((p) => p.classList.remove("active"));
      pin.classList.add("active");
      detail.querySelector(".m-mo").textContent = pin.dataset.month;
      detail.querySelector(".m-yr").textContent = pin.dataset.year;
      detail.querySelector("h3").textContent = pin.dataset.city;
      detail.querySelector("p").textContent = pin.dataset.desc;
      detail.querySelectorAll("img[data-key]").forEach((img) => { img.hidden = img.dataset.key !== pin.dataset.key; });
    };
    pins.forEach((pin) => {
      pin.addEventListener("click", () => show(pin));
      pin.addEventListener("focus", () => show(pin));
      pin.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(pin); } });
    });
  }

  /* ---------- Vote for the next city ---------- */
  const voteList = document.querySelector(".vote-list");
  if (voteList) {
    const items = [...voteList.querySelectorAll(".vote-item")];
    let voted = null;
    try { voted = localStorage.getItem("marlowby-vote"); } catch (e) {}
    const render = () => {
      const totals = items.map((it) => Number(it.dataset.votes) + (it.dataset.city === voted ? 1 : 0));
      const sum = totals.reduce((a, b) => a + b, 0);
      items.forEach((it, i) => {
        const pct = Math.round((totals[i] / sum) * 100);
        it.querySelector(".vote-bar span").style.width = pct + "%";
        it.querySelector(".pct").textContent = pct + "%";
        const btn = it.querySelector("button");
        const mine = it.dataset.city === voted;
        btn.setAttribute("aria-pressed", String(mine));
        btn.textContent = mine ? "Voted ✓" : "Vote";
      });
    };
    const status = document.getElementById("vote-status");
    items.forEach((it) => it.querySelector("button").addEventListener("click", () => {
      voted = voted === it.dataset.city ? null : it.dataset.city;
      try { voted ? localStorage.setItem("marlowby-vote", voted) : localStorage.removeItem("marlowby-vote"); } catch (e) {}
      render();
      if (status) status.textContent = voted
        ? `Voted for ${voted}. It now has ${it.querySelector(".pct").textContent}.`
        : `Vote for ${it.dataset.city} removed.`;
    }));
    render();
  }

  /* ---------- FAQ filter + search ---------- */
  const faq = document.querySelector(".faq");
  if (faq) {
    const search = document.getElementById("faq-search");
    const filterBtns = document.querySelectorAll(".faq-filters button");
    const empty = document.querySelector(".faq-empty");
    const count = document.getElementById("faq-count");
    let cat = "all";
    const apply = () => {
      const q = search.value.trim().toLowerCase();
      let shown = 0;
      faq.querySelectorAll("details").forEach((d) => {
        const matchCat = cat === "all" || d.dataset.cat === cat;
        const matchQ = !q || d.textContent.toLowerCase().includes(q);
        const ok = matchCat && matchQ;
        d.hidden = !ok;
        if (ok) shown++;
      });
      empty.style.display = shown ? "none" : "block";
      if (count) count.textContent = shown
        ? `${shown} ${shown === 1 ? "answer" : "answers"} shown`
        : "No answers match";
    };
    filterBtns.forEach((b) => b.addEventListener("click", () => {
      cat = b.dataset.cat;
      filterBtns.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      apply();
    }));
    search.addEventListener("input", apply);
  }

  /* ---------- Join: multi-step sign-up ---------- */
  const join = document.getElementById("join-form");
  if (join) {
    const PRICES = { Postcard: 29, Neighborhood: 49, "Grand Tour": 79 };
    const steps = [...join.querySelectorAll(".form-step")];
    const progress = [...document.querySelectorAll(".form-progress li")];
    let current = 0;

    // Pre-select plan from URL (?plan=Neighborhood)
    const params = new URLSearchParams(location.search);
    const pre = params.get("plan");
    if (pre) {
      const radio = join.querySelector(`input[name=plan][value="${CSS.escape(pre)}"]`);
      if (radio) radio.checked = true;
    }
    const gift = params.get("gift");
    if (gift) { const g = join.querySelector("#gift"); if (g) g.checked = true; }

    const go = (n) => {
      steps[current].classList.remove("active");
      current = n;
      steps[current].classList.add("active");
      progress.forEach((li, i) => {
        li.classList.toggle("done", i < current);
        li.classList.toggle("current", i === current);
        if (i === current) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
      });
      if (current === steps.length - 1) buildSummary();
      const h = steps[current].querySelector("h2");
      if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
    };

    const validate = (step) => {
      let ok = true;
      step.querySelectorAll(".field[data-required]").forEach((f) => {
        const input = f.querySelector("input, select");
        let valid;
        if (input.type === "radio") valid = !!step.querySelector(`input[name=${input.name}]:checked`);
        else valid = input.value.trim() !== "" && input.checkValidity();
        f.classList.toggle("invalid", !valid);
        (input.type === "radio" ? [...step.querySelectorAll(`input[name=${input.name}]`)] : [input])
          .forEach((el) => el.setAttribute("aria-invalid", String(!valid)));
        if (!valid && ok) { input.focus(); ok = false; }
      });
      return ok;
    };

    const buildSummary = () => {
      const d = new FormData(join);
      const plan = d.get("plan");
      const billing = d.get("billing");
      const base = PRICES[plan];
      const monthly = billing === "annual" ? Math.round(base * 0.85) : base;
      const interests = d.getAll("interests");
      const box = document.getElementById("summary");
      box.innerHTML = `
        <dl>
          <dt>Plan</dt><dd>The ${plan}</dd>
          <dt>Billing</dt><dd>${billing === "annual" ? "Annual (15% off)" : "Monthly"}</dd>
          <dt>Ship to</dt><dd>${escapeHTML(d.get("name"))}, ${escapeHTML(d.get("city"))}, ${escapeHTML(d.get("state"))}</dd>
          <dt>Interests</dt><dd>${interests.length ? interests.map(escapeHTML).join(", ") : "Surprise me!"}</dd>
          ${d.get("gift") ? "<dt>Gift</dt><dd>Yes, with a gift note</dd>" : ""}
        </dl>
        <div class="summary-total"><span>First box</span><span>$${monthly}${billing === "annual" ? "/mo" : ""}</span></div>
        <p class="note-small" style="margin:8px 0 0">Free shipping in the contiguous U.S. First box ships the 1st of next month.</p>`;
    };

    join.addEventListener("click", (e) => {
      if (e.target.matches("[data-next]")) { if (validate(steps[current])) go(current + 1); }
      if (e.target.matches("[data-prev]")) go(current - 1);
    });
    join.addEventListener("input", (e) => {
      const f = e.target.closest(".field.invalid");
      if (!f) return;
      f.classList.remove("invalid");
      f.querySelectorAll("[aria-invalid]").forEach((el) => el.setAttribute("aria-invalid", "false"));
    });
    join.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validate(steps[current])) return;
      document.getElementById("join-wrap").hidden = true;
      const s = document.getElementById("join-success");
      s.hidden = false;
      s.querySelector(".success-name").textContent = new FormData(join).get("name").split(" ")[0];
      s.querySelector("h2").focus();
    });
  }

  function escapeHTML(s) {
    return String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
})();

/* ==========================================================
   Motion: smooth scrolling (Lenis) + scroll reveals (GSAP)
   Everything is visible without this; it only adds movement.
   Turned off for people who ask their device for reduced motion.
   ========================================================== */
(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);

  if (window.Lenis) {
    const lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.9 });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target && a.getAttribute("href").length > 1) { e.preventDefault(); lenis.scrollTo(target, { offset: -90 }); }
    }));
    window.marlowbyLenis = lenis;
  }

  // Headings marked up as lines slide up one line at a time
  document.querySelectorAll("[data-lines]").forEach((el) => {
    gsap.from(el.querySelectorAll(".line > span"), {
      yPercent: 110, duration: 1.05, ease: "power4.out", stagger: 0.09,
      scrollTrigger: { trigger: el, start: "top 88%", once: true },
    });
  });

  // Blocks fade up; siblings inside [data-rise-group] go one after another
  document.querySelectorAll("[data-rise-group]").forEach((group) => {
    gsap.from(group.children, {
      y: 48, opacity: 0, duration: 1, ease: "power3.out", stagger: 0.1,
      scrollTrigger: { trigger: group, start: "top 86%", once: true },
    });
  });
  document.querySelectorAll("[data-rise]").forEach((el) => {
    gsap.from(el, { y: 48, opacity: 0, duration: 1, ease: "power3.out",
      scrollTrigger: { trigger: el, start: "top 88%", once: true } });
  });

  // Parallax: data-parallax="-12" moves the element 12% of its height while its section scrolls past
  document.querySelectorAll("[data-parallax]").forEach((el) => {
    gsap.to(el, { yPercent: Number(el.dataset.parallax), ease: "none",
      scrollTrigger: { trigger: el.closest("section") || el, start: "top top", end: "bottom top", scrub: true } });
  });
})();

/* ==========================================================
   Shop-style details: shrinking menu bar, city word in the hero,
   route carousel. All work without the motion libraries.
   ========================================================== */
(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Menu bar tightens once you start scrolling
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 60);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Hero: the city name cycles through the 2027 route
  const rot = document.querySelector(".rotator");
  if (rot && !reduce) {
    const words = [...rot.querySelectorAll(".rot-word")];
    let i = 0;
    setInterval(() => {
      if (document.hidden) return;
      const prev = words[i];
      i = (i + 1) % words.length;
      words.forEach((w) => w.classList.remove("was-on"));
      prev.classList.replace("is-on", "was-on");
      words[i].classList.add("is-on");
    }, 2200);
  }

  // Route carousel: arrows, progress line, and "+" buttons that open each card
  document.querySelectorAll("[data-carousel]").forEach((wrap) => {
    const track = wrap.querySelector(".route-track");
    const bar = wrap.querySelector(".route-progress span");
    const [prev, next] = wrap.querySelectorAll(".route-arrows button");
    const step = () => (track.querySelector(".route-card")?.offsetWidth || 300) + 20;
    const update = () => {
      const max = track.scrollWidth - track.clientWidth;
      const pct = max > 0 ? track.scrollLeft / max : 1;
      bar.style.width = `${Math.max(12, (track.clientWidth / track.scrollWidth) * 100 + pct * (100 - (track.clientWidth / track.scrollWidth) * 100))}%`;
      prev.disabled = track.scrollLeft < 4;
      next.disabled = track.scrollLeft > max - 4;
    };
    prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: reduce ? "auto" : "smooth" }));
    next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: reduce ? "auto" : "smooth" }));
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
    track.querySelectorAll(".r-plus").forEach((b) => b.addEventListener("click", () => {
      const card = b.closest(".route-card");
      const open = card.classList.toggle("open");
      b.setAttribute("aria-expanded", String(open));
    }));
  });
})();
