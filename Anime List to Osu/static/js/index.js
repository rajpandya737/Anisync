function replaceSubstrings() {
  const h3Elements = document.querySelectorAll('.card-container h3');
  h3Elements.forEach(h3 => {
    let updatedText = h3.textContent;
    updatedText = updatedText.replace(/\\&quot;/g, "\"");
    updatedText = updatedText.replace(/fate\\\//gi, "fate/");
    h3.textContent = updatedText;
  });
}
  // Call the function after the page loads
  document.addEventListener('DOMContentLoaded', replaceSubstrings);

  const toTop = document.querySelector(".to-top");
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      toTop.classList.add("active");
    } else {
      toTop.classList.remove("active");
    }
  })
  

  