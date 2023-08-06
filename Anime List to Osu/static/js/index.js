function replaceFateSubstring() {
    const h3Elements = document.querySelectorAll('.card-container h3');
    h3Elements.forEach(h3 => {
      const originalText = h3.textContent;
      const updatedText = originalText.replace(/fate\\\//gi, "fate/");
      h3.textContent = updatedText;
    });
  }
  

  // Call the function after the page loads
  document.addEventListener('DOMContentLoaded', replaceFateSubstring);

  const toTop = document.querySelector(".to-top");
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      toTop.classList.add("active");
    } else {
      toTop.classList.remove("active");
    }
  })
  

  