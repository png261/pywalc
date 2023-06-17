import { SYS } from './data.js'
import { $ } from './helper.js'

const $title = $('.sys__title')

function render() {
    $title.innerHTML = `Connected ${SYS.os}-${SYS.name}`
}

export default {
    render,
}
