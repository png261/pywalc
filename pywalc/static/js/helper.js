export const $ = document.querySelector.bind(document)
export const $$ = document.querySelectorAll.bind(document)

export function getParam(name) {
    const params = new URLSearchParams(window.location.search)
    return params.get(name)
}

export function setCssVar(name, value) {
    document.documentElement.style.setProperty(`--${name}`, value)
}
