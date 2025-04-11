import tempfile
from typing import Any

from aiogram.types import Message


class PhotoProcessor:
    """PhotoProcessor class is responsible for processing photos.

    It handles saving photos to temporary files and converting them to the
    required format for detection.
    """

    @staticmethod
    async def save_photo_to_tempfile(data: dict[str, Any], message: Message) -> str:
        photo_file = await message.bot.get_file(data["predict_get_photo"])
        photo_bytes = await message.bot.download_file(photo_file.file_path)

        if hasattr(photo_bytes, "read"):
            photo_bytes = photo_bytes.read()
        else:
            return None, None

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(photo_bytes)
            tmp.flush()

        return tmp.name

