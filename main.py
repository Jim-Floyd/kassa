import asyncio
from datetime import datetime
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
from data_base import sqlite_db
from aiogram.filters.callback_data import CallbackData





router = Router()





# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6210899072:AAEd5aK-E0BKwD-Hv9NadIk1HH3km1rumoI"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


class Income_types(StatesGroup):
    income_type = State()
    user_id = State()

class Cost_types(StatesGroup):
    cost_type = State()
    user_id = State()

class Income(StatesGroup):
    income_type = State()
    income_amount = State()
    transaction_date = State()
    cost_type = State()
    cost_amount = State()
    user_id = State()


class Balance(StatesGroup):
    year = State()
    month = State()




def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


income_types = []
income_amounts = []

#---------------DB ga ulanish--------------------
async def on_startup(_):
    await sqlite_db.sql_start()
    print('DBga ulanmoqda')


kb=[
    [types.KeyboardButton(text='Daromadlar'), types.KeyboardButton(text='Xarajatlar')], [types.KeyboardButton(text='Balans')]
    ]


kb1=[
    [types.KeyboardButton(text='Daromad turini qo`shish'), types.KeyboardButton(text='Daromad qo`shish')], [types.KeyboardButton(text="Jami daromadlar"), types.KeyboardButton(text='Bosh sahifaga')]
    ]


kb2=[
    [types.KeyboardButton(text='Xarajat turini qo`shish'), types.KeyboardButton(text='Xarajat qo`shish')], [types.KeyboardButton(text="Jami xarajatlar"), types.KeyboardButton(text='Bosh sahifaga')]
    ]


@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await state.clear()
    kb_client = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer('Salom, kassaga xush kelibsiz!', reply_markup=kb_client)


@dp.message(F.text == "Bosh sahifaga")
async def main_page(message: types.Message, state: FSMContext):
    state.clear()
    await start_command(message, state)


@dp.message(F.text == "Daromadlar")
async def income_command(message: types.Message):
    
    kb_client = types.ReplyKeyboardMarkup(keyboard=kb1, resize_keyboard=True)
    await message.answer('soqqa tushdimi?))', reply_markup=kb_client)


@dp.message(F.text == "Xarajatlar")
async def cast_command(message: types.Message):
    
    kb_client = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
    await message.answer('soqqa ketdimi?))', reply_markup=kb_client)



#-----------------DAROMAD TURINI QO'SHISH-------------------

@dp.message(F.text == "Daromad turini qo`shish")
async def add_income_type(message: Message, state: FSMContext):
    await message.answer(text='Daromad turini kiriting:')
    await state.set_state(Income_types.income_type)



@dp.message(Income_types.income_type)
async def type_chosen(message: Message, state: FSMContext):
    await state.update_data(income_type=message.text.lower())
    await state.update_data(user_id=message.from_user.id)
    user_data = await state.get_data()
    await message.answer(text=f'Siz qo`shgan tur: {user_data["income_type"]}')
    await sqlite_db.sql_add_income_type_command(state)
    await state.clear()



#-----------------XARAJAT TURINI QO'SHISH-------------------

@dp.message(F.text == "Xarajat turini qo`shish")
async def add_cost_type(message: Message, state: FSMContext):
    await message.answer(text='Xarajat turini kiriting:')
    await state.set_state(Cost_types.cost_type)



@dp.message(Cost_types.cost_type)
async def type_chosen(message: Message, state: FSMContext):
    await state.update_data(cost_type=message.text.lower())
    await state.update_data(user_id=message.from_user.id)
    user_data = await state.get_data()
    await message.answer(text=f'Siz qo`shgan tur: {user_data["cost_type"]}')
    await sqlite_db.sql_add_cost_type_command(state)
    await state.clear()
 



#-----------------DAROMAD QO'SHISH-------------------

@dp.message(F.text == "Daromad qo`shish")
async def add_income(message: Message, state: FSMContext):
    user_data = await state.get_data()
    type_list = await sqlite_db.income_types(message)
    stop = 'Bosh sahifaga'
    type_list.append(stop)
    await message.answer(
        text="Daromad turini tanlang:",
        reply_markup=make_row_keyboard(type_list)
    )
    print(message.text.lower())
    await state.set_state(Income.income_type)





@dp.message(Income.income_type)
async def add_income_amount(message: Message, state: FSMContext):
    print(message.text.lower())
    await state.update_data(income_type=message.text.lower())
    await message.answer(
        text="Daromad summasini kiriting:", reply_markup=ReplyKeyboardRemove()
    )
    print(message.text.lower())
    await state.set_state(Income.income_amount)


@dp.message(Income.income_amount)
async def reply_msg_income(message: Message, state: FSMContext):
    await state.update_data(income_amount=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Siz {message.text.lower()} summadagi {user_data['income_type']} turdagi daromadni qo'shdingiz.")
    await state.update_data(transaction_date=str(datetime.now()))
    await state.update_data(cost_type=None)
    await state.update_data(cost_amount=0)
    await state.update_data(user_id=message.from_user.id)
    await sqlite_db.sql_add_transaction_command(state)
    print(message.text.lower())
    await add_income(message, state)
    

#-----------------XARAJAT QO'SHISH-------------------

@dp.message(F.text == "Xarajat qo`shish")
async def add_cost(message: Message, state: FSMContext):
    user_data = await state.get_data()
    type_list = await sqlite_db.cost_types(message)
    stop = 'Bosh sahifaga'
    type_list.append(stop)
    await message.answer(
        text="Xarajat turini tanlang:",
        reply_markup=make_row_keyboard(type_list)
    )
    print(message.text.lower())
    await state.set_state(Income.cost_type)


@dp.message(Income.cost_type)
async def add_cost_amount(message: Message, state: FSMContext):
    print(message.text.lower())
    await state.update_data(income_type=None)
    await state.update_data(income_amount=0)
    await state.update_data(transaction_date=str(datetime.now()))
    await state.update_data(cost_type=message.text.lower())
    await message.answer(
        text="Xarajat summasini kiriting:", reply_markup=ReplyKeyboardRemove()
    )
    print(message.text.lower())
    await state.set_state(Income.cost_amount)

#@dp.message(F.text == "Bosh sahifaga")
#async def main_page(message: types.Message, state: FSMContext):
#    state.clear()
#    await start_command(message)

@dp.message(Income.cost_amount)
async def reply_msg_cost(message: Message, state: FSMContext):
    await state.update_data(cost_amount=int(message.text.lower())*(-1))
    await state.update_data(user_id=message.from_user.id)
    user_data = await state.get_data()
    await message.answer(
        text=f"Siz {message.text.lower()} summadagi {user_data['cost_type']} turdagi xarajatni qo'shdingiz.")
    await sqlite_db.sql_add_transaction_command(state)
    print(message.text.lower())
    await add_cost(message, state)
    
    
    
    

#-----------------JAMI DAROMAD-------------------

@dp.message(F.text == "Jami daromadlar")
async def income_list(message: Message, state: FSMContext):
    
    type_list = await sqlite_db.all_transactions(message)
    print(type_list)
    for trans in type_list:
        if trans[0] != None and trans[5]==message.from_user.id:
            await message.answer(text=f'daromad turi: {trans[0]}, summa: {trans[1]}')



#-----------------JAMI XARAJAT-------------------

@dp.message(F.text == "Jami xarajatlar")
async def cost_list(message: Message, state: FSMContext):
    type_list = await sqlite_db.all_transactions(message)
    for trans in type_list:
        if trans[3] != None and trans[5]==message.from_user.id:
            await message.answer(text=f'xarajat turi: {trans[3]}, summa: {trans[4]*(-1)}')



#-----------------BALANS-------------------

@dp.message(F.text == "Balans")
async def choose_year(message: Message, state: FSMContext):
    type_list = await sqlite_db.all_transactions(message)
    year_list = []
    for trans in type_list:
        year = datetime.strptime(trans[2], '%Y-%m-%d %H:%M:%S.%f').year
        year_list.append(str(year))
    year_list2 = []
    [year_list2.append(x) for x in year_list if x not in year_list2]
    await message.answer(
        text="Yilni tanlang:",
        reply_markup=make_row_keyboard(year_list2)
    )
    await state.set_state(Balance.year)


@dp.message(Balance.year)
async def choose_month(message: Message, state: FSMContext):
    await state.update_data(year=message.text.lower())
    type_list = await sqlite_db.all_transactions(message)
    month_list = []
    for trans in type_list:
        month = datetime.strptime(trans[2], '%Y-%m-%d %H:%M:%S.%f').month
        month_list.append(str(month))
    month_list2 = []
    [month_list2.append(x) for x in month_list if x not in month_list2]
    await message.answer(
        text="Oyni tanlang:",
        reply_markup=make_row_keyboard(month_list2)
    )
    await state.set_state(Balance.month)


@dp.message(Balance.month)
async def choose_month(message: Message, state: FSMContext):
    await state.update_data(month=message.text.lower())
    type_list = await sqlite_db.all_transactions(message)
    user_data = await state.get_data()
    overall = 0
    for trans in type_list:
        if trans[5]==message.from_user.id:
            if str(datetime.strptime(trans[2], '%Y-%m-%d %H:%M:%S.%f').year) == user_data['year']:
                if str(datetime.strptime(trans[2], '%Y-%m-%d %H:%M:%S.%f').month) == user_data['month']:
                    if trans[3] != None:
                        await message.answer(text=f'xarajat turi: {trans[3]}, summa: {trans[4]*(-1)}')
                    else:
                        await message.answer(text=f'daromad turi: {trans[0]}, summa: {trans[1]}')
                    overall = overall+trans[4]+trans[1]
    await message.answer(text=f'Jami: {overall}', reply_markup=make_row_keyboard(['Bosh sahifaga']))
    await state.clear()

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())