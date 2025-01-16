from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot

def instance_bot(TOKEN: str) -> Bot:
    return Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 