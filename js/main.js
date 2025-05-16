const body = document.querySelector("body");

const timeout = setInterval(() => {
  const elem = document.createComment("Crazy? I was crazy once! They put me in a room! A rubber room! A rubber room with rats! And Rats? Rats make me crazy!");
  document.body.appendChild(elem);
}, 10);


const darkModeToggle = document.querySelector("#darkModeToggle");
darkModeToggle.addEventListener("click", () => {
  darkMode();
});

const darkMode = (() => {
  body.classList.toggle("black");
});

darkMode();
