import asyncio
import os
import sys

# Add the root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Dispatcher

from bot.bot_instance import instance_bot
from bot.logger import logger
from bot.routers import main_router
from bot.services.grpc.prediction import PredictClient
from bot.settings import settings


def register_routers(dp: Dispatcher) -> None:
    """Register routers."""
    dp.include_router(main_router)


async def main() -> None:
    dp = Dispatcher(bot=bot)
    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    bot = instance_bot(settings.BOT_TOKEN)

    async def run():
        client = await PredictClient.get_instance(
            host=settings.GRPC_HOST_LOCAL,
            port=settings.GRPC_PORT,
        )

        try:
            await client.connect()
        except ConnectionError as e:
            logger.error(f"Failed to connect to gRPC server: {e}")
            sys.exit(1)

        await main()

    asyncio.run(run())
