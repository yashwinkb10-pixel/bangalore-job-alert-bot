# send_daily_once.py
import os
import asyncio

from bangalore_job_alerts import build_daily_message
from telegram import Bot


async def main():
    bot_token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["CHAT_ID"]

    bot = Bot(token=bot_token)

    text = build_daily_message()

    await bot.send_message(chat_id=chat_id, text=text)


if __name__ == "__main__":
    asyncio.run(main())
