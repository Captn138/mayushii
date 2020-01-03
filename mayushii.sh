#!/bin/bash
if [ $(dpkg -l|grep ffmpeg|wc -l) -lt 1 ]
then
	apt-get install ffmpeg
fi

if [ $(dpkg -l|grep python3|wc -l) -lt 1 ]
then
	apt-get install python3
fi

if [ $(dpkg -l|grep python3-pip|wc -l) -lt 1 ]
then
	apt-get install python3-pip
fi

if [ $(python3 -m pip list|grep discord|wc -l) -lt 1 ]
then
	python3 -m pip install discord.py
	python3 -m pip install discord.py[voice]
fi

if [ $(python3 -m pip list|grep PyNaCl|wc -l) -lt 1 ]
then
	python3 -m pip install PyNaCl
fi
echo ****************************************** >> python.log
date >> python.log
python3 bot.py >> python.log
