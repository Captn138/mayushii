# mayushii
Personal simple administrative Bot for Discord written with discord.py

## Installation
```sh
sudo apt install ffmpeg
python3 -m pip install pip -U
python3 -m pip install discord-py dotenv -U
touch .env
chmod 400 .env
```

Edit the `.env` file to add `TOKEN=your_token_here`.

## Run
```python
python3 bot.py
```

## Ubuntu Users
It seems that `pip3` won't install `dotenv` package. You have to install it through `sudo apt install python3-dotenv`.