import * as DATA from './data.js'
import Sys from './Sys.js'
import Color from './Color.js'
import Theme from './Theme.js'
import Wallpaper from './Wallpaper.js'
import Actions from './Actions.js'

function render() {
    Color.updateCssVar()
    Wallpaper.updateCssVar()
    Wallpaper.render()
    Sys.render()
    Color.render()
    Theme.render()
}

function events() {
    Wallpaper.events()
    Theme.events()
    Color.events()
    Actions.events()
}

; (async function run() {
    await DATA.init()
    render()
    events()
})()
