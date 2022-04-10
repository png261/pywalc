const container = document.querySelector("section#color")
const color_input = container.querySelectorAll('input[type="color"]')
const reset_btn = document.querySelector("button#reset")

import DATA,{updateData} from "./data.js"

const update = async function ({name, value}) {
    if (!DATA.options.update_on_change) return;

    DATA.pywal.colors[name] = value
    const response = await fetch(`color`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(DATA.pywal)
    });
}

const render = async function () {
    Object.entries(DATA.pywal.colors).forEach(([colorName,colorValue]) => {
        const colorInput = container.querySelector(`input[name="${colorName}"]`)
        colorInput.value = colorValue
    });
}

const reset = async function() {
	await fetch("reset")
	await updateData()
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
}

export {
	update,
	render,
	events
}
