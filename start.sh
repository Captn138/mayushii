#!/usr/bin/bash

set -e

if [[ $(python3 --version 2> /dev/null | awk -F. '{print $2}') -lt 10 && ! $(python3.10 --version 2> /dev/null) ]];
	cat << EOI >> /dev/stderr
Python 3.10 or greater is not installed!
Please install it using the following commands if your distro does not support this version via its packet manager:
wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
tar -xf Python-3.10.*.tgz
cd Python-3.10.*/
./configure --prefix=/usr/local --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j \$(nproc)
sudo make altinstall
EOI
        exit 1
fi

if [[ $(python3 --version 2>/dev/null | awk -F. '{print $2}') -ge 10 ]]
then
	PYTHON_BIN="python3"
else
	PYTHON_BIN="python3.$(compgen -c python3 | grep -v - | awk -F. '{print $2}' | grep -v -E \"$^\" | sort -rn | uniq | head -n 1)"
fi

$PYTHON_BIN -m venv ~/venv
pip3 install -r ~/bot/requirements.txt
cd ~/bot
tmux new-session -d -s mayushii python3 bot.py
