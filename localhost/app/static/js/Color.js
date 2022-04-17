const container = document.querySelector("section#color")
const color_input = container.querySelectorAll('input[type="color"]')
const reset_btn = document.querySelector("button#reset")
const wallpaper_btn = document.querySelector("button#color__wallpaper")

import DATA,{fetchColor} from "./data.js"

const update = async function (colors) {
    if (!DATA.options.update_on_change) return;

	DATA.color = {...DATA.color,...colors}
    const response = await fetch(`color`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(DATA.color)
    });
}

const render = async function () {
    Object.entries(DATA.color).forEach(([colorName,colorValue]) => {
        const colorInput = container.querySelector(`input[name="${colorName}"]`)
        colorInput.value = colorValue
    });
}

const reset = async function() {
	await fetch("reset")
	await fetchColor()
    render()
}

const getWallpaper = async function (){
    const respone = await fetch(`color/wallpaper/${DATA.wallpaper.current}`)
	const data = await respone.json()
	DATA.color = data.colors
	update(DATA.color)
	render()
}

const events = function () {
    color_input.forEach( inputEl => {
		inputEl.addEventListener('input', function() {
			let name = this.name
			let value = this.value
			update({name, value})
		})
	});
    reset_btn.addEventListener('click', reset)
    wallpaper_btn.addEventListener('click', getWallpaper)
}

export {
	update,
	render,
	events
}
