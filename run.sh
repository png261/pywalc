#!/bin/bash
HOST=127.0.0.1
API_PORT=2601
LOCAL_PORT=2004
CACHE_DIR="$HOME/.cache/pwy"
WALLPAPER_DIR="$CACHE_DIR/wallpapers"
SITE='https://png261.github.io/pwy/'

processid=/tmp/pwy_process
tmp_api=/tmp/pwy_api
tmp_site=/tmp/pwy_site
tmp_qrcode=/tmp/pwy_qrcode

banner(){

	cat <<- EOF

		██████╗ ██╗    ██╗██╗   ██╗
		██╔══██╗██║    ██║╚██╗ ██╔╝
		██████╔╝██║ █╗ ██║ ╚████╔╝ 
		██╔═══╝ ██║███╗██║  ╚██╔╝  
		██║     ╚███╔███╔╝   ██║   
		╚═╝      ╚══╝╚══╝    ╚═╝   

	EOF
}

pwy_stop(){
	[[ ! -f $processid ]] && return

	kill $(cat $processid) > /dev/null 2>&1
	rm $processid
}

init(){
	[[ ! -d ".server" ]] && mkdir -p ".server"
	[[ ! -d $WALLPAPER_DIR ]] && mkdir -p $WALLPAPER_DIR
	pwy_stop
}

download_cloudflared() {
	url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$1"
	file=`basename $url`

	[[ -e "$file" ]] && rm -rf "$file"

	wget --no-check-certificate "$url" > /dev/null 2>&1
	[[ ! -e "$file" ]] && echo -e "\n Error occured, Install Cloudflared manually."

	mv -f "$file" .server/cloudflared && chmod +x .server/cloudflared 
}

install_cloudflared() {
	[[ -e ".server/cloudflared" ]] && return

	echo -e "\nInstalling Cloudflared..."
	case `uname -m` in 
		*'arm'*)
			download_cloudflared 'arm' ;;
		*'aarch64'*)
			download_cloudflared 'arm64' ;;
		*'x86_64'*)
			download_cloudflared 'amd64' ;;
		*)
			download_cloudflared '386' ;;
	esac

}

start_api() {
	uvicorn app:app --app-dir api --host $HOST --port $API_PORT > /dev/null 2>&1 & echo "$!" >> $processid
}

start_localhost() {
	start_api
	python -m http.server -b $HOST $LOCAL_PORT > /dev/null 2>&1 & echo "$!" >> $processid
	API_URL="$HOST:$API_PORT" 
	SITE_URL="$HOST:$LOCAL_PORT/pwy/?api=http://$API_URL" 
	show_result
}

start_cloudflared() { 
	logfile=".cloudflared.log"
	isOnline=$(ping -q -c1 google.com &>/dev/null) 
	if [ ! isOnline ]; then
		echo "You are offline, check your connection...." 
		sleep 2
		tunnel_menu

		return
	fi

	rm -f $logfile && start_api 

	.server/cloudflared tunnel -url "$HOST":"$API_PORT" --logfile $logfile > /dev/null 2>&1 & echo "$!" >> $processid

	while [ ! $API_URL ]
	do
		API_URL=$(grep -so 'https://[-0-9a-z]*\.trycloudflare.com' "$logfile")
		sleep 0.2
	done

	SITE_URL="$SITE?api=$API_URL"
	show_result
}

show_result() {
	[[ -z "$API_URL" ]] && return;

	clear
	banner

	echo -e "\nAPI: $API_URL"
	echo -e "\nURL: $SITE_URL"

	echo -e "\nQRCODE:\n"
	qrencode -t ansiutf8 -m 2 <<< $SITE_URL

	echo $API_URL > $tmp_api
	echo $SITE_URL > $tmp_site
	qrencode $SITE_URL -o $tmp_qrcode
}

tunnel_menu() {
	clear 
	banner

	cat <<- EOF
		[01] Local   
		[02] Online
		[03] Copy
		[04] Stop
	EOF

	read -p "Your option:"

	case $REPLY in 
		1 | 01)
			start_localhost ;;
		2 | 02)
			start_cloudflared ;;
		3 | 03)
			copy_menu ;;
		4 | 04)
			pwy_stop ;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 0.5
			tunnel_menu
			;;
	esac
}

copy_menu() {
	clear 
	banner

	cat <<- EOF
		[01] URL   
		[02] QRCODE
		[03] API
	EOF

	read -p "Your option: "

	case $REPLY in 
		1 | 01)
			xclip -i $tmp_site -sel c ;;
		2 | 02)
			xclip -i $tmp_qrcode -t image/png -sel c ;;
		3 | 03)
			xclip -i $tmp_api -sel c ;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 0.5
			tunnel_menu
			;;
	esac
}
init
install_cloudflared
tunnel_menu
