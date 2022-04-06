
const section_theme = document.querySelector("section#theme")
const select_theme = document.querySelector('select[name="theme_name"]')

const section_wallpaper = document.querySelector("section#wallpaper")
const gallery = section_wallpaper.querySelector("#gallery")


const section_color = document.querySelector("section#colors")
const colorInputs = section_color.querySelectorAll('input[type="color"]')

const section_option = document.querySelector("section#options")
const optionInputs = section_option.querySelectorAll('input')

const btn_changeAll = document.querySelector("button#changeAll")
const btn_reset = document.querySelector("button#reset")

const BASE_URL = ""
const OPTION = {
    update_on_change : true,
    theme_option: "light",
}

let PYWAL, WALLPAPERS;

async function fetchData(url) {
    let response = await fetch(`${BASE_URL}/${url}`);
    let result = await response.json();
    return result
}

async function restColor() {
    await fetchData('reset')
    PYWAL = await fetchData("all")
    renderColors()
}

async function changeWallpaper(el,wallpaper) {
    pictures = gallery.querySelectorAll(".gallery_picture.active")
    pictures.forEach(pic => { pic.classList.remove("active"); });
	console.log(wallpaper)

    const response = await fetch(`${BASE_URL}/wallpaper`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(wallpaper)
    });
    // const result = await response.json();

    el.classList.add("active");
}

async function renderGallery() {
    WALLPAPERS = await fetchData("wallpaper")
    gallery.innerHTML = WALLPAPERS.reduce(
        (html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="gallery_picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}

async function renderTheme(){
    themes = await fetchData("theme")
	select_theme.innerHTML = themes[OPTION.theme_option].reduce((html,theme) => html +=`<option>${theme}</option>`,"") 
}


async function updateColor({name, value}) {
    if (!OPTION.update_on_change) return;

    PYWAL.colors[name] = value
    const response = await fetch(`${BASE_URL}/color`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(PYWAL)
    });
    const result = await response.json();
    return result
}

async function renderColors() {
    Object.entries(PYWAL.colors).forEach(([colorName,colorValue]) => {
        const colorInput = section_color.querySelector(`input[name="${colorName}"]`)
        colorInput.value = colorValue
    });
}

function handleEvent() {
    colorInputs.forEach(
        inputEl => {inputEl.addEventListener('input', function() {
            let name = this.name
            let value = this.value
            updateColor({name, value})
        })});

    optionInputs.forEach(
        inputEl => {inputEl.addEventListener('change', function() {
            const option_name = this.name
            const value = this.checked
            OPTION[option_name] = value
        })});

    btn_reset.addEventListener('click', restColor)
}

async function app() {
    PYWAL = await fetchData("all")
    renderGallery()
    renderTheme()
    renderColors()
    handleEvent()
}
app()
