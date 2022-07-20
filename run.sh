#!/bin/bash
source config

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
	[[ ! -d $WALLPAPER_DIR ]] && mkdir -p $WALLPAPER_DIR
}

start_api() {
    pwy_stop
	[[ ! -d $PYWALL_DIR ]] && wal --theme random
    cp $(cat "${PYWALL_DIR}/wal") "${WALLPAPER_DIR}/current"
	uvicorn app:app --app-dir api --host $HOST --port $API_PORT > /dev/null 2>&1 & echo "$!" >> $processid
}

start_localhost() {
	start_api
	python -m http.server -b $HOST $LOCAL_PORT > /dev/null 2>&1 & echo "$!" >> $processid
	API_URL="http://$HOST:$API_PORT" 
	SITE_URL="http://$HOST:$LOCAL_PORT/pwy/?api=$API_URL" 
	show_result
}

start_cloudflared() { 
	isOnline=$(ping -q -c1 google.com &>/dev/null) 
	if [ ! isOnline ]; then
		echo "You are offline, check your connection...." 
		sleep 2
		tunnel_menu
		return
	fi

	start_api 

	rm -f $server_log
	.server/cloudflared tunnel -url "$HOST":"$API_PORT" --logfile  $server_log > /dev/null 2>&1 & echo "$!" >> $processid

	while [ ! $API_URL ]
	do
		API_URL=$(grep -so 'https://[-0-9a-z]*\.trycloudflare.com' "$server_log")
		sleep 0.2
	done

	SITE_URL="$SITE?api=$API_URL"
	show_result
}

show_result() {
	[[ -z "$API_URL" ]] && return;

	clear
	banner

	echo -e "\nURL: $SITE_URL"
	echo -e "\nAPI: $API_URL"

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
		[05] Reset
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
		5 | 05)
			pwy_stop 
			rm -rf $CACHE_DIR ;;
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
		[04] Go Back...
	EOF

	read -p "Your option: "

	case $REPLY in 
		1 | 01)
			xclip -i $tmp_site -sel c ;;
		2 | 02)
			xclip -i $tmp_qrcode -t image/png -sel c ;;
		3 | 03)
			xclip -i $tmp_api -sel c ;;
		4 | 04)
			tunnel_menu ;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 0.5
			copy_menu
			;;
	esac
}
init
tunnel_menu
