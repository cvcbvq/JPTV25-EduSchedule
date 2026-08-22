import sqlite3 
import asyncio
from aiogram import Bot, Dispatcher, types 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile


#ОБЩАЯ ИНИЦИАЛИЗАЦИЯ
# / ÜLDINE INITSIALISEERIMINE

TOKEN = "8771936252:AAGoqAOq7P8oY8pRkQh-m7bI82yNQo04SXE"    
bot = Bot(token=TOKEN)
dp = Dispatcher()



# ЧАСТЬ 1: БАЗА ДАННЫХ И ЛОГИКА (Руслан)
# OSA 1: ANDMEBAAS JA LOOGIKA (Ruslan)


def create_database():
    #Создание таблиц базы данных / Andmebaasi tabelite loomine
    connection = sqlite3.connect("eduschedule.db")
    cursor = connection.cursor()

    # Таблица пользователей / Kasutajate tabel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            task_done INTEGER DEFAULT 0
        )
    """)

    # ТАБЛИЦА ЗАДАЧ / ÜLESANDE TABEL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            task TEXT,
            deadline TEXT
        
    """)

    connection.commit()
    connection.close()


def get_or_create_user(user_id: int):
    #Получение или регистрация пользователя / Kasutaja saamine või registreerimine
    connection = sqlite3.connect("eduschedule.db")
    cursor = connection.cursor()
    cursor.execute("SELECT task_done FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (user_id, task_done) VALUES (?, 0)", (user_id,))
        connection.commit()
        connection.close()
        return 0   


    connection.close()
    return user[0]


def increment_tasks_done(user_id: int):
    #Увелечение счетчика выполнения ДЗ / Tehtud üleannete suurendamine
    connection = sqlite3.connect("eduschedule.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET tasks_done = task_done + 1 WHERE user_id = ?", (user_id,))
    connection.commit()
    connection.close()


    def add_homework(subject: str, task: str, deadline: str):
        #Добавление ДЗ в базу / Kodutöö lisamine andmebaasi
        connection = sqlite3.connect("eduschedule.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO homework (subject, task, deadline) VALUES (?, ?, ?)", (subject, task, deadline))
        connection.commit()
        connection.close()


    def get_all_homework():
        #Получение всех ДЗ из базы / Kõigi kodutööde saamine andmebaasist
        connection = sqlite3.connect("eduschedule.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, subject, task, deadline FROM homework")
        result = cursor.fetchall()
        connection.close()
        return result


    def delete_homework(homework_id: int):
        #Удаление ДЗ из базы / Kodutöö kustutamine andmebaasist
        connection = sqlite3.connect("eduschedule.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM homework WHERE id = ?", (homework_id,))
        connection.commit()
        connection.close()

# =====================================================================
#  ЧАСТЬ 2: КОМАНДЫ БОТА И ИНТЕРФЕЙС (Ярослав)
#  OSA 2: TELEGRAM BOTI KÄSUD JA UI (Jaroslav)
# =====================================================================


@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Стартовая команда / Alguskäsk"""
    user_id = message.from_user.id
    get_or_create_user(user_id)
    await message.answer("📚 Tere! See on EduSchedule bot.\n"
                         "Aitan sul jälgida oma kodutöid ja tunde! 🐸")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Кманда помощи / Abikäsk"""
    help_text = (
    "EduSchedule on bot õppimise ja kodutööde haldamiseks.\n\n"
    "Käsud:\n"
    "/start - Alusta boti kasutamist\n"
    "/help - Abiinfo\n"
    "/dz - Vaata aktiivselt
    "/lisa - Lisa uus kodutöö\n"
    "/mina - Sinu statistika\n"
    "/dev - Arendaja menüü"
) 
 try:
        photo = FSInputFile("assets/Help.png")
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=help_text)
    except Exception:
        await message.answer(help_text)

@dp.message(Command("dz"))
async def dz_command(message: types.Message):
    """Просмотр домашних заданий / Kodutööde vaatamine"""
    user_id = message.from_user.id
    get_or_create_user(user.id)

homeworks = get_all_homework()

if not homeworks:
    await message.answer("🎉 Kodutöid pole! Kõik on tehtud.")
    return

await message.answer("📖 **Aktiivsed kodutööd:**", parse_mode="Markdown")

for hw in homeworks:
    hw_id, subject, task, deadline = hw
    text = f"📌 **Aine:** {subject}\n📝 **Ülesanne:** {task}\n⏳ **Tähtaeg:** {deadline}"

    keyboard = InlineKeyboardMarkup(unline_keyboard=[
        [InlineKeyboardButton(text="✅ Märgi tehtuks", callback_data=f"done_{hw_id}")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query(lamba c: c.data and c.data.startswith("done_"))
async def done_callback.from_user.id
hw_id = int(callback.data.split("_")[1])

delete_homework(hw_id)
increment_tasks_done(user_id)

await callback.answer("Tubli! Ülesanne on tehtud! 🎉", show_alert=True)
await callback.message.delete()

@dp.message(Command("lisa"))
async def lisa_command(message: types.Message):
    """Меню быстрого добавления / Kiire lisamise menüü"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Python (Harjutus 5)", callback_data="add_Python_Harjutus 5_Homme")],
        [InlineKeyboardButton(text="Matemaatika (Lk 42)", callback_data="add_Matemaatika_Lk 42_Reede")],
        [InlineKeyboardButton(text="Inglise keel (Grammar)", callback_data="add_Inglise_Grammar_Esmaspäev")]
    ])
    await message.answer("Vali kiir-lisatav kodutöö või vali aine:", reply_markup=keyboard)

@dp.callback_query(lamba c: c.data and and c.data.startswith("add_"))
async def add_callback(callback: types.CallbackQuery):
     """Сохранение добавленного ДЗ / Lisatud kodutöö salvestamine"""
     _, subject, task, deadline = callback.data.split("_")

     add_homework(subject, task, deadline)

    await callback.answer(f"Kdutöö aines {subject} lisatud!", show_alert=True))
    await callback.message.answer(
        f"✅ Uus kodutöö lisatud!\n📌 **Aine:** {subject}\n📝 **Ülesanne:** {task}", 
        parse_mode="Markdown"
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("done_"))
async def done_callback(callback: types.CallbackQuery):
    """Обработка кнопки 'Сделано' / 'Tehtud' nupu haldur"""
    user_id = callback.from_user.id
    hw_id = int(callback.data.split("_")[1])

    delete_homework(hw_id)
    increment_tasks_done(user_id)

    await callback.answer("Tubli! Ülesanne on tehtud! 🎉", show_alert=True)
    await callback.message.delete()

    @dp.message(Command("lisa"))
async def lisa_command(message: types.Message):
    """Меню быстрого добавления / Kiire lisamise menüü"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Python (Harjutus 5)", callback_data="add_Python_Harjutus 5_Homme")],
        [InlineKeyboardButton(text="Matemaatika (Lk 42)", callback_data="add_Matemaatika_Lk 42_Reede")],
        [InlineKeyboardButton(text="Inglise keel (Grammar)", callback_data="add_Inglise_Grammar_Esmaspäev")]
    ])
    await message.answer("Vali kiir-lisatav kodutöö või vali aine:", reply_markup=keyboard)

    @dp.callback_query(lamba c: c.data and c.data.startswith("add_"))
    async def add_callback(callback: types.CallbackQuery):
         """Сохранение добавленного ДЗ / Lisatud kodutöö salvestamine"""
        _, subject, task, deadline = callback.data.split("_")

    add_homework(subject, tast, deadline)

    await callback.answer(f"Kodutöö aines {subject} lisatud!", show_alert=True)
    await callback.message.answer(
        f"✅ Uus kodutöö lisatud!\n📌 **Aine:** {subject}\n📝 **Ülesanne:** {task}", 
        parse_mode="Markdown"
    )


@dp.message(command("mina"))
async def mina_command(message: types.Message):
    """Профил и статистика / Profil ja statistika"""
    user_id = message.from_user.id
    tasks_done = get_or_create_user(user_id)

    text = f"📊 **Sinu statistika:**\n\nID: {user_id}\nTehtud kodutöid kokku: {tasks_done} 🏆"

    try:
        photo = FSInputFile("assets/Mina.png")
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, parse_mode="Markdown")
    except Exception:
        await message.answer(text, parse_mode="Markdown")


@dp.message(Command("dev"))
async def dev_command(message: types.Message):
    """Меню разработчика / Arendaja menüü"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kasutajate statistika", callback_data="dev_stats")],
        [InlineKeyboardButton(text="Puhasta andmebaas", callback_data="dev_clear")]
    ])

    try:
        photo - FSInputFile("assets/Dev.png")
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="🛠 Dev menüü:", reply_markup=keyboard)
    except Exception:
        await message.answer("🛠 Dev menüü:", reply_markup=keyboard)


@dp.callback_query(lamba c: c.data abd c.data.startswith("dev_"))
async def dev_callback(callback: types.CallbackQuery):
    """Логика админ панели / Arendaja menüü loogika"""
    action = callback.data.split("_")[1]

   if action == "stats":
        connection = sqlite3.connect("eduschedule.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        connection.close()

        text = "Kasutajate andmebaas:\n\n"
        for u in users:
            text += f"ID: {u[0]} | Tehtud: {u[1]}\n"

        text += f"\nKokku kasutajaid: {len(users)}"
        await callback.message.answer(text[:4000])
        await callback.answer()

   elif action == "clear":
        connection = sqlite3.connect("eduschedule.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM homework")
        connection.commit()
        connection.close()

        await callback.message.answer("Andmebaas on täielikult puhastatud!")
        await callback.anwer()
