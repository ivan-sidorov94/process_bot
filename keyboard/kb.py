from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb = CallbackData("proc_name","proc")

def make_kb(items: list[str]):
    keyboard = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text=item, callback_data=cb.new(proc=item)) for item in items]
    keyboard.add(*buttons)
    return keyboard