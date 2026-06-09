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
