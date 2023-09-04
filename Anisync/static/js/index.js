function replaceSubstrings() {
  let e = document.querySelectorAll(".card-container h3");
  e.forEach((e) => {
    let t = e.textContent;
    (t = (t = (t = (t = t.replace(/\\"/g, '"')).replace(
      /fate\\\//gi,
      "fate/"
    )).replace(/&amp;/g, "&")).replace(/\\&quot;/g, '"')),
      (e.textContent = t);
  });
}
document.addEventListener("DOMContentLoaded", replaceSubstrings);
const toTop = document.querySelector(".to-top");
window.addEventListener("scroll", () => {
  window.pageYOffset > 100
    ? toTop.classList.add("active")
    : toTop.classList.remove("active");
});
