const DATA={
	pywal:{},
	options:{
		update_on_change : true,
		theme_option: "light",
	},
	themes:{},
	wallpaper:""
}

export async function updateData() {
    let response = await fetch(`all`);
	DATA.pywal = await response.json();
}

export default DATA


