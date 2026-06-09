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
