from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv()

btnUrlChannel = InlineKeyboardButton(text="Channel", url=os.getenv('CHANNEL_URL'))
channelMenu = InlineKeyboardMarkup(row_width=1)
channelMenu.insert(btnUrlChannel)
