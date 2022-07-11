#!/bin/bash
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

init(){
	chmod +x run.sh
}

pip_install
install_pkgs
init
