import { $, $$, setCssVar } from './helper.js'
import { COLOR, WALLPAPER } from './data.js'

const $inputs = $$('.color__input')
const $getWallpaper = $('#color__wallpaper')

async function getWallpaper() {
    COLOR.set(await WALLPAPER.colors())
    render()
}

function updateCssVar(colors = COLOR.get()) {
    Object.entries(colors).forEach(([name, value]) => setCssVar(name, value))
}

function render(colors = COLOR.get()) {
    $inputs.forEach((input) => (input.value = colors[input.name]))
}

function events() {
    $inputs.forEach((input) =>
        input.addEventListener('input', function () {
            COLOR.put(this)
        })
    )
    $getWallpaper.addEventListener('click', getWallpaper)
}

export default {
    render,
    events,
    getWallpaper,
    updateCssVar,
}
