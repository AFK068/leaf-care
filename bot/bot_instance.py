from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def instance_bot(TOKEN: str) -> Bot:
    return Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
