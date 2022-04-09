import * as Color from "./handleColor.js"
import * as Wallpaper from "./handleWallpaper.js"

import DATA,{updateData} from "./data.js"

const section_theme = document.querySelector("section#theme")
const select_theme = document.querySelector('.theme__select select[name="theme_name"]')


const section_option = document.querySelector("section#configs")
const optionInputs = section_option.querySelectorAll('input')

const btn_changeAll = document.querySelector("button#changeAll")

async function fetchData(url) {
    let response = await fetch(`/${url}`);
    let result = await response.json();
    return result
}

async function renderTheme(){
    DATA.themes = await fetchData(`theme`)
	select_theme.innerHTML = DATA.themes[DATA.options.theme_option].reduce((html,theme) => html +=`<option>${theme}</option>`,"") 
}

async function render(){
    await Wallpaper.render()
    await renderTheme()
}

function events(){
	Color.handleEvents()
    optionInputs.forEach( inputEl => { inputEl.addEventListener('change', function() {
		const option_name = this.name
		const value = this.checked
		DATA.options[option_name] = value
	})});
}

async function app() {
	await updateData()
	await render()
	await events()
}
app()
