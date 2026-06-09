// mobile menu
const navToggle = document.getElementById("nav-toggle");
const navMenu = document.getElementById("nav-menu");
if (navToggle && navMenu) {
  const setOpen = (open) => {
    navMenu.classList.toggle("open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };
  navToggle.addEventListener("click", () => setOpen(!navMenu.classList.contains("open")));
  navMenu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
}

// scroll-spy: highlight the nav link for the section in view
const navLinks = navMenu ? [...navMenu.querySelectorAll('a[href^="#"]')] : [];
const sectionFor = (id) => navLinks.find((a) => a.getAttribute("href") === "#" + id);
if (navLinks.length) {
  const spy = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        navLinks.forEach((a) => a.classList.remove("active"));
        const link = sectionFor(en.target.id);
        if (link) link.classList.add("active");
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );
  ["vans", "sell", "reviews", "faq", "about", "contact"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) spy.observe(el);
  });
}

// back to top
const toTop = document.getElementById("to-top");
if (toTop) {
  const onScroll = () => (toTop.hidden = window.scrollY < 600);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}

// scroll reveals
const io = new IntersectionObserver(
  (entries) => entries.forEach((en) => en.isIntersecting && (en.target.classList.add("in"), io.unobserve(en.target))),
  { threshold: 0.12 }
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// van detail modal
const modal = document.getElementById("van-modal");
const gallery = modal.querySelector(".modal-gallery");
const titleEl = modal.querySelector("h3");
const refEl = modal.querySelector(".modal-ref");
const statusEl = modal.querySelector(".modal-status");
const bulletsEl = modal.querySelector(".modal-bullets");
const notesEl = modal.querySelector(".modal-notes");
const specsEl = modal.querySelector(".modal-specs");

document.querySelectorAll(".van-card").forEach((card) => {
  card.addEventListener("click", () => {
    const van = JSON.parse(card.dataset.van);
    titleEl.textContent = van.title;
    refEl.textContent = van.code || "";
    notesEl.textContent = van.notes || "";
    notesEl.style.display = van.notes ? "" : "none";

    // availability banner: price + book-a-viewing for live stock; "sold" otherwise
    statusEl.replaceChildren();
    if (van.available) {
      const price = document.createElement("span");
      price.className = "modal-price";
      price.textContent = van.price || "";
      const cta = document.createElement("a");
      cta.className = "btn btn-solid";
      cta.href = "tel:+447813696011";
      cta.textContent = "Book a viewing";
      statusEl.append(price, cta);
      statusEl.classList.add("is-available");
    } else {
      const sold = document.createElement("span");
      sold.className = "modal-sold";
      sold.textContent = "Sold — gone to a new home";
      statusEl.append(sold);
      statusEl.classList.remove("is-available");
    }

    gallery.replaceChildren(
      ...van.photos.map((p, i) => {
        const img = document.createElement("img");
        img.src = p;
        img.alt = `${van.title} — photo ${i + 1}`;
        img.loading = "lazy";
        return img;
      })
    );

    bulletsEl.replaceChildren(
      ...(van.bullets || []).map((b) => {
        const li = document.createElement("li");
        li.textContent = b;
        return li;
      })
    );

    specsEl.replaceChildren(
      ...Object.entries(van.specs).map(([k, v]) => {
        const cell = document.createElement("div");
        const label = document.createElement("b");
        label.textContent = k;
        const val = document.createElement("span");
        val.textContent = v;
        cell.append(label, val);
        return cell;
      })
    );

    gallery.scrollLeft = 0;
    modal.showModal();
  });
});

modal.querySelector(".modal-close").addEventListener("click", () => modal.close());
modal.addEventListener("click", (e) => {
  const r = modal.getBoundingClientRect();
  if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) modal.close();
});

// forms — preview only: no backend yet, so confirm inline instead of submitting
document.querySelectorAll("form.tl-form").forEach((form) => {
  const status = form.querySelector(".form-status");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const name = form.elements.name ? form.elements.name.value.trim() : "";
    status.hidden = false;
    status.textContent = `Thanks${name ? ", " + name : ""}! This is a preview, so nothing was sent — once live it'll go straight to Mike. For now, call or WhatsApp 07813 696011.`;
    form.reset();
    status.scrollIntoView({ block: "nearest", behavior: "smooth" });
  });
});

// toggle the hidden sold grid (its cards are already in the DOM, so their click
// handlers were bound above — `hidden` just collapses them out of view)
const soldToggle = document.getElementById("sold-toggle");
const soldExtra = document.getElementById("sold-extra");
if (soldToggle && soldExtra) {
  const showLabel = soldToggle.textContent;
  soldToggle.addEventListener("click", () => {
    const nowOpen = soldExtra.hidden; // about to open if currently hidden
    soldExtra.hidden = !nowOpen;
    soldToggle.setAttribute("aria-expanded", String(nowOpen));
    soldToggle.textContent = nowOpen ? "Show fewer sold vans" : showLabel;
  });
}
