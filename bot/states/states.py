from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    predict = State()
    predict_get_photo = State()