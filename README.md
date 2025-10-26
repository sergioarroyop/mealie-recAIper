# Mealie Reciper Bot

Telegram bot that receive cooking videos links, transcribes the audio, and generates structured Mealie recipes using OpenAI. Audio transcription can run through ElevenLabs (if the token is present) or fall back to Whisper. The resulting recipe is pushed directly to a Mealie instance.

## Features

- Downloads audio with `yt-dlp` from supplied video URLs.
- Transcribes speech with ElevenLabs Scribe or Whisper depending on configured tokens.
- Builds a Spanish recipe prompt and generates schema.org compliant JSON-LD via OpenAI.
- Creates the recipe in Mealie automatically and cleans temporary audio files.

## Requirements

- Python 3.10+
- `ffmpeg` (required for audio conversion when running locally)
- A Mealie instance with API access
- Telegram bot token to receive channel posts
- OpenAI API access (mandatory), ElevenLabs API access (optional)

## Environment Variables

These can be placed in a `.env` file or exported in your shell before starting the bot.

| Variable | Required | Description |
| --- | --- | --- |
| `BOT_TOKEN` | ✅ | Telegram bot token. |
| `OPENAI_TOKEN` | ✅ | OpenAI API key for recipe generation. |
| `MEALIE_TOKEN` | ✅ | Mealie API token used to create recipes. |
| `MEALIE_API_URL` | ✅ | Base URL of your Mealie instance (e.g. `https://mealie.example.com`). |
| `ELEVENLABS_TOKEN` | ⛔ | ElevenLabs API key; when absent the bot falls back to Whisper. |
| `WHISPER_MODEL` | ⛔ | Whisper model name (default: `medium`) when no ElevenLabs token is supplied. |
| `EXTRA_PROMPT` | ⛔ | Additional instructions appended to the recipe prompt. |

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env  # if you maintain one
# edit .env with the tokens described above
python code/main.py
```

The bot listens for messages sent to the configured Telegram channel. Ensure your bot is permitted to read channel posts and that temporary audio files in `/tmp` are writable.

## Docker

The repository includes a ready-to-use Docker setup.

```bash
docker compose up --build -d
```

Place your environment variables in a `.env` file next to `docker-compose.yml`. The container installs `ffmpeg`, the Python dependencies, and starts the bot.

## Project Structure

```
code/
├── bot/                # Telegram router and handlers
├── config/             # Settings loader (dotenv)
├── lib/                # Mealie, AI, cleaner, and YT-DLP helpers
└── main.py             # Application entrypoint and client initialization
```

## Logging & Troubleshooting

- Logs are emitted to stdout with emoji markers for major steps.
- When using Docker, check logs with `docker compose logs -f bot`.
- If transcription fails, verify your ElevenLabs or Whisper configuration and confirm `ffmpeg` is available.
- Mealie HTTP errors include the API response in the logs for easier debugging.
