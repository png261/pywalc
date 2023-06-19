import { $, $$, setCssVar } from './util.js'
import API from './Api.js'


const Wallpaper = new class {
    async init() {
        const { current, list } = await API.get('wallpaper')
        this.current = current
        this.list = list
        this.setupHTML()
    }

    setupHTML() {
        this.$gallery = $('.wallpaper__gallery')
        this.$input_upload = $('.wallpaper__upload input[type="file"]')
    }

    render() {
        (this.list).map((id) => (this.$gallery.innerHTML +=
            `<div id="${id}"
                        class="wallpaper__img"
                        onclick="changeWallpaper(this.id)"  
                        style="background-image:url(/cache/wallpapers/${id})">
                    </div>`))
        this.updateActiveElement()
    }

    handleEvents() {
        this.$input_upload.addEventListener('change', async () => {
            this.list = await this.upload([...this.$input_upload.files])
            this.render()
        })
        window.changeWallpaper = (id) => {
            this.current = id
            this.updateActiveElement()
        }
    }

    updateActiveElement(id = this.current) {
        $$('.wallpaper__img.active').forEach((el) => el.classList.remove('active'))

        const activeEl = $(`.wallpaper__img[id='${id}']`)
        if (activeEl) {
            activeEl.classList.add('active')
        }
    }

    async getColors() {
        return await API.get(`wallpaper/${this.current}/color`)
    }

    async update() {
        await API.put(`wallpaper/${this.current}`)
    }

    async upload(images) {
        return await API.upload('wallpaper', images)
    }

    async apply() {
        const { current, list } = await API.get('wallpaper/apply')
        this.current = current
        this.list = list
    }

    updateCss() {
        setCssVar('background-image', `url(/cache/wallpapers/${this.current})`)
    }
}

export default Wallpaper
