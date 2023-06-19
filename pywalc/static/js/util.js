const $ = document.querySelector.bind(document)
const $$ = document.querySelectorAll.bind(document)

function getParam(name) {
    const params = new URLSearchParams(window.location.search)
    return params.get(name)
}

function setCssVar(name, value) {
    document.documentElement.style.setProperty(`--${name}`, value)
}

export {
    $, $$, getParam, setCssVar
}
