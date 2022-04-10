import DATA,{updateData} from "./data.js"

const section_theme = document.querySelector("section#theme")
const select_theme = document.querySelector('.theme__select select[name="theme_name"]')

async function render(){
	let response = await fetch(`theme`)
    DATA.themes = await response.json()
	select_theme.innerHTML = DATA.themes[DATA.options.theme_option].reduce((html,theme) => html +=`<option>${theme}</option>`,"") 
}

export {
	render
}
