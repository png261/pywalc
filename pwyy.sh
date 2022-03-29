#!/bin/bash

## Directories
if [[ ! -d ".server" ]]; then
	mkdir -p ".server"
fi

if [[ -e ".cld.log" ]]; then
	rm -rf ".cld.log"
fi

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
	if [[ `command -v php` && `command -v wget` && `command -v curl` && `command -v unzip` ]]; then
		echo -e "\nPackages already installed."
	else
		pkgs=(php curl wget unzip)
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

## Install Cloudflared
install_cloudflared() {
	if [[ -e ".server/cloudflared" ]]; then
		echo -e "\nCloudflared already installed."
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

## Setup website and start php server
HOST='127.0.0.1'
PORT='8080'

setup_site() {
	echo -e "\nSetting up server..."
	echo -ne "\nStarting PHP server..."
	cd localhost && python run.py > /dev/null 2>&1 & 
}


## Start Cloudflared
start_cloudflared() { 
	rm .cld.log > /dev/null 2>&1 &
	echo -e "\nInitializing... (http://$HOST:$PORT )"
	{ sleep 1; setup_site; }
	echo -ne "\n\nLaunching Cloudflared..."
	sleep 2 && .server/cloudflared tunnel -url "$HOST":"$PORT" --logfile .cld.log > /dev/null 2>&1 &
	sleep 10 &&
	cldflr_link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ".cld.log")
	echo -ne "\n\n Done!!"
	echo -e "\nURL: $cldflr_link"
}

## Start localhost
start_localhost() {
	echo -e "\nInitializing... ( http://$HOST:$PORT )"
	setup_site
	echo -e "\nSuccessfully Hosted at : http://$HOST:$PORT "
}

## Main
kill_pid
dependencies
install_cloudflared
start_cloudflared
