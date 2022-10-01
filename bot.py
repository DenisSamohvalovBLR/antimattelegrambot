from dotenv import load_dotenv
import os
import logging
import string
import json
from aiogram import Bot, Dispatcher, executor, types
import markups

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


def check_sub_channel(chat_member):
    return chat_member['status'] != "left"


@dp.message_handler(content_types=['new_chat_members'])
async def user_joined(message: types.Message):
    await message.answer("Welcome\nTo send messages, subscribe to the channel", reply_markup=markups.channelMenu)


@dp.message_handler()
async def mess_handler(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=os.getenv('CHANNEL_ID'), user_id=message.from_user.id)):
        text = message.text.lower()
        for word in os.getenv('WORDS'):
            if word in text:
                await message.delete()
    else:
        await message.answer("To send messages, subscribe to the channel", reply_markup=markups.channelMenu)
        await message.delete()


# Мой ID
@dp.message_handler(commands="test", commands_prefix="/")
async def test(message: types.Message):
    await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}")


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()


@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(
            set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
