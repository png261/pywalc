import DATA,{fetchColor} from "./data.js"

const container = document.querySelector("section#color")
const color_input = container.querySelectorAll('input[type="color"]')
const reset_btn = document.querySelector("button#reset")
const wallpaper_btn = document.querySelector("button#color__wallpaper")

export async function update (colors) {
    if (!DATA.options.update_on_change) return;

	console.log(colors)
	DATA.color = {...DATA.color,...colors}
	console.log(DATA.color)
    const response = await fetch(`color`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(DATA.color)
    });
}

export async function render () {
    Object.entries(DATA.color).forEach(([colorName,colorValue]) => {
        const colorInput = container.querySelector(`input[name="${colorName}"]`)
        colorInput.value = colorValue
    });
}

async function reset() {
	await fetch("reset")
	await fetchColor()
    render()
}

export async function getWallpaper (){
    const respone = await fetch(`color/wallpaper/${DATA.wallpaper.current}`)
	const data = await respone.json()
	DATA.color = data.colors
	update(DATA.color)
	render()
}

export function events () {
    color_input.forEach( inputEl => {
		inputEl.addEventListener('input', function() {
			const {name,value} = this
			update({[name]:value})
		})
	});
    reset_btn.addEventListener('click', reset)
    wallpaper_btn.addEventListener('click', getWallpaper)
}
