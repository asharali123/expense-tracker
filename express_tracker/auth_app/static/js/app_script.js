const toggleBtn = document.getElementById("themeToggle");
toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    if (document.body.classList.contains("dark-mode")) {
        toggleBtn.textContent = "☀️";
        toggleBtn.classList.remove("btn-outline-dark");
        toggleBtn.classList.add("btn-outline-light");
    } else {
        toggleBtn.textContent = "🌙";
        toggleBtn.classList.remove("btn-outline-light");
        toggleBtn.classList.add("btn-outline-dark");
    }
});