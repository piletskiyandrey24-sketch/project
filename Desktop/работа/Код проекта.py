import os
import requests
from dotenv import load_dotenv
import json
import asyncio                                                                      
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")                #токен бота

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

tasks = {}
active_napominaniya = {}
user_data = {}

#********СПИСОК ЗАПРЕЩЁННОЙ ЛЕКСИКИ********

FORBIDDEN_WORDS = [
    # Наркотики и психоактивные вещества
    'наркотик', 'наркота', 'наркобизнес', 'наркоторговля',
    'мефедрон', 'амфетамин', 'кокаин', 'героин', 'марихуана', 'гашиш',
    'спайс', 'соль', 'экстази', 'лсд', 'метамфетамин',
    'закладка', 'клад', 'шоп', 'гидра', 'вещество',
    'психоактивный', 'дурь', 'травка', 'бошки', 'шишки',

    # Оружие и взрывчатка
    'оружие', 'огнестрельное', 'автомат', 'пистолет', 'винтовка', 'карабин',
    'взрывчатка', 'взрывное устройство', 'тротил', 'динамит', 'самодельное взрывное устройство',
    'боеприпасы', 'патроны', 'граната', 'мина', 'коктейль молотова',
    'нож', 'арбалет', 'кастет', 'баллончик', 'травмат', 'нарезное',
    'браконьерство', 'незаконная охота',

    # Терроризм и экстремизм
    'терроризм', 'террористический', 'экстремизм', 'экстремистский',
    'исламское государство', 'игил', 'талибан', 'аль-каида',
    'нацизм', 'фашизм', 'расизм', 'ксенофобия',
    'националистический', 'скинхед', 'кровь', 'геноцид',

    # Незаконный игорный бизнес
    'казик',
    'казино', 'игровой автомат', 'букмекерская контора', 'тотализатор', 'покер',
    'онлайн-казино', 'слоты', 'рулетка', 'блекджек',

    # Финансовые преступления
    'финансовая пирамида', 'пирамида', 'форекс', 'хайп', 'инвестиционный проект',
    'обнал', 'обналичивание', 'фиктивный', 'отмывание денег', 'схема',
    'денежный суррогат', 'криптовалюта', 'биткоин', 'эфириум', 'майнинг', 'криптобиржа',
    'чёрный обнал', 'серый обнал', 'доля', 'пассивный доход', 'супердоход',

    # Мошенничество
    'мошенничество', 'афера', 'надувательство', 'фальшивый', 'поддельный',
    'фишинг', 'взлом', 'кардинг', 'скимер', 'слепой платеж',
    'нигерийское письмо', 'фейковый', 'скам', 'лохотрон',

    # Противоправные действия в сфере интимных услуг
    'проституция', 'бордель', 'интим', 'эскорт', 'секс за деньги',
    'сутенер', 'сводник', 'публичный дом',

    # Нарушение авторских прав и контрафакт
    'контрафакт', 'подделка', 'реплика', 'копия бренда', 'паленый',
    'серый импорт', 'нелицензионный', 'пиратка', 'кряк', 'активатор',

    # Иное
    'незаконный', 'противозаконный', 'преступный', 'уголовный',
    'обход закона', 'дыра в законе', 'коррупция', 'взятка',
    'рабство', 'торговля людьми', 'детское порно', 'жестокое обращение'
]

#*****************СОХРАНЕНИЕ И ЗАГРУЗКА*************

def load_data():
    global user_data
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        user_data = {}

        for chat_id_str, user_info in data.items():
            chat_id = int(chat_id_str)
            zametki = user_info.get('заметки', [])
        
            napominalki = []
            if 'напоминания' in user_info:
                for item in user_info['напоминания']:
                    text, date_str = tuple(item)
                    date = datetime.fromisoformat(date_str)
                    napominalki.append((text, date))

            flags = {'flag_AI': False,
                        'flag_add': False,
                        'flag_del': False,
                            'flag_change': False,
                            'flag_change2': False, 
                            'flag_add_nap1': False,
                            'flag_add_nap2': False,
                            'flag_del_nap': False
                            }
            
            history = user_info.get('история', [])

            user_data[chat_id] = {'заметки': zametki, 'напоминания': napominalki, 'флаги': flags, 'история': history}
    except FileNotFoundError:
        user_data = {}
        save_data()


def save_data():
    data = {}
    for chat_id, info in user_data.items():
        napominalki = []
        for text, date in info['напоминания']:
            napominalki.append((text, date.isoformat()))
        data[str(chat_id)] = {
            'заметки': info['заметки'],
            'напоминания': napominalki,
            'история': info['история']
        }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#*********************КЛАВИАТУРЫ*******************

def main_keyboard():                            #клавиатура главное меню
    buttons = [
        [KeyboardButton(text='💼 Бизнес-советник')],
        [KeyboardButton(text='📚 Заметки')],
        [KeyboardButton(text='📅 Планировщик')],
        [KeyboardButton(text='❓ Помощь')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def back_keyboard():
    buttons = [
        [KeyboardButton(text='◀️ Назад')]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def end_keyboard():
    buttons = [
        [KeyboardButton(text='✅ Готово'),
         KeyboardButton(text='🗑️ Очистить диалог')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
def zametki_keyboard():
    buttons = [
        [KeyboardButton(text='📋 Показать заметки')],
        [KeyboardButton(text='✏️ Добавить заметку')],
        [KeyboardButton(text='🗑️ Удалить заметку')],
        [KeyboardButton(text='🔄 Изменить заметку')],
        [KeyboardButton(text='◀️ Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def napominalka_keyboard():
    buttons = [
        [KeyboardButton(text='📋 Показать напоминания')],
        [KeyboardButton(text='✏️ Добавить напоминание')],
        [KeyboardButton(text='🗑️ Удалить напоминание')],
        [KeyboardButton(text='◀️ Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

#***************************ПРОВЕРКИ*****************


def proverka_flags(message):
    chat_id = message.chat.id
    FLAG = True
    for flag in user_data[chat_id]['флаги']:
        if user_data[chat_id]['флаги'][flag] == True:
            FLAG = False
            break
    return FLAG

#****************НАЧАЛО РАБОТЫ****************
@dp.message(Command("start"))
async def start(message: Message):
    load_data() 
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {
            'заметки': [],
            'напоминания': [],
            'флаги': {
                'flag_AI': False,
                'flag_add': False,
                'flag_del': False,
                'flag_change': False,
                'flag_change2': False,
                'flag_add_nap1': False,
                'flag_add_nap2': False,
                'flag_del_nap': False
            },
            'история': []
        }
        save_data()
    # Запускаем отдельную задачу reminder для каждого пользователя
    if chat_id not in tasks:
        task = asyncio.create_task(reminder(chat_id))
        tasks[chat_id] = task
        print(f"Запущена задача напоминаний для пользователя {chat_id}")
    await message.answer("✨ *Добро пожаловать в Business Assistant Bot!* ✨\n\n"
        "Я — ваш виртуальный бизнес-партнёр и помощник в генерации идей. "
        "Помогаю продумывать бизнес-решения, структурировать мысли и ничего не забывать.\n\n"
        "📌 *Кнопки главного меню*:\n"
        "• 💼 *Бизнес-советник* — консультации по бизнесу, генерация идей, анализ решений\n"
        "• 📚 *Заметки* — храните важные мысли, списки, идеи\n"
        "• 📅 *Планировщик* — установите дату и время, я напомню\n"
        "• ❓ *Помощь* — краткая инструкция по использованию\n\n")
    await main_menu(message)


async def main_menu(message: Message):   #главное меню
    await message.answer('👇 Выберите действие в меню ниже',
    reply_markup=main_keyboard()
    )


#****************************ФУНКЦИЯ РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ*********************
@dp.message(lambda message: message.text and message.text == '❓ Помощь' and proverka_flags(message))      
async def rukovodstvo(message: Message):
    instruction_text = (
        "📖 *Руководство пользователя*\n\n"
        "💼 *Бизнес-советник*\n"
        "• Задайте любой вопрос о бизнесе, идеях или решениях\n"
        "• Я помогу проанализировать ситуацию и предложить варианты\n"
        "• Кнопка «🗑️ Очистить диалог» — сбрасывает контекст диалога\n"
        "• Кнопка «✅ Готово» — завершает сеанс и возвращает в меню\n"
        "✨ *Совет:* Чем подробнее вы опишете свою задачу, тем точнее будет мой ответ!\n\n"
        "📚 *Заметки*\n"
        "• «📋 Показать заметки» — просмотр всех сохранённых заметок\n"
        "• «✏️ Добавить заметку» — введите текст, и я сохраню\n"
        "• «🗑️ Удалить заметку» — выберите номер заметки для удаления\n"
        "• «🔄 Изменить заметку» — выберите номер и введите новый текст\n\n"
        
        "📅 *Планировщик*\n"
        "• «📋 Показать напоминания» — список всех запланированных напоминаний\n"
        "• «✏️ Добавить напоминание» — сначала текст, затем дата и время\n"
        "• Формат даты: ГГГГ-ММ-ДД ЧЧ:ММ (пример: 2026-05-20 14:30)\n"
        "• «🗑️ Удалить напоминание» — выберите номер для удаления\n\n"
        
        "🔄 *Общие команды*\n"
        "• «назад» — отмена текущего действия и возврат в меню\n"
        "• /start — перезапустить бота\n\n"
        )                                     
    await message.answer(instruction_text, reply_markup=back_keyboard())
#**************************💼 Бизнес-советник**********************


system_prompt = "Ты виртуальный бизнес-партнер. Пользователь захочет " \
"проконсультироваться с тобой по поводу открытия бизнеса, или захочет получить совет " \
"по принятию какого-нибудь бизнес-решения. У него чаще всего есть возможности, но нет идей. На основе его просьбы и данных сформулируй " \
"чёткий и ясный ответ. Будь дружелюбен и вежлив. Для более точного ответа можешь задавать ему вопросы. Если пользователь запросит что-то незаконное, вежливо ответь ему, что не можешь с этим помочь. И ещё: не делай грамматических ошибок."


def AI(chat_id, user_message, system_prompt):       #поиск ответа у ии
    if 'история' not in user_data[chat_id]:
        user_data[chat_id]['история'] = []  

    history = user_data[chat_id]['история']       

    if history == []:
        history.append({"role": "system", "content": system_prompt})

    history.append({"role": "user", "content": user_message})

    if len(history) > 12:
        user_data[chat_id]['история'] = [history[0]] + history[-10:]
    save_data()
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": history, 
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        while True:
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"]["content"]

            for word in FORBIDDEN_WORDS:
                if word in answer.lower():
                    break
            else:
                history.append({"role": "assistant", "content": answer})
                save_data()
                return answer
    except:
        return "❌ Не удалось обработать запрос. Попробуйте ещё раз."

@dp.message(lambda message: message.text and message.text == '💼 Бизнес-советник' and proverka_flags(message))      # меню по первой кнопке
async def ai_chat(message: Message):
    chat_id = message.chat.id
    user_data[chat_id]['флаги']['flag_AI'] = True                                                       
    await message.answer("💼 *Бизнес-советник*\n\n"
        "Задайте мне любой вопрос о бизнесе, идеях или решениях.\n"
        "Чем подробнее опишете ситуацию — тем точнее будет ответ!\n\n"
        "• Кнопка «✅ Готово» — завершает сеанс и возвращает в меню\n"
        "📌 *Совет:* Используйте кнопку «🗑️ очистить диалог», "
        "чтобы начать новый диалог с чистого листа.\n\n"
        "✏️ *Введите ваш запрос:", reply_markup=back_keyboard())
    
@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_AI'] == True and message.text != '◀️ Назад')  # вывод ответа ИИ       
async def get_question(message: types.Message):
    chat_id = message.chat.id
    if message.text == "✅ Готово":
        user_data[chat_id]['флаги']['flag_AI'] = False
        await message.answer('💼 Жду новых бизнес-задач!')
        await main_menu(message)  
        return
    elif message.text == '🗑️ Очистить диалог':
        user_data[chat_id]['история'] = []
        save_data() 
        await message.answer('🗑️ История диалога очищена!')
        return
    else:
        for  word in FORBIDDEN_WORDS:
            if word in message.text.lower():
                await message.answer('🚫 Запрос содержит недопустимые темы. Пожалуйста, переформулируйте в рамках бизнес-консультации.', reply_markup=end_keyboard()) 
                break
        else:                
            Answer = AI(chat_id, message.text, system_prompt)
            await message.answer(Answer, reply_markup=end_keyboard())


#************************Заметки*******************************


def show_zametki(chat_id):
    zametki = user_data[chat_id]['заметки']
    if zametki != []:
        answer = "📋 *Ваши заметки*\n\n"
        for i in range(len(zametki)):
            answer += f"{i+1}. 📌 {zametki[i]}\n"
        return answer
    else:
        return ('📝 Список заметок пуст. Добавьте запись через кнопку «✏️ Добавить заметку»')

def add_zametki(chat_id, user_message):
    zametki = user_data[chat_id]['заметки']
    zametki.append(user_message)
    save_data()
    

def delete_zametki(chat_id, index):
    zametki = user_data[chat_id]['заметки']
    del zametki[index-1]
    save_data()

def change_zametki(chat_id, index, text):
    zametki = user_data[chat_id]['заметки']
    zametki[index-1] = text
    save_data()
    


#меню заметок

@dp.message(lambda message: message.text and message.text == '📚 Заметки' and proverka_flags(message))
async def zametki_chat(message: Message):
    await message.answer("📝 *Мои заметки*\n\n"
        "Здесь вы можете хранить важные мысли, идеи, списки задач.\n\n"
        "📌 *Возможности:*\n"
        "• 📋 *Показать заметки* — просмотр всех сохранённых записей\n"
        "• ✏️ *Добавить заметку* — создайте новую заметку\n"
        "• 🗑️ *Удалить заметку* — выберите номер для удаления\n"
        "• 🔄 *Изменить заметку* — выберите номер и введите новый текст\n\n"
        "👇 *Выберите действие:*", reply_markup=zametki_keyboard())

#показ заметок
@dp.message(lambda message: message.text and message.text == '📋 Показать заметки'  and proverka_flags(message))
async def show_zametki_chat(message: Message):
    chat_id = message.chat.id
    answer = show_zametki(chat_id)
    await message.answer(answer, reply_markup=zametki_keyboard())

#функции по добавлению заметок
@dp.message(lambda message: message.text and message.text == '✏️ Добавить заметку' and proverka_flags(message))
async def add_zametki_chat(message: Message):
    chat_id = message.chat.id
    await message.answer('✏️ *Новая заметка*\n\nОтправьте текст заметки:', reply_markup=back_keyboard())
    user_data[chat_id]['флаги']['flag_add'] = True


@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_add'] == True and message.text != '◀️ Назад')
async def adding_zametki(message: Message):
    chat_id = message.chat.id
    add_zametki(chat_id, message.text)
    await message.answer('✅ Заметка успешно добавлена!', reply_markup=zametki_keyboard())
    user_data[chat_id]['флаги']['flag_add'] = False

#удаление заметок
@dp.message(lambda message: message.text and message.text == '🗑️ Удалить заметку' and proverka_flags(message))
async def delete_zametki_chat(message: Message):
    chat_id = message.chat.id
    if user_data[chat_id]['заметки'] != []:
        await message.answer('🗑️ *Удаление заметки*\n\nВведите номер заметки, которую хотите удалить:', reply_markup=ReplyKeyboardRemove())
        user_data[chat_id]['флаги']['flag_del'] = True
        answer = show_zametki(chat_id)
        await message.answer(answer, reply_markup=back_keyboard())
    else:
        await message.answer('📝 Список заметок пуст. Добавьте запись через кнопку «✏️ Добавить заметку»', reply_markup=zametki_keyboard())

@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_del'] == True and message.text != '◀️ Назад')
async def deleting_zametki(message: Message):
    if (message.text).isdigit():
        chat_id = message.chat.id
        zametki = user_data[chat_id]['заметки']
        index = int(message.text)
        if index > 0 and index <= len(zametki):
            delete_zametki(chat_id, index)
            await message.answer('✅ Заметка успешно удалена!', reply_markup=zametki_keyboard())
            user_data[message.chat.id]['флаги']['flag_del'] = False
        else:
            await message.answer('❌ Неверный номер. Пожалуйста, выберите номер из списка заметок.', reply_markup=back_keyboard())
    else:
        await message.answer('❌ Неверный формат. Введите, пожалуйста, номер цифрой.', reply_markup=back_keyboard())

#изменение заметок

@dp.message(lambda message: message.text and message.text == '🔄 Изменить заметку' and proverka_flags(message))
async def change_zametki_chat(message: Message):
    chat_id = message.chat.id
    if user_data[chat_id]['заметки'] != []:
        await message.answer('✏️ *Изменение заметки*\n\nВведите номер заметки, которую хотите изменить:', reply_markup=ReplyKeyboardRemove())
        user_data[chat_id]['флаги']['flag_change'] = True
        answer = show_zametki(chat_id)
        await message.answer(answer, reply_markup=back_keyboard())
    else:
        await message.answer('📝 Список заметок пуст. Добавьте запись через кнопку «✏️ Добавить заметку»', reply_markup=zametki_keyboard())

@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_change'] == True and message.text != '◀️ Назад')
async def changing_zametki_step1(message: Message):
    if (message.text).isdigit():
        chat_id = message.chat.id
        zametki = user_data[chat_id]['заметки']
        index = int(message.text)
        if index > 0 and index <= len(zametki):
            await message.answer('✏️ *Редактирование заметки*\n\nВведите новый текст заметки:', reply_markup=back_keyboard())
            user_data[chat_id]['флаги']['index'] = index
            user_data[chat_id]['флаги']['flag_change'] = False
            user_data[chat_id]['флаги']['flag_change2'] = True
        else:
            await message.answer('❌ Неверный номер. Пожалуйста, выберите номер из списка заметок.', reply_markup=back_keyboard())
    else:
        await message.answer('❌ Неверный формат. Введите, пожалуйста, номер цифрой.', reply_markup=back_keyboard())


@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_change2'] == True and message.text != '◀️ Назад')
async def changing_zametki_step2(message: Message):
    chat_id = message.chat.id
    index = user_data[chat_id]['флаги']['index']
    change_zametki(chat_id, index, message.text)
    await message.answer('✅ Заметка успешно изменена!', reply_markup=zametki_keyboard())
    user_data[chat_id]['флаги']['flag_change2'] = False
    user_data[chat_id]['флаги'].pop('index', None)



#*****************************НАПОМИНАНИЯ***************************


def show_napominaniya(chat_id):
    napominaniya = user_data[chat_id]['напоминания']
    if napominaniya != []:
        answer = "⏰ *Ваши напоминания*\n\n"
        for i in range(len(napominaniya)):
            remind = napominaniya[i]
            answer += f"{i+1}. 📌 {remind[0]}\n   ⏱️ {remind[1].strftime('%d.%m.%Y в %H:%M')}\n\n"
        return answer
    else:
        return ('🔔 У вас пока нет напоминаний. Нажмите «✏️ Добавить напоминание», чтобы создать первое!')

def add_napominaniya(chat_id, user_message, date):
    napominaniya = user_data[chat_id]['напоминания']
    napominaniya.append([user_message, date])
    save_data()
    

def delete_napominaniya(chat_id, index):
    napominaniya = user_data[chat_id]['напоминания']
    del napominaniya[index-1]
    save_data()

@dp.message(lambda message: message.text and message.text == '📅 Планировщик' and proverka_flags(message))
async def napominaniya_chat(message: Message):
    await message.answer("📅 *Планировщик*\n\n"
    "👋 **Добро пожаловать! Я ваш персональный помощник.**\n\n"
    "Здесь вы можете планировать важные дела, встречи и задачи, "
    "чтобы бот вовремя о них напомнил.\n\n"
    "📌 *Возможности:*\n"
    "• 📋 *Показать напоминания* — просмотр всех запланированных уведомлений\n"
    "• ✏️ *Добавить напоминание* — установить новое напоминание на нужное время\n"
    "• 🗑️ *Удалить напоминание* — отменить ненужное или выполненное напоминание\n\n"
    "👇 *Выберите действие:*", reply_markup=napominalka_keyboard())

@dp.message(lambda message: message.text and message.text == '📋 Показать напоминания' and proverka_flags(message))
async def show_napominaniya_chat(message: Message):
    chat_id = message.chat.id
    answer = show_napominaniya(chat_id)
    await message.answer(answer, reply_markup=napominalka_keyboard())

@dp.message(lambda message: message.text and message.text == '✏️ Добавить напоминание' and proverka_flags(message))
async def add_napominaniya_chat(message: Message):
    chat_id = message.chat.id
    await message.answer('✏️ *Новое напоминание*\n\nВведите текст напоминания:', reply_markup=back_keyboard())
    user_data[chat_id]['флаги']['flag_add_nap1'] = True


@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_add_nap1'] == True and message.text != '◀️ Назад')
async def adding_napominaniya(message: Message):
    chat_id = message.chat.id
    text = message.text
    await message.answer(
        "📅 *Укажите дату и время*\n\n"
"Формат: ГГГГ-ММ-ДД ЧЧ:ММ\n"
"📍 Пример: 2026-05-20 14:30\n\n"
"🕐 *Важно:* дата должна быть в будущем", reply_markup=back_keyboard())
    user_data[chat_id]['флаги']['text'] = text
    user_data[chat_id]['флаги']['flag_add_nap1'] = False
    user_data[chat_id]['флаги']['flag_add_nap2'] = True


@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_add_nap2'] == True and message.text != '◀️ Назад')
async def adding_nap2(message: Message):
    date_str = message.text
    chat_id = message.chat.id
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M")
        if dt <= datetime.now():
            await message.answer('❌ Неверная дата. Пожалуйста, укажите дату и время в будущем.', reply_markup=back_keyboard())
        else:
            text = user_data[chat_id]['флаги']['text']
            add_napominaniya(chat_id, text, dt)
            await message.answer('✅ Напоминание успешно добавлено!', reply_markup=napominalka_keyboard())
            user_data[chat_id]['флаги']['flag_add_nap2'] = False
            user_data[chat_id]['флаги'].pop('text', None)
    except:
        await message.answer("❌ Неверный формат даты или такой даты не существует.\n\n"
"📅 Правильный формат: ГГГГ-ММ-ДД ЧЧ:ММ\n"
"📍 Пример: 2026-05-20 14:30", reply_markup=back_keyboard())


@dp.message(lambda message: message.text and message.text == '🗑️ Удалить напоминание' and proverka_flags(message))
async def delete_napominaniya_chat(message: Message):
    chat_id = message.chat.id
    if user_data[chat_id]['напоминания'] != []:
        await message.answer('🗑️ *Удаление напоминания*\n\nВведите номер напоминания, которое хотите удалить:', reply_markup=ReplyKeyboardRemove())
        user_data[chat_id]['флаги']['flag_del_nap'] = True
        answer = show_napominaniya(chat_id)
        await message.answer(answer, reply_markup=back_keyboard())
    else:
        await message.answer('🔔 У вас пока нет напоминаний. Нажмите «✏️ Добавить напоминание», чтобы создать первое!', reply_markup=napominalka_keyboard())

@dp.message(lambda message: user_data[message.chat.id]['флаги']['flag_del_nap'] == True and message.text != '◀️ Назад')
async def deleting_napominaniya(message: Message):
    if (message.text).isdigit():
        chat_id = message.chat.id
        napominaniya = user_data[chat_id]['напоминания']
        index = int(message.text)
        if index > 0 and index <= len(napominaniya):
            delete_napominaniya(chat_id, index)
            await message.answer('✅ Напоминание успешно удалено', reply_markup=napominalka_keyboard())
            user_data[message.chat.id]['флаги']['flag_del_nap'] = False
        else:
            await message.answer('❌ Неверный номер. Пожалуйста, выберите номер из списка напоминаний', reply_markup=back_keyboard())
    else:
        await message.answer('❌ Неверный формат. Введите, пожалуйста, номер цифрой.', reply_markup=back_keyboard())







async def proverka_napominaniy():
    """Функция проверки напоминаний (работает в фоне)"""
    while True:
        await asyncio.sleep(30)  # Проверяем каждые 30 секунд
        print("Проверка напоминаний...")
        
        # Важно: создаём копию списка для итерации
        now_time = datetime.now()
        to_remove = []
        need_save = False

        for chat_id, info in user_data.items():  # Итерируемся по копии
            for reminder in info['напоминания']:
                napominanie, data = reminder[0], reminder[1]
                if data <= now_time:
                    print(f"Напоминание готово: {napominanie}")

                    if chat_id not in active_napominaniya:
                        active_napominaniya[chat_id] = []
                    active_napominaniya[chat_id].append(napominanie)
                    to_remove.append(reminder)

            for lis in to_remove:
                info['напоминания'].remove(lis)
                save_data()
        if to_remove:
            save_data()


async def reminder(chat_id: int):
    while True:
        await asyncio.sleep(5) 
        if chat_id in active_napominaniya and active_napominaniya[chat_id]:
            # Отправляем ВСЕ активные напоминания
            for napominanie in active_napominaniya[chat_id][:]:  # Итерируемся по копии
                await bot.send_message(chat_id, f"🔔 НАПОМИНАНИЕ: {napominanie}")
                active_napominaniya[chat_id].remove(napominanie)
                print(f"Отправлено напоминание пользователю {chat_id}: {napominanie}")


@dp.message(lambda message: message.text == '◀️ Назад')
async def back(message):
    chat_id = message.chat.id
    if user_data[chat_id]['флаги'].get('flag_AI', False):
        user_data[chat_id]['флаги']['flag_AI'] = False
        await message.answer('Выход из режима "💼 Бизнес-советник"')
        await main_menu(message)
        return
    
    # 2. Если в режиме добавления заметок
    if user_data[chat_id]['флаги'].get('flag_add', False):
        user_data[chat_id]['флаги']['flag_add'] = False
        await message.answer('❌ Добавление заметки отменено', reply_markup=zametki_keyboard())
        return
    
    # 3. Если в режиме удаления заметок
    if user_data[chat_id]['флаги'].get('flag_del', False):
        user_data[chat_id]['флаги']['flag_del'] = False
        await message.answer('❌ Удаление заметки отменено', reply_markup=zametki_keyboard())
        return
    
    # 5. Если в режиме изменения заметок (второй шаг)
    if user_data[chat_id]['флаги'].get('flag_change2', False):
        user_data[chat_id]['флаги']['flag_change2'] = False
        user_data[chat_id]['флаги'].pop('index', None)
        await message.answer('❌ Изменение заметки отменено', reply_markup=zametki_keyboard())
        return
    
    # 4. Если в режиме изменения заметок (первый шаг)
    if user_data[chat_id]['флаги'].get('flag_change', False):
        user_data[chat_id]['флаги']['flag_change'] = False
        await message.answer('❌ Изменение заметки отменено', reply_markup=zametki_keyboard())
        return
    
    # 6. Если в режиме добавления напоминания (первый шаг)
    if user_data[chat_id]['флаги'].get('flag_add_nap1', False):
        user_data[chat_id]['флаги']['flag_add_nap1'] = False
        await message.answer('❌ Добавление напоминания отменено', reply_markup=napominalka_keyboard())
        return

    # 7. Если в режиме удаления напоминания
    if user_data[chat_id]['флаги'].get('flag_del_nap', False):
        user_data[chat_id]['флаги']['flag_del_nap'] = False
        await message.answer('❌ Удаление напоминания отменено', reply_markup=napominalka_keyboard())
        return
    
    # 8. Если в режиме добавления напоминания (второй шаг)
    if user_data[chat_id]['флаги'].get('flag_add_nap2', False):
        user_data[chat_id]['флаги']['flag_add_nap2'] = False
        user_data[chat_id]['флаги'].pop('text', None)
        await message.answer('❌ Добавление напоминания отменено', reply_markup=napominalka_keyboard())
        return
    # 9. Если ничего не активно - просто показываем главное меню
    await main_menu(message)




async def main():
    asyncio.create_task(proverka_napominaniy())
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())