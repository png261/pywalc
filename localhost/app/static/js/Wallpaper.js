import DATA,{fetchWallpaper} from "./data.js"

const container = document.querySelector("section#wallpaper")
const gallery = container.querySelector(".wallpaper__gallery")
const input_folder = container.querySelector('.wallpaper__upload input[type="file"]')

export async function change(el, wallId) {
    gallery.querySelectorAll(".wallpaper__picture.active").forEach(pic => { pic.classList.remove("active") });

    await fetch(`wallpaper`, {
        method : 'POST',
        headers : {'Content-Type' : 'application/json'},
        body : JSON.stringify(wallId)
    });
	DATA.wallpaper.current = wallId

    el.classList.add("active");
}
window.changeWallpaper = change

export async function upload([...imgs]) {
	const formData = new FormData();
	imgs.map(img => formData.append("images", img))

	const respone = await fetch(`uploadWallpaper`, {
        method : 'POST',
        body : formData 
    });
	const {success, newUrl} = await respone.json()

	if(success){
		gallery.innerHTML += newUrl.reduce((html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="wallpaper__picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
	}
}

export async function events() {
	input_folder.addEventListener("change",function (){
		upload(this.files)
	})
}

export async function render() {
    gallery.innerHTML = DATA.wallpaper.list.reduce((html, url) => html += `<div onclick="changeWallpaper(this,'${url}')" class="wallpaper__picture" style="background-image:url(/static/wallpapers/${url})"> </div>`, "")
}
