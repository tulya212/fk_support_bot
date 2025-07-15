
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
API_TOKEN = '7177666983:AAHgWg6yZKhaJ-BZRACUkxi68bfgDrj2SvI'

# Список серийных номеров
allowed_serials = {
    "0010258608", "0010289689", "0010289069", "0010289073", "0010289071",
    "0010289697", "0010289699", "0010289310", "0010289690", "0010289070",
    "0010276287", "0010289230", "0010294124", "0010299304", "0010299303",
     "0010298017",
"0010298018",
"0010298101",
"0010298019",
"0010298102",
"0010298020",
"0010298016",
"0010304011",
"0010301717",
"0010302157",
"0010301716",
"0010302153",
"0010302156",
"0010302154",
"0010301192",
"0010301720",
"0010299329",
"0010299330",
"0010302155",
"0010299327",
"0010276286",
"0010308785",
"0010305788",
"0010306890",
"0010305791",
"0010305892",
"0010305790",
"0010306889",
"0010306887",
"0010308786",
"0010306892",
"0010308789",
"0010311210",
"0010311510",
"0010311511",
"0010311507",
"0010306879",
"0010311509",
"0010311508",
"0010313377",
"0010313378",
"0010311669",
"0010289067",
"0010289693",
"10280734",
"0010289071",
"0010289697",
"0010289699",
"0010271325",
"0010289062",
"2024416002",
"0010299302",
"0010313904",
"0010314805",
"0010317827",
"0010317828",
"2411129852",
"0010308787"	
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню после подтверждения номера
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("☕ Выбрать модель кофемашины")

# Меню выбора модели
model_menu = ReplyKeyboardMarkup(resize_keyboard=True)
model_menu.add("Azkoyen Vitro S1", "Azkoyen Vitro S5")
model_menu.add("Jetinno JL22", "Jetinno JL24", "Jetinno JL300")

# Меню действий
action_menu = ReplyKeyboardMarkup(resize_keyboard=True)
action_menu.add("📛 У меня неисправность!", "📘 Обучение и инструкция")
action_menu.add("❓ Остались вопросы?")

# Меню с проблемами
problem_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
problem_menu.add(
    "🧠 Я знаю название ошибки",
    "🧯 Пролив или протечка", "🔌 Не включается",
    "💳 Аппарат не наливает после оплаты",
    "❗ На напитках восклицательные знаки",
    "💧 NO WATER / нет воды",
    "🗑 Слив отходов не работает",
    "⚙️ Проблема с терминалом",
    "🌀 Проблема с миксером",
    "👎 Невкусный кофе",
    "🔧 Заварочный блок (F.ESPRSS.UNT.POS)",
    "🥫 Сухие ингредиенты (молоко, шоколад, карамель и т.д.)",
    "⚙️ Проблема с гриндером",
    "🤷 Я не знаю, что за проблема"
)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Чтобы продолжить, введите серийный номер вашей кофемашины:")

@dp.message_handler(lambda msg: msg.text in allowed_serials)
async def verify_serial(message: types.Message):
    await message.answer("✅ Номер подтверждён. Продолжим:", reply_markup=main_menu)

@dp.message_handler(lambda msg: msg.text == "☕ Выбрать модель кофемашины")
async def choose_model(message: types.Message):
    await message.answer("Выберите вашу модель:", reply_markup=model_menu)

@dp.message_handler(lambda msg: msg.text in ["Azkoyen Vitro S1", "Azkoyen Vitro S5", "Jetinno JL22", "Jetinno JL24", "Jetinno JL300"])
async def model_selected(message: types.Message):
    model = message.text
    if "Azkoyen" in model:
        info = "ℹ️ ВАЖНО\n\nНа экране автомата должен быть восклицательный знак — это значит, что есть ошибка.\n\nОткройте дверь и нажмите кнопку PROG (или C на пульте, если это S5).\n\nОшибка появится справа на экране. Запомните или сфотографируйте её.\n\n🔸 Если восклицательного знака нет — ошибок сейчас нет.\nЕсли напитки не нажимаются, попробуйте перезагрузить автомат."
    else:
        info = "ℹ️ ВАЖНО\n\nНажмите и удерживайте логотип Fastkava в левом верхнем углу экрана.\nВведите сервисный пароль.\n\nСправа появится список ошибок. Запомните или сфотографируйте текущую ошибку."
    await message.answer(info)
    await message.answer("Что хотите сделать?", reply_markup=action_menu)

@dp.message_handler(lambda msg: msg.text == "📛 У меня неисправность!")
async def problems_list(message: types.Message):
    await message.answer("Выберите, какая проблема у автомата:", reply_markup=problem_menu)

@dp.message_handler(lambda msg: msg.text == "🧠 Я знаю название ошибки")
async def known_error(message: types.Message):
    await message.answer("Введите название ошибки на экране (например: NO WATER, GRINDER JAM)")

@dp.message_handler(lambda msg: "NO WATER" in msg.text.upper())
async def no_water_solution(message: types.Message):
    await message.answer("💧 Обнаружена ошибка: NO WATER\n\n...\n(вставим подробную инструкцию сюда — ты её уже дал, и я загружу в код)")

@dp.message_handler(lambda msg: "NO WASTE BIN" in msg.text.upper())
async def waste_bin_solution(message: types.Message):
    await message.answer("🗑 Обнаружена ошибка: NO WASTE BIN\n\n...\n(здесь будет инструкция по замене и сбросу счётчика)")

# и так далее для других ошибок...

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    # Запуск бота
    import asyncio
    from aiogram import executor
    from bot import dp  # Импортируй Dispatcher из своего кода

    asyncio.run(executor.start_polling(dp, skip_updates=True))



