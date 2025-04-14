#!/bin/bash

# Запуск FastAPI серверу на бекграунді
gunicorn -w 4 -b 0.0.0.0:$PORT server.api:app &

# Запуск Telegram-бота
python3 bot/main.py