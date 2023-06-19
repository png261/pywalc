import { $, $$, setCssVar } from './util.js'
import Wallpaper from './Wallpaper.js'
import API from './Api.js'


const Color = new class {
    async init() {
        this.colors = await API.get('color')
        this.setupHTML()
    }

    setupHTML() {
        this.$input_colors = $$('.color__input')
        this.$btn_get_wallpaper_colors = $('#color__wallpaper')
    }

    render(colors = this.colors) {
        this.$input_colors.forEach((input) => (input.value = colors[input.name]))
    }

    handleEvents() {
        this.$input_colors.forEach((input) =>
            input.addEventListener('input', function() {
                this.colors[this.name] = this.value
            })
        )
        this.$btn_get_wallpaper_colors.addEventListener('click', async () => await this.getWallpaper(), false)
    }

    async update() {
        await API.put('color', this.colors)
    }

    async apply() {
        this.colors = await API.get('color/apply')
    }

    change(colors) {
        this.colors = colors
    }

    updateCss(colors = this.colors) {
        Object.entries(colors).forEach(([name, value]) => setCssVar(name, value))
    }

    async getWallpaper() {
        this.change(await Wallpaper.getColors())
        this.render()
    }
}

export default Color
