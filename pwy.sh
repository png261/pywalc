#!/bin/bash
public_url=""
HOST='127.0.0.1'
PORT='8080'

DEFAULT_TUNNEL="cloudflared"

## Directories
if [[ ! -d ".server" ]]; then
	mkdir -p ".server"
fi

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

## Kill already running process
kill_pid() {
	if [[ `pidof python` ]]; then
		killall python > /dev/null 2>&1
	fi
	if [[ `pidof ngrok` ]]; then
		killall ngrok > /dev/null 2>&1
	fi
	if [[ `pidof cloudflared` ]]; then
		killall cloudflared > /dev/null 2>&1
	fi
}

## Dependencies
dependencies() {
	if [[ `command -v python` && `command -v wget` && `command -v curl` && `command -v unzip` ]]; then
		return
	else
		pkgs=(python curl wget unzip)
		for pkg in "${pkgs[@]}"; do
			type -p "$pkg" &>/dev/null || {
				echo -e "\nInstalling package : "
				if [[ `command -v pkg` ]]; then
					pkg install "$pkg" -y
				elif [[ `command -v apt` ]]; then
					apt install "$pkg" -y
				elif [[ `command -v apt-get` ]]; then
					apt-get install "$pkg" -y
				elif [[ `command -v pacman` ]]; then
					sudo pacman -S "$pkg" --noconfirm
				elif [[ `command -v dnf` ]]; then
					sudo dnf -y install "$pkg"
				else
					echo -e "\nUnsupported package manager, Install packages manually."
				fi
			}
		done
	fi

	install_cloudflared
	install_ngrok

}

## Download Ngrok
download_ngrok() {
	url="$1"
	file=`basename $url`
	if [[ -e "$file" ]]; then
		rm -rf "$file"
	fi
	wget --no-check-certificate "$url" > /dev/null 2>&1
	if [[ -e "$file" ]]; then
		unzip "$file" > /dev/null 2>&1
		mv -f ngrok .server/ngrok > /dev/null 2>&1
		rm -rf "$file" > /dev/null 2>&1
		chmod +x .server/ngrok > /dev/null 2>&1
	else
		echo -e "\nError occured, Install Ngrok manually."
		{ reset_color; exit 1; }
	fi
}


## Download Cloudflared
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

## Install ngrok
install_ngrok() {
	if [[ -e ".server/ngrok" ]]; then
		return
	else
		echo -e "\nInstalling ngrok..."
		arch=`uname -m`
		if [[ ("$arch" == *'arm'*) || ("$arch" == *'Android'*) ]]; then
			download_ngrok 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip'
		elif [[ "$arch" == *'aarch64'* ]]; then
			download_ngrok 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm64.zip'
		elif [[ "$arch" == *'x86_64'* ]]; then
			download_ngrok 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
		else
			download_ngrok 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'
		fi
	fi

}


## Install Cloudflared
install_cloudflared() {
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


setup_site() {
	cd localhost && python run.py > /dev/null 2>&1 & 
}

## Start localhost
start_localhost() {
	setup_site
	echo -e "\nSuccessfully Hosted at : http://$HOST:$PORT "
	show_result
}

## Start Cloudflared
start_ngrok() { 
	setup_site 
	echo -ne "\nLaunching Ngrok..."
	sleep 2 && .server/ngrok http "$HOST":"$PORT" > /dev/null 2>&1 &
	sleep 8 &&
	public_url=$(curl -s -N  http://127.0.0.1:4040/api/tunnels | jq .tunnels[0].public_url)
	show_result
}

## Start Cloudflared
start_cloudflared() { 
	rm .cld.log > /dev/null 2>&1 &
	setup_site 
	echo -ne "\nLaunching Cloudflared..."
	sleep 2 && .server/cloudflared tunnel -url "$HOST":"$PORT" --logfile .cld.log > /dev/null 2>&1 &
	sleep 8 &&
	public_url=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ".cld.log")
	show_result
}

## Start localhost
show_result() {
	[[ -z "$public_url" ]] && return;
	echo -e "\nURL: $public_url"
	echo -e "\nQRCODE:\n"
	curl "qrcode.show/$public_url"

	# save to temp
	echo $public_url > /tmp/pwy_link
	qrencode -o /tmp/pwy_qrcode $public_url
}

## Tunnel selection
tunnel_menu() {
	clear 
	banner

	cat <<- EOF
		[01] Localhost   
		[02] Ngrok.io    
		[03] Cloudflared
	EOF

	read -p "Select a port forwarding service : "

	case $REPLY in 
		1 | 01)
			start_localhost;;
		2 | 02)
			start_ngrok;;
		3 | 03)
			start_cloudflared;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 1
			tunnel_menu
			;;
	esac
}

copy_menu(){
	clear 
	banner

	cat <<- EOF
		[01] Link   
		[02] QRCODE
	EOF

	read -p "Select thing to copy: "

	case $REPLY in 
		1 | 01)
			xclip -se c -i /tmp/pwy_link
			echo "Copied Link"	
			;;
		2 | 02)
			xclip -se c -t image/png -i /tmp/pwy_qrcode
			echo "Copied Qrcode" 
			;;
		*)
			echo -ne "\nInvalid Option, Try Again...\n"
			sleep 1
			copy_menu
			;;
	esac
}

#Main
kill_pid
dependencies
main
tunnel_menu
# copy_menu
