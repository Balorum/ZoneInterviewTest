#!/bin/bash

# Запуск FastAPI серверу на бекграунді
uvicorn server.api:app --host 0.0.0.0 --port 10000 &

# Запуск Telegram-бота
python3 bot/main.py