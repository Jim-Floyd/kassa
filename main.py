import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from config import BOT_TOKEN
from aiogram.types import ReplyKeyboardMarkup,  ReplyKeyboardRemove
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext



router = Router()





# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6210899072:AAEd5aK-E0BKwD-Hv9NadIk1HH3km1rumoI"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


class Income_types(StatesGroup):
    income_type = State()


class Income(StatesGroup):
    income_type = State()
    income_amount = State()
    income_date = State()



def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


income_types = ['Sotuv', 'Xizmat ko`rsatish']


@dp.message(Command("start"))
async def start_command(message: types.Message):
    kb=[
    [types.KeyboardButton(text='Daromadlar'), types.KeyboardButton(text='Xarajatlar')], [types.KeyboardButton(text='Balans')]
    ]
    kb_client = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Salom, kassaga xush kelibsiz!', reply_markup=kb_client)


@dp.message(F.text == "Daromadlar")
async def income_command(message: types.Message):
    kb=[
    [types.KeyboardButton(text="Jami_daromadlar"), types.KeyboardButton(text='Daromad_qo`shish')], [types.KeyboardButton(text='Daromad_turini_qo`shish')]
    ]
    kb_client = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('daromading 200$', reply_markup=kb_client)


@dp.message(F.text == "Daromad_turini_qo`shish")
async def add_income_type(message: Message, state: FSMContext):
    await message.answer(text='Daromadni kiriting:')
    
    
    await state.set_state(Income_types.income_type)


@dp.message(Income_types.income_type)
async def type_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    user_data = await state.get_data()
    await message.answer(text=f'Siz qo`shgan tur: {user_data}')  
    await state.update_data(chosen_income=message.text.lower()) 
    await state.clear()


@dp.message(F.text == "Daromad_qo`shish")
async def add_income_type(message: Message, state: FSMContext):
    await message.answer(text='Daromadni turini tanlang:')
    
    
    await state.set_state(Income_types.income_type)


@dp.message(Income_types.income_type)
async def type_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    user_data = await state.get_data()
    await message.answer(text=f'Siz qo`shgan tur: {user_data}')  
    await state.update_data(chosen_income=message.text.lower()) 
    await state.clear()


@dp.message(Command("Xarajatlar"))
async def cost_command(message: types.Message):
    await message.answer('xarajating 100$')




async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())