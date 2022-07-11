#!/bin/bash
source config

pip_install(){
	requirements=(
		fastapi
		pywal
		python-multipart
	)

	pip install $requirements
}

install_pkgs(){
	pkgs=(
		feh
		uvicorn
		xclip qrencode
	)
	checked=$(command -v $(printf "%s " ${pkgs[@]}) | wc -l)

	if [[ "${#pkgs[@]}" == "${checked}" ]]; then
		echo "package has been installed"
		return
	else
		for pkg in "${pkgs[@]}"; do
			type -p "$pkg" &>/dev/null || {
				echo -e "\nInstalling package : $pkg"
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

install_cloudflared() {
	download_cloudflared() {
		url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$1"
		file=`basename $url`

		[[ -e "$file" ]] && rm -rf "$file"

		wget --no-check-certificate "$url" > /dev/null 2>&1
		[[ ! -e "$file" ]] && echo -e "\n Error occured, Install Cloudflared manually."

		mv -f "$file" .server/cloudflared && chmod +x .server/cloudflared 
	}

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
	echo "Cloudflared has been install"
}

init(){
	[[ ! -d ".server" ]] && mkdir -p ".server"
	pip_install
	install_pkgs
	install_cloudflared

	chmod +x run.sh
}

init
