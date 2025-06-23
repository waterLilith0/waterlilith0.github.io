// Utility to dynamically switch between light.css and dark.css
function setThemeCss(theme) {
  // Remove any existing theme stylesheet
  let lightLink = document.getElementById('light-css');
  let darkLink = document.getElementById('dark-css');

  if (lightLink) lightLink.remove();
  if (darkLink) darkLink.remove();

  // Add the correct stylesheet
  const head = document.head;
  if (theme === "dark") {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/dark.css';
    link.id = 'dark-css';
    head.appendChild(link);
  } else {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/light.css';
    link.id = 'light-css';
    head.appendChild(link);
  }
}

const darkModeToggle = document.querySelector("#darkModeToggle");

function applyTheme(theme) {
  setThemeCss(theme);
  if (darkModeToggle) {
    darkModeToggle.checked = (theme === "dark");
  }
}

// On script load
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    applyTheme("dark");
  } else {
    applyTheme("light");
  }
});

if (darkModeToggle) {
  darkModeToggle.addEventListener("change", () => {
    if (darkModeToggle.checked) {
      localStorage.setItem("theme", "dark");
      applyTheme("dark");
    } else {
      localStorage.setItem("theme", "light");
      applyTheme("light");
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems);
});