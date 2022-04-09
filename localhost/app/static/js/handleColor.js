const section_color = document.querySelector("section#color")
const colorInputs = section_color.querySelectorAll('input[type="color"]')
const resetBtn = document.querySelector("button#reset")

import DATA,{updateData} from "./data.js"

const update = async function ({name, value}) {
    if (!DATA.options.update_on_change) return;

    DATA.pywal.colors[name] = value
    const response = await fetch(`color`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(DATA.pywal)
    });
    const result = await response.json();
    return result
}

const render = async function () {
    Object.entries(DATA.pywal.colors).forEach(([colorName,colorValue]) => {
        const colorInput = section_color.querySelector(`input[name="${colorName}"]`)
        colorInput.value = colorValue
    });
}

const reset = async function() {
	await fetch("reset")
	await updateData()
    render()
}

const handleEvents = function () {
    colorInputs.forEach( inputEl => {inputEl.addEventListener('input', function() {
		let name = this.name
		let value = this.value
		update({name, value})
	})});
    resetBtn.addEventListener('click', reset)
}

export {
	update,
	render,
	handleEvents
}
