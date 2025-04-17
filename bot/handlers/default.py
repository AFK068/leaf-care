from aiogram import Router
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

default_router = Router(name=__name__)

@default_router.message()
async def handle_unknown_message(message: Message) -> None:
    """Handle unknown commands or text messages."""
    await message.answer(
        "❓ Я не понимаю эту команду или сообщение.\n"
        "Попробуйте использовать /help, чтобы узнать, что я могу сделать.",
        reply_markup=ReplyKeyboardRemove(),
    )
