let DATA={
	color:{},
	theme:{
		dark: true,
		list:{}
	},
	wallpaper:{
		current:"",
		list:[]
	},
	options:{
		update_on_change : true,
	},
}

export async function fetchColor() {
    const response = await fetch("all");
	const result = await response.json()
	DATA.color = result.colors
}

export async function fetchTheme() {
    const response = await fetch("theme");
	const result = {...await response.json()}
	DATA.theme.list = result
}

export async function fetchWallpaper() {
    const response = await fetch("wallpaper");
	const result = await response.json()
	DATA.wallpaper.list = result
}

export async function initData(){
	await fetchTheme()
	await fetchWallpaper()
	await fetchColor()
}

export default DATA


