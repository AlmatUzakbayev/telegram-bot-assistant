# Telegram Bot Assistant

A Telegram assistant that answers text questions, voice messages and photos using
Google Gemini. Built in November 2024 as my first project combining a Telegram bot,
a FastAPI backend and an LLM.

## Features

- **Text** — answers a question with a detailed explanation (Gemini via LangChain)
- **Voice** — a voice message is sent to Gemini as audio; the bot answers the question
  or solves the problem it contains
- **Photo** — analyzes an image: solves a task step by step, explains a book page or
  summarizes the content

## Architecture

```
Telegram user
      ↓
Aiogram bot (bot/app/tg_app.py)
      ↓  HTTP
FastAPI backend (bot/app/app.py)
      ↓
Google Gemini (bot/chatgenerator.py)
```

| Endpoint | Request body | Purpose |
|----------|--------------|---------|
| `POST /chat/ask` | `{"user_input": "..."}` | Text question |
| `POST /chat/voice` | `{"file_path": "..."}` | Voice message (OGG file saved by the bot) |
| `POST /chat/image` | `{"image_input": "..."}` | Photo (file saved by the bot) |

## Tech Stack

Python · FastAPI · aiogram 3 · LangChain · Google Gemini · pydub / ffmpeg · Docker

## Running

1. Create a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_token
GOOGLE_API_KEY=your_google_key
```

2. With Docker (the image installs ffmpeg):
```bash
docker-compose up --build
```

Or locally (ffmpeg must be installed):
```bash
pip install -e .
run_bot
```

`run_bot` starts the FastAPI backend on port 8000 and the Telegram bot together.

## Notes

This is an early project and is kept as it was written in 2024. It uses
`gemini-1.5-flash` through the `google-generativeai` SDK; Google has since retired
that model and replaced the SDK with `google-genai`. My later projects use the current SDK:
[company-analyzer](https://github.com/AlmatUzakbayev/company-analyzer) and
[AI-VET](https://github.com/AlmatUzakbayev/AI-VET).
