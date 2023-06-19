import { $ } from './util.js'
import API from './Api.js'
import Color from './Color.js'


const Theme = new class {
    async init() {
        this.themes = await API.get('theme')
        this.category = 'dark'
        this.setupHTML()
    }

    setupHTML() {
        this.$select_themes = $('.theme__select>select')
        this.$switch_category = $('.theme__option input[name="dark"]')
    }

    render() {
        this.$select_themes.innerHTML = this.themes[this.category].reduce(
            (html, theme) => (html += `<option>${theme}</option>`),
            ''
        )
    }

    handleEvents() {
        this.$select_themes.addEventListener('change', async () => await this.updateColors())
        this.$switch_category.addEventListener('change', () => {
            this.category = this.$switch_category.checked ? 'dark' : 'light'
            this.render()
        })
    }

    async get(name) {
        return API.get(`theme/${this.category}/${name}`)
    }

    async updateColors() {
        Color.change(await this.get(this.$select_themes.value))
        Color.render()
    }
}

export default Theme

