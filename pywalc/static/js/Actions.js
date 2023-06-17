import { SYS, WALLPAPER, COLOR } from './data.js'
import { $ } from './helper.js'
import Color from './Color.js'
import Wallpaper from './Wallpaper.js'

const $reset = $('.action__reset')
const $change = $('.action__change')

function events() {
    async function reset() {
        await SYS.reset()

        await WALLPAPER.load()
        await COLOR.load()

        Color.updateCssVar()
        Wallpaper.updateCssVar()

        Wallpaper.active()
        Color.render()
    }
    $reset.addEventListener('click', reset)

    async function change() {
        await WALLPAPER.update()
        await COLOR.update()

        await WALLPAPER.load()
        await COLOR.load()

        Color.updateCssVar()
        Wallpaper.updateCssVar()
    }
    $change.addEventListener('click', change)
}

export default {
    events,
}
