from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink
from loguru import logger

base_router = Router(name=__name__)


@base_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Handle the /start command.

    Clear the state and send a welcome message to the user.
    """
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
async def cmd_help(message: Message, state: FSMContext) -> None:
    """Handle the /help command.

    Clear the state and send a help message to the user.
    """
    await state.clear()
    logger.info(f"User with ID: {message.from_user.id} requested help")

    await message.answer(
        (
            "🛠 <b>Доступные команды:</b>\n\n"
            "🔹 <b>/start</b> — перезапускает бота и выводит приветственное сообщение.\n"
            "🔹 <b>/help</b> — показывает список доступных команд и инструкцию по "
            "использованию.\n"
            "🔹 <b>/predict</b> — запустит процесс анализа фотографии "
            "на наличие признаков заболеваний.\n\n"
            "📸 <b>Рекомендации по отправке изображения для анализа:</b>\n\n"
            "📌 Лучше всего отправлять фото одного листа растения крупным планом — это "
            "повышает точность распознавания.\n\n"
            "📌 Однако можно отправить и изображение всего растения — бот "
            "автоматически определит и выделит каждый лист, после чего "
            "проанализирует их по отдельности.\n\n"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

