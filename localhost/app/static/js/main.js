import handleColor,{updateColor} from "./handleColor.js"
import DATA,{updateData} from "./data.js"

const section_theme = document.querySelector("section#theme")
const select_theme = document.querySelector('.theme__select select[name="theme_name"]')

const section_wallpaper = document.querySelector("section#wallpaper")
const gallery = section_wallpaper.querySelector("#gallery")

const section_option = document.querySelector("section#configs")
const optionInputs = section_option.querySelectorAll('input')

const btn_changeAll = document.querySelector("button#changeAll")

async function fetchData(url) {
    let response = await fetch(`/${url}`);
    let result = await response.json();
    return result
}

async function changeWallpaper(el,wallpaper) {
    pictures = gallery.querySelectorAll(".gallery_picture.active")
    pictures.forEach(pic => { pic.classList.remove("active"); });

    const response = await fetch(`wallpaper`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(DATA.wallpaper)
    });

    el.classList.add("active");
}

async function renderGallery() {
    DATA.wallpaper = await fetchData("wallpaper")
    gallery.innerHTML = DATA.wallpaper.reduce(
        (html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="gallery_picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}

async function renderTheme(){
    DATA.themes = await fetchData(`theme`)
	select_theme.innerHTML = DATA.themes[DATA.options.theme_option].reduce((html,theme) => html +=`<option>${theme}</option>`,"") 
}


function handleEvent() {
    optionInputs.forEach(
        inputEl => {inputEl.addEventListener('change', function() {
            const option_name = this.name
            const value = this.checked
            DATA.options[option_name] = value
        })});
}

async function app() {
	await updateData()
    await renderGallery()
    await renderTheme()
    await handleColor()
    await handleEvent()
}
app()
