import DATA,{fetchWallpaper} from "./data.js"

const container = document.querySelector("section#wallpaper")
const gallery = container.querySelector(".wallpaper__gallery")
const input_folder = container.querySelector(".wallpaper__folder input")

async function change(el, url) {
    gallery.querySelectorAll(".wallpaper__picture.active").forEach(pic => { pic.classList.remove("active") });

    await fetch(`wallpaper`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(url)
    });

    el.classList.add("active");
}
window.changeWallpaper = change

async function upload([...imgs]) {
	const formData = new FormData();
	imgs.map(img => formData.append("images", img))

    await fetch(`uploadWallpaper`, {
        method : 'POST',
        body : formData 
    });
	await fetchWallpaper()
	await render()
}

async function events() {
	input_folder.addEventListener("change",function (){
		upload(this.files)
	})
}

async function render() {
    gallery.innerHTML = DATA.wallpaper.list.reduce((html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="wallpaper__picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}

export {
	change,
	render,
	events,
}
