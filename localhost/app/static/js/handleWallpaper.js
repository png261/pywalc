import DATA,{updateData} from "./data.js"

const section_wallpaper = document.querySelector("section#wallpaper")
const gallery = section_wallpaper.querySelector(".wallpaper__gallery")

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
    DATA.wallpaper = await fetchData("wallpaper")
    gallery.innerHTML = DATA.wallpaper.reduce(
        (html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="wallpaper__picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}

export {
	change,
	render,
}
