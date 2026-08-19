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
    import sqlite3
    import asyncio
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command
    from aiogram.types import InLineKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, FsinputFile
# =====================================================================
#  ОБЩАЯ ИНИЦИАЛИЗА / ÜLDINE INITSIALISEERIMINE
# =====================================================================
TOKEN = "8771936252:AAGoqAOq7P8oY8pRkQh-m7bI82yNQo04SXE"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# =====================================================================
#  ЧАСТЬ 1: БАЗА ДАННЫХ И ЛОГИКА (Руслан)
#  OSA 1: ANDMEBAAS JA LOOGIKA (Ruslan)
# =====================================================================

def create_database():
    """Создание таблиц базы данных / Andmebaasi tabelite loomine"""
    connection = sqlite3.connect("eduschedule.db")
    cursor = connection.cursor()

    # Таблица пользователей / Kasutajate tabel
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,tasks_done INTEGER DEFAULT 0)""")
    # Таблица домашних заданий / Kodutööde tabel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            task TEXT,
            deadline TEXT
        )
    """)

    connection.commit()
    connection.close()


    
   
