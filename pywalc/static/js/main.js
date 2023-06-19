import System from './System.js'
import Wallpaper from './Wallpaper.js'
import Theme from './Theme.js'
import Color from './Color.js'
import Actions from './Actions.js'


function render() {
    Color.updateCss()
    Wallpaper.updateCss()
    Wallpaper.render()
    System.render()
    Color.render()
    Theme.render()
}

function handleEvents() {
    Wallpaper.handleEvents()
    Color.handleEvents()
    Theme.handleEvents()
    Actions.handleEvents()
}

async function init() {
    await System.init()
    await Color.init()
    await Wallpaper.init()
    await Theme.init()
    Actions.init()
}

async function main() {
    await init()
    handleEvents()
    render()
}
main()
