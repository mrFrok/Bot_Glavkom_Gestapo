from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    question1 = State()
    question2 = State()