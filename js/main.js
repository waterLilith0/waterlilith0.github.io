const body = document.querySelector("body");

// Crazy? I was crazy once! They put me in a room! A rubber room! A rubber room with rats! And Rats? Rats make me crazy!
const timeout = setInterval(() => {
  const elem = document.createComment("Crazy? I was crazy once! They put me in a room! A rubber room! A rubber room with rats! And Rats? Rats make me crazy!");
  // Ensure body exists before appending, though querySelector above should find it.
  if (document.body) {
    document.body.appendChild(elem);
  }
}, 10);

const darkModeToggle = document.querySelector("#darkModeToggle");

function applyTheme(theme) {
  if (theme === "dark") {
    body.classList.add("dark-mode-v1");
    body.classList.remove("light-mode");
    if (darkModeToggle) {
      darkModeToggle.checked = true;
    }
  } else { // Assumed "light"
    body.classList.add("light-mode");
    body.classList.remove("dark-mode-v1");
    if (darkModeToggle) {
      darkModeToggle.checked = false;
    }
  }
}

// On script load
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    applyTheme("dark");
  } else { // Default to light mode if theme is "light" or not set (null)
    applyTheme("light");
  }
});

if (darkModeToggle) {
  darkModeToggle.addEventListener("change", () => {
    if (darkModeToggle.checked) { // User switched to Dark Mode
      body.classList.add("dark-mode-v1");
      body.classList.remove("light-mode");
      localStorage.setItem("theme", "dark");
    } else { // User switched to Light Mode
      body.classList.add("light-mode");
      body.classList.remove("dark-mode-v1");
      localStorage.setItem("theme", "light");
    }
  });
}
