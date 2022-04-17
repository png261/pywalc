let DATA={};

export async function fetchColor() {
    const response = await fetch("color");
	const result = await response.json()
	DATA.color = result.colors
}

export async function fetchTheme() {
    const response = await fetch("theme");
	const result = await response.json()
	DATA.theme.list = result
}

export async function fetchWallpaper() {
    const response = await fetch("wallpaper");
	const result = await response.json()
	DATA.wallpaper.list = result
}

export async function initData (){
    const response = await fetch("all");
	const result = await response.json()
	DATA = result
}

export default DATA


