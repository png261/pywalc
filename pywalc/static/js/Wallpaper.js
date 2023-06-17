import { BASE_URL } from './api.js'
import { $, $$, setCssVar } from './helper.js'
import { WALLPAPER } from './data.js'

const $gallery = $('.wallpaper__gallery')
const $input = $('.wallpaper__upload input[type="file"]')

function active(id = WALLPAPER.current) {
    $$('.wallpaper__img.active').forEach((el) => el.classList.remove('active'))

    const activeEl = $(`.wallpaper__img[id='${id}']`)
    activeEl && activeEl.classList.add('active')
}

function img(id) {
    return `url(${BASE_URL}/cache/wallpapers/${id})`
}

window.changeWallpaper = (id) => {
    WALLPAPER.current = id
    active()
}

function render(imgs = WALLPAPER.list) {
    function html(id) {
        return `<div id="${id}"
                    class="wallpaper__img"
                    onclick="changeWallpaper(this.id)"  
                    style="background-image:${img(id)}">
                </div>`
    }

    imgs.map((id) => ($gallery.innerHTML += html(id)))
    active()
}

function events() {
    async function upload() {
        render(await WALLPAPER.upload([...$input.files]))
    }
    $input.addEventListener('change', upload)
}

function updateCssVar() {
    setCssVar('background-image', img(WALLPAPER.current))
}

export default {
    render,
    events,
    updateCssVar,
    active,
}
