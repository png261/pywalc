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

init(){
	if [[ ! -d ".server" ]]; then
		mkdir -p ".server"
	fi
	if [[ ! -d $CACHE_DIR ]]; then
		mkdir -p $CACHE_DIR
	fi

	if [[ `pidof python` ]]; then
		killall python > /dev/null 2>&1
	fi
	if [[ `pidof cloudflared` ]]; then
		killall cloudflared > /dev/null 2>&1
	fi
}

install_cloudflared() {
	download_cloudflared() {
		url="$1"
		file=`basename $url`

		if [[ -e "$file" ]]; then
			rm -rf "$file"
		fi

		wget --no-check-certificate "$url" > /dev/null 2>&1

		if [[ -e "$file" ]]; then
			mv -f "$file" .server/cloudflared > /dev/null 2>&1
			chmod +x .server/cloudflared > /dev/null 2>&1
		else
			echo -e "\n Error occured, Install Cloudflared manually."
		fi
	}

	if [[ -e ".server/cloudflared" ]]; then
		return
	else
		echo -e "\nInstalling Cloudflared..."
		arch=`uname -m`
		if [[ "$arch" == *'arm'* ]]; then
			download_cloudflared 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm'
		elif [[ "$arch" == *'aarch64'* ]]; then
			download_cloudflared 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
		elif [[ "$arch" == *'x86_64'* ]]; then
			download_cloudflared 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
		else
			download_cloudflared 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386'
		fi
	fi

}

start_api() {
	cd api && python app.py > /dev/null 2>&1 & 
}

start_localhost() {
	start_api
	python -m http.server -d client -b $HOST $LOCAL_PORT > /dev/null 2>&1 & 
	API_URL="$HOST:$API_PORT" 
	SITE_URL="$HOST:$LOCAL_PORT?api=$API_URL" 
	show_result
}

start_cloudflared() { 
	logfile=".cloudflared.log"

	rm -f $logfile &
	start_api 
	.server/cloudflared tunnel -url "$HOST":"$API_PORT" --logfile $logfile > /dev/null 2>&1 &

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

	echo -e "\nAPI: $API_URL"
	echo -e "\nURL: $SITE_URL"

	echo -e "\nQRCODE:\n"
	qrencode -t ansiutf8 -m 2 <<< $SITE_URL

	echo $API_URL > /tmp/pwy_link
	echo "$SITE?api=$API_URL" > /tmp/pwy_site
	qrencode $SITEURL -o /tmp/pwy_qrcode 
}

tunnel_menu() {
	clear 
	banner

	cat <<- EOF
		[01] Localhost   
		[02] Cloudflared
	EOF

	read -p "Select a port forwarding service : "

	case $REPLY in 
		1 | 01)
			start_localhost;;
		2 | 02)
			start_cloudflared;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 0.5
			tunnel_menu
			;;
	esac
}

init
dependencies
tunnel_menu
