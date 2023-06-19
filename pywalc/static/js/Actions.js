import { $ } from './util.js'
import Wallpaper from './Wallpaper.js'
import Color from './Color.js'
import System from './System.js'


const Actions = new class {
    init() {
        this.setupHTML()
    }

    setupHTML() {
        this.$btn_reset = $('.action__reset')
        this.$btn_change = $('.action__change')
    }

    handleEvents() {
        this.$btn_reset.addEventListener('click', async function reset() {
            await System.reset()

            await Wallpaper.apply()
            await Color.apply()

            Color.updateCss()
            Wallpaper.updateCss()

            Wallpaper.updateActiveElement()
            Color.render()
        })

        this.$btn_change.addEventListener('click',
            async function change() {
                await Wallpaper.update()
                await Color.update()

                await Wallpaper.apply()
                await Color.apply()

                Color.updateCss()
                Wallpaper.updateCss()
            }
        )
    }
}

export default Actions

