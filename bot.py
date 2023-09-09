import psutil
import os
import pyautogui
import logging
import asyncio
from config import admin_id ,TOKEN
from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from keyboard.kb import make_kb, cb

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop)

PROCESS_NAMES = ['Notepad.exe', 'CalculatorApp.exe', 'mspaint.exe']
notified = set()

async def check_process(dp):
    global notified
    while True:
        process_found = set()
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in PROCESS_NAMES:
                process_found.add(proc.info['name'])
        for name in process_found - notified:
            await bot.send_message(chat_id=admin_id, text=f'Процесс {name} запущен!')
        notified = process_found
        await asyncio.sleep(5)



class Kill_proc(StatesGroup):
    kill = State()




@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    if message.from_user.id == admin_id:
        process_list = []
        for proc in psutil.process_iter():
            if proc.name() not in process_list:
                process_list.append(proc.name())
        await bot.send_message(message.from_user.id, process_list)

@dp.message_handler(commands="kill")
async def cmd_kill(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        process_list = []
        for proc in psutil.process_iter():
            if proc.name() not in process_list:
                process_list.append(proc.name())
        process_list.sort()
        await message.answer(text="Выберите название процесса", reply_markup=make_kb(process_list))

@dp.message_handler(commands="screen")
async def cmd_screen(message: types.Message):
    if message.from_user.id == admin_id:
        screen = pyautogui.screenshot()
        screen.save(r'.\screen.jpg')
        photo = InputFile(".\screen.jpg")
        await bot.send_photo(admin_id, photo=photo)
        os.remove(".\screen.jpg")
        
@dp.callback_query_handler(cb.filter())
async def callbacks(call: types.CallbackQuery, callback_data: dict):
    program = callback_data["proc"]
    process_list = []
    for proc in psutil.process_iter():
        if proc.name() not in process_list:
            process_list.append(proc.name())
    if program in process_list:
        os.system("TASKKILL /F /IM "+program)
        await call.answer(text="Процесс "+ program + " закрыт", show_alert=True)
