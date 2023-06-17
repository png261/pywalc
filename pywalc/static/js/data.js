import API from './api.js'

let COLOR
let THEME
let WALLPAPER
let SYS

class Wallpaper {
    constructor({ current, list }) {
        this.current = current
        this.list = list
    }
    async colors() {
        return await API.get(`wallpaper/${this.current}/color`)
    }
    async update() {
        await API.put(`wallpaper/${this.current}`)
    }
    async upload(imgs) {
        return await API.upload('wallpaper', imgs)
    }
    async load() {
        const { current, list } = await API.get('wallpaper/load')
        this.current = current
        this.list = list
    }
}

class Theme {
    constructor({ dark, light }) {
        this.isDark = true
        this.dark = dark
        this.light = light
    }
    async get(name) {
        return API.get(`theme/${this.isDark ? 'dark' : 'light'}/${name}`)
    }
}

class Color {
    constructor(colors) {
        this.colors = colors
    }
    get() {
        return this.colors
    }
    put({ name, value }) {
        this.colors[name] = value
    }
    set(colors) {
        this.colors = colors
    }
    async update() {
        await API.put('color', this.colors)
    }
    async load() {
        this.colors = await API.get('color/load')
    }
}

class Sys {
    constructor({ os, name }) {
        this.os = os
        this.name = name
    }
    async reset() {
        await API.get('reset')
    }
}

async function init() {
    WALLPAPER = new Wallpaper(await API.get('wallpaper'))
    THEME = new Theme(await API.get('theme'))
    COLOR = new Color(await API.get('color'))
    SYS = new Sys(await API.get('sys'))
}

export { COLOR, THEME, WALLPAPER, SYS, init }
