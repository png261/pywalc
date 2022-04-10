import DATA,{updateData} from "./data.js"

const container = document.querySelector("section#wallpaper")
const gallery = container.querySelector(".wallpaper__gallery")

async function change(el, url) {
    gallery.querySelectorAll(".wallpaper__picture.active").forEach(pic => { pic.classList.remove("active") });

    const response = await fetch(`wallpaper`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(url)
    });

    el.classList.add("active");
}
window.changeWallpaper = change

async function render() {
	let response = await fetch("wallpaper")
    DATA.wallpaper = await response.json()
    gallery.innerHTML = DATA.wallpaper.reduce(
        (html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="wallpaper__picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}

export {
	change,
	render,
}
