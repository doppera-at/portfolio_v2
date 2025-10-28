// ### ON PAGE LOAD
// Get preferences and set theme accordingly
var localStorageTheme = localStorage.getItem("theme")
var darkSchemePreferred = window.matchMedia("(prefers-color-scheme: dark)")

if (localStorageTheme == "dark") {
    toggleDarkMode()
} else if (localStorageTheme == "light") {
    toggleLightMode()
} else {
    localStorage.setItem("theme", darkSchemePreferred ? "dark" : "light")
    if (darkSchemePreferred) toggleDarkMode()
    else toggleLightMode()
}


function toggleTheme() {
    if (document.body.classList.contains("dark-mode")) toggleLightMode() 
    else toggleDarkMode()
}

function toggleLightMode() {
    document.body.classList.remove("dark-mode")
    document.getElementById("toggle-dark-mode").innerText = "Theme: ☾"
    localStorage.setItem("theme", "light")
}
function toggleDarkMode() {
    document.body.classList.add("dark-mode")
    document.getElementById("toggle-dark-mode").innerText = "Theme: ☀"
    localStorage.setItem("theme", "dark")
}