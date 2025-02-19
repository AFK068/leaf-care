from aiogram import Router

from bot.handlers import base_router, predict_router

main_router = Router()

main_router.include_routers(
    base_router,
    predict_router,
)
