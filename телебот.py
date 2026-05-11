import asyncio                                                                      
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BOT_TOKEN = '8631150033:AAF4dWJSwiQlLq_6uRMGThq2fipMow991dg'                #токен бота

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

tasks = {}

zametki = ['погладить', 'поспать']

flag_AI = False
flag_add = False
flag_del = False
flag_change2 = False

def main_keyboard():                            #клавиатура главное меню
    buttons = [
        [KeyboardButton(text='AI')],
        [KeyboardButton(text='заметки')],
        [KeyboardButton(text='напоминалка')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def back_keyboard():                                #клавиатура с кнопкой назад
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='назад')]], 
        resize_keyboard=True
    )

def zametki_keyboard():
    buttons = [
        [KeyboardButton(text='показать заметки')],
        [KeyboardButton(text='добавить заметки')],
        [KeyboardButton(text='удалить заметки')],
        [KeyboardButton(text='изменить заметки')],
        [KeyboardButton(text='назад')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def proverka(message):
    return all([message.text,
                message.text != 'AI',
                message.text != 'назад',
                message.text != 'заметки',
                message.text != 'напоминалка',
                message.text != 'показать заметки',
                message.text != 'добавить заметки',
                message.text != 'удалить заметки',
                message.text != 'назад'])


@dp.message(Command("start"))
async def start(message: Message):                              #главное меню
    await message.answer('Выберіте операцію',
    reply_markup=main_keyboard()
    )




def AI(user_message):                                     #поиск ответа у ии
    return f'по запросу {user_message} найдено:'

@dp.message(lambda message: message.text and message.text == 'AI')
async def ai_chat(message: Message):
    global flag_AI
    flag_AI = True                                                        # меню по первой кнопке
    await message.answer('Введите запрос', reply_markup=ReplyKeyboardRemove())
    
@dp.message(lambda message: proverka(message) and flag_AI)         
async def get_question(message: types.Message):                             # вывод ответа ИИ
    Answer = AI(message.text)
    await message.answer(Answer, reply_markup=back_keyboard())
    global flag_AI
    flag_AI = False





def show_zametki():
    answer = ''
    for i in range(len(zametki)):
        answer = answer + f'{i+1}. {zametki[i]} \n'
    return answer

def add_zametki(user_message):
    zametki.append(user_message)
    

def delete_zametki(index):
    del zametki[index-1]

def change_zametki(index, text):
    zametki[index-1] = text
    


#меню заметок

@dp.message(lambda message: message.text and message.text == 'заметки')
async def zametki_chat(message: Message):
    await message.answer('нажмите кнопку', reply_markup=zametki_keyboard())

#показ заметок
@dp.message(lambda message: message.text and message.text == 'показать заметки')
async def show_zametki_chat(message: Message):
    answer = show_zametki()
    await message.answer(answer, reply_markup=zametki_keyboard())

#функции по добавлению заметок
@dp.message(lambda message: message.text and message.text == 'добавить заметки')
async def add_zametki_chat(message: Message):
    await message.answer('Введите текст заметки', reply_markup=ReplyKeyboardRemove())
    global flag_add
    flag_add = True


@dp.message(lambda message: proverka(message) and flag_add)
async def adding_zametki(message: Message):
    if message.text != '':
        add_zametki(message.text)
        await message.answer('Заметка успешно добавлена!', reply_markup=zametki_keyboard())
        global flag_add
        flag_add = False
    else:
        await message.answer('Неверный формат ввода', reply_markup=zametki_keyboard())

#удаление заметок
@dp.message(lambda message: message.text and message.text == 'удалить заметки')
async def delete_zametki_chat(message: Message):
    await message.answer('Введите номер заметки, которую нужно удалить', reply_markup=ReplyKeyboardRemove())
    global flag_del
    flag_del = True
    answer = show_zametki()
    await message.answer(answer, reply_markup=ReplyKeyboardRemove())

@dp.message(lambda message: proverka(message) and flag_del)
async def deleting_zametki(message: Message):
    if (message.text).isdigit():
        index = int(message.text)
        if index > 0 and index <= len(zametki):
            delete_zametki(index)
            await message.answer('Заметка успешно удалена', reply_markup=zametki_keyboard())
        else:
            await message.answer('неверный номер', reply_markup=zametki_keyboard())
    else:
        await message.answer('Неверный формат ввода', reply_markup=zametki_keyboard())
    global flag_del
    flag_del = False

#изменение заметок

@dp.message(lambda message: message.text and message.text == 'изменить заметки')
async def change_zametki_chat(message: Message):
    await message.answer('Введите номер заметки, которую нужно изменить', reply_markup=ReplyKeyboardRemove())
    global flag_change2
    flag_change2 = True
    answer = show_zametki()
    await message.answer(answer, reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: proverka(message) and flag_change2)
async def changing_zametki(message: Message):
    if (message.text).isdigit():
        global index
        index = int(message.text)
        if index > 0 and index <= len(zametki):
            await message.answer('Введите текст изменённой заметки', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('неверный номер', reply_markup=zametki_keyboard())
    else:
        await message.answer('Неверный формат ввода', reply_markup=zametki_keyboard())
    global flag_change2
    flag_change2 = True


@dp.message(lambda message: proverka(message) and flag_change2)
async def changing_zametki(message: Message):
    change_zametki(index, message.text)
    await message.answer('Заметка успешно изменена', reply_markup=zametki_keyboard())
    global flag_change
    flag_change = True
    global flag_change2
    flag_change2 = True



@dp.message(lambda message: message.text and message.text == 'назад')
async def back(message: Message):
    await start(message)


async def reminder(chat_id:int):
    while True:
        await asyncio.sleep(5)  # Кожні 5 секунд (змініть на потрібне число)
        await bot.send_message(chat_id, 'nigger')


async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())