// Code from:
//https://www.cssscript.com/automatic-dark-mode-bootstrap/

;(function () {
    console.log('auto dark mode')
    const htmlElement = document.querySelector("html")
    console.log(htmlElement, htmlElement.getAttribute("data-bs-theme"))
    if(htmlElement.getAttribute("data-bs-theme") === 'auto') {
        function updateTheme() {
            document.querySelector("html").setAttribute("data-bs-theme",
                window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
        }
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme)
        updateTheme()
    }
})()