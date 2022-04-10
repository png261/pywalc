import DATA,{updateData} from "./data.js"
import * as Color from "./Color.js"

const section = document.querySelector("section#theme")
const theme_select = document.querySelector('.theme__select select[name="theme_name"]')


async function change(name){
    const response = await fetch("theme", {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(name)
    });
}

async function render(){
	let response = await fetch(`theme`)
    DATA.themes = await response.json()
	theme_select.innerHTML = DATA.themes[DATA.options.theme_option].reduce((html,theme) => html +=`<option>${theme}</option>`,"") 
}

async function events(){
	theme_select.addEventListener("change", async function() {
		await change(this.value)
		await updateData()
		await Color.render()
	}) 
}

export {
	render,
	events
}
