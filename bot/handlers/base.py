from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink
from loguru import logger

base_router = Router(name=__name__)


@base_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"User with ID: {message.from_user.id} started bot")

    await message.answer(
        (
            f"👋 Привет, {hbold(message.from_user.full_name)}!\n\n"
            "🤖 Я бот, который поможет выявить заболевание по фотографии.\n\n"
            "🔍 Чтобы приступить к анализу, введите команду /predict\n\n"
            "❓ Если у вас есть вопросы по изпользованию, введите команду /help\n\n"
            "💻 Мой исходный код: {git_url}"
        ).format(git_url=hlink("Github", "https://github.com/AFK068/leaf-care")),
        reply_markup=ReplyKeyboardRemove(),
    )


@base_router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"User with ID: {message.from_user.id} requested help")

    await message.answer(("help"), reply_markup=ReplyKeyboardRemove())
