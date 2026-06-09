// scroll reveals
const io = new IntersectionObserver(
  (entries) => entries.forEach((e) => e.isIntersecting && (e.target.classList.add("in"), io.unobserve(e.target))),
  { threshold: 0.12 }
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// van detail modal
const modal = document.getElementById("van-modal");
const gallery = modal.querySelector(".modal-gallery");
const titleEl = modal.querySelector("h3");
const summaryEl = modal.querySelector(".summary");
const specsEl = modal.querySelector(".modal-specs");

document.querySelectorAll(".van-card").forEach((card) => {
  card.addEventListener("click", () => {
    const van = JSON.parse(card.dataset.van);
    titleEl.textContent = van.title;
    summaryEl.textContent = van.summary;

    gallery.replaceChildren(
      ...van.photos.map((p, i) => {
        const img = document.createElement("img");
        img.src = p;
        img.alt = `${van.title} — photo ${i + 1}`;
        img.loading = "lazy";
        return img;
      })
    );

    specsEl.replaceChildren(
      ...Object.entries(van.specs).map(([k, v]) => {
        const cell = document.createElement("div");
        const label = document.createElement("b");
        label.textContent = k;
        cell.append(label, document.createTextNode(v));
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
