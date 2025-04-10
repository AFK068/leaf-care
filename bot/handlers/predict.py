import grpc
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from states import Form

from bot.logger import logger
from bot.services import (
    DetectHandler,
    PhotoProcessor,
    PlantDiagnostics,
    PredictionService,
)

predict_router = Router(name=__name__)


@predict_router.message(Command("predict"))
async def cmd_predict(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите тип растения для дальнейшего анализа:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Помидор"), KeyboardButton(text="Огурец")],
                [KeyboardButton(text="Дыня"), KeyboardButton(text="Арбуз")],
                [KeyboardButton(text="Клубника"), KeyboardButton(text="Перец")],
            ],
            resize_keyboard=True,
        ),
    )

    await state.set_state(Form.predict)


@predict_router.message(Form.predict)
async def handle_plant_selection(message: Message, state: FSMContext) -> None:
    await state.update_data(predict=message.text)
    data = await state.get_data()

    if data["predict"] not in [
        "Помидор",
        "Дыня",
        "Клубника",
        "Огурец",
        "Арбуз",
        "Перец",
    ]:
        await message.answer("❌ Вы выбрали неверное растение.")
        await cmd_predict(message, state)
        return

    await message.answer(
        f"Вы выбрали: {data['predict']}\nТеперь отправьте фото для анализа:",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(Form.predict_get_photo)


@predict_router.message(Form.predict_get_photo, F.photo)
async def handle_get_photo(message: Message, state: FSMContext) -> None:
    await state.update_data(predict_get_photo=message.photo[-1].file_id)
    data = await state.get_data()

    # Save the photo to a temporary file.
    try:
        image_path = await PhotoProcessor.save_photo_to_tempfile(
            data=data,
            message=message,
        )
    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        await message.answer("❌ Ошибка при обработке фото.")
        return

    await message.answer("🔄 Идет анализ фото...")

    # Detect objects in the image.
    try:
        detect_handler = await DetectHandler.get_instance(
            model_path="models/leaf_detect.pt",
        )

        detection_boxes, photo = await detect_handler.detect(image_path)
        detection_count = len(detection_boxes)

        if detection_count:
            logger.info(f"Detected {detection_count} objects.")
            await message.answer(f"Обнаружено объектов: {detection_count}")
        else:
            logger.info("No objects detected.")
            await message.answer("Объекты не обнаружены. Попробуйте другое фото.")
            return

        await message.reply_photo(
                photo=photo,
                caption="🔍 Обнаруженные объекты",
            )

        await state.clear()

    except Exception as e:
        logger.error(f"Error during detection: {e}")
        await message.answer("❌ Ошибка при обнаружении объектов.")
        await state.clear()
        return

    # Make predictions based on the detected objects.
    try:
        predict_result = await PredictionService.predict(
            data=data,
            detection_boxes=detection_boxes,
        )

        plant_diagnostics = PlantDiagnostics()
        report = await plant_diagnostics.analyze_and_report(
            results=predict_result,
            plant_type=data["predict"].lower(),
        )

        if not report:
            await message.answer("❌ Что-то пошло не так. Отчет пуст, повторите попытку позже.")
        else:
            for item in report:
                await message.answer(item)

    except ConnectionError as e:
        await message.answer("❌ Не удалось подключиться к серверу. Попробуйте позже.")
        logger.error(f"Connection error: {e}")
        await state.clear()
    except grpc.RpcError as e:
        error_message = f"❌ Ошибка сервера: {e.details()}"
        await message.answer(error_message)
        logger.error(f"gRPC error: {e}")
        await state.clear()
    except Exception as e:
        await message.answer("❌ Произошла непредвиденная ошибка. Попробуйте еще раз.")
        logger.error(f"Unexpected error: {e}")
        await state.clear()


@predict_router.message(Form.predict_get_photo)
async def handle_invalid_input(message: Message) -> None:
    """Handle invalid input when a photo is expected."""
    await message.answer("❌ Я ожидаю фотографию. Пожалуйста, отправьте фото для анализа.")
