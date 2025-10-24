Aadhaar Family Bot - Ready to Run (Simple ZIP)
---------------------------------------------

Files included:
- aadhaar_bot.py    : Main Python bot script
- .env              : Environment file with your TELEGRAM_TOKEN and API settings
- README.txt        : This file

Requirements:
- Python 3.8+
- pip install python-telegram-bot==13.15 requests python-dotenv

Steps to run locally (Linux / macOS / Windows with WSL recommended):

1) Extract the ZIP to a folder.
2) (Optional) Create a virtual environment:
   python -m venv venv
   source venv/bin/activate   (on Windows: venv\Scripts\activate)

3) Install dependencies:
   pip install python-telegram-bot==13.15 requests python-dotenv

4) Make sure the .env file contains your TELEGRAM_TOKEN (already filled).
   If you want to change API key or base, edit the .env file.

5) Run the bot:
   python aadhaar_bot.py

6) Open Telegram, search your bot username, send /start then send a 12-digit Aadhaar number.

Notes & Safety:
- This bot calls a public Aadhaar-linked family API. Use responsibly.
- Do not share your bot token publicly. If the token is compromised, regenerate it via BotFather.
- For production, consider deploying on a VPS and using webhook mode.

