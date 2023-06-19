import { $ } from './util.js'
import API from './Api.js'


const System = new class {
    async init() {
        const data = await API.get('sys')
        this.os = data.os
        this.name = data.name
        this.setupHTML()
    }

    async setupHTML() {
        this.$title = $('.sys__title')
    }

    async reset() {
        await API.get('reset')
    }

    render() {
        this.$title.innerHTML = `Connected ${this.os}-${this.name}`
    }
}

export default System
