import * as Color from "./Color.js"
import * as Theme from "./Theme.js"
import * as Wallpaper from "./Wallpaper.js"

import DATA,{initData} from "./data.js"

const section_option = document.querySelector("section#configs")
const optionInputs = section_option.querySelectorAll('input')
const btn_changeAll = document.querySelector("button#changeAll")

async function render(){
    await Wallpaper.render()
    await Color.render()
    await Theme.render()
}

function events(){
	Color.events()
	Theme.events()

    optionInputs.forEach( inputEl => { inputEl.addEventListener('change', function() {
		const option_name = this.name
		const value = this.checked
		DATA.options[option_name] = value
	})});
}

async function app() {
	await initData()
	await render()
	await events()
}
app()

