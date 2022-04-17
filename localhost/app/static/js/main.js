import * as Settings from "./Settings.js"
import * as Color from "./Color.js"
import * as Theme from "./Theme.js"
import * as Wallpaper from "./Wallpaper.js"

import DATA,{initData} from "./data.js"

async function render(){
	await Wallpaper.render()
	await Color.render()
	await Theme.render()
}

function events(){
	Settings.events()
	Wallpaper.events()
	Theme.events()
	Color.events()
}

async function app() {
	await initData()
	await render()
	await events()
}
app()

