import os
import threading
import json

from flask import Flask
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# файл для хранения верифицированных пользователей
VERIFIED_FILE = 'verified.json'

def load_verified() -> set[int]:
    if os.path.exists(VERIFIED_FILE):
        with open(VERIFIED_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_verified(users: set[int]):
    with open(VERIFIED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(users), f, ensure_ascii=False, indent=2)

verified_users = load_verified()

class Form(StatesGroup):
    serial = State()

# ==== Настройка бота ====
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ==== Клавиатуры ====
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add("☕ Выбрать модель кофемашины")
model_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "Azkoyen Vitro S1", "Azkoyen Vitro S5",
    "Jetinno JL22", "Jetinno JL24", "Jetinno JL300"
)
action_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "📛 У меня неисправность!", "📘 Обучение и инструкция"
).add("❓ Остались вопросы?")
problem_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    "🧠 Я знаю название ошибки",
    "🧯 Пролив или протечка",
    "🔌 Не включается",
    "💧 NO WATER / нет воды",
    "🗑 Слив отходов не работает",
    "🔧 Заварочный блок (F.ESPRSS.UNT.POS)"
)

# ==== Список разрешённых серийников ====
allowed_serials = {
    "0010258608", "0010289689", "0010289069", "0010289073",
    # … остальной список …
}

# ==== Handlers ====

@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    if message.from_user.id in verified_users:
        await state.finish()
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_menu)
    else:
        await Form.serial.set()
        await message.answer("👋 Привет! Введите серийный номер вашей кофемашины:")


@dp.message_handler(state=Form.serial)
async def process_serial(message: types.Message, state: FSMContext):
    sn = message.text.strip()
    if sn in allowed_serials:
        verified_users.add(message.from_user.id)
        save_verified(verified_users)
        await state.finish()
        await message.answer("✅ Серийный номер подтверждён!", reply_markup=main_menu)
    else:
        await message.answer("❌ Неверный серийный номер, попробуйте ещё раз:")


@dp.message_handler(lambda m: m.text == "☕ Выбрать модель кофемашины", state='*')
async def choose_model(message: types.Message):
    await message.answer("Выберите модель:", reply_markup=model_menu)


@dp.message_handler(lambda m: m.text.startswith(("Azkoyen", "Jetinno")), state='*')
async def model_selected(message: types.Message):
    if "Azkoyen" in message.text:
        text = (
            "ℹ️ ВАЖНО\n\n"
            "На экране Azkoyen должен быть восклицательный знак — это ошибка.\n"
            "Откройте дверь и нажмите PROG/C, посмотрите справа на экране.\n\n"
            "Если нет восклицательного знака — ошибок нет. Иначе перезагрузите."
        )
    else:
        text = (
            "ℹ️ ВАЖНО\n\n"
            "Нажмите и удерживайте логотип Fastkava в углу, введите пароль.\n"
            "Смотрите журнал ошибок справа."
        )
    await message.answer(text)
    await message.answer("Что делаем дальше?", reply_markup=action_menu)


@dp.message_handler(lambda m: m.text == "📛 У меня неисправность!", state='*')
async def problems_list(message: types.Message):
    await message.answer("Выберите проблему:", reply_markup=problem_menu)


@dp.message_handler(lambda msg: "F.ESPRSS.UNT.POS" in msg.text.upper() or "G.ESPRESSO UNIT" in msg.text.upper(), state='*')
async def espress_unit_error(message: types.Message):
    await message.answer(
        "🔧 Обнаружена ошибка: F.ESPRSS.UNT.POS (G.ESPRESSO UNIT)\n\n"
        "❗ Это значит, что заварочный блок «застрял» между позициями или не может вернуться в исходное положение.\n\n"
        "🔍 Проверьте пошагово:\n"
        "1. ⚡ Перезагрузите автомат\n"
        "   — Отключите питание, подождите 5 сек и включите обратно\n"
        "   — Должны слышаться характерные «гул» и щелчок мотора, возвращающего блок\n\n"
        "2. 🚪 Откройте дверь автомата и убедитесь:\n"
        "   • Всё стоит ровно, ничего не заклинило\n"
        "   • Блок зафиксирован «флажками» сверху-справа и снизу-слева\n\n"
        "🔧 Если не помогло — снимите заварочный блок вручную:\n"
        "   1. Найдите поршень (к нему подходит прозрачная трубка подачи кофе)\n"
        "   2. Снимите миксер (бежевая деталь с красной трубкой)\n"
        "   3. Разблокируйте крепления: переведите «флажки» в открытое положение, потяните блок вверх — снимите\n"
        "   4. Внутри вы увидите запрессованную таблетку — осторожно выковыряйте её зубочисткой или ножом\n"
        "   5. Промойте блок, установите обратно:\n"
        "      • Закрепите оба «флажка»\n"
        "      • Вставьте скобу поршня на место\n"
        "      • Плотно защёлкните миксер\n\n"
        "6. ⚡ Перезагрузите автомат ещё раз\n\n"
        "📸 Если проблема осталась — сделайте фото блока внутри и вышлите техподдержке."
    )


@dp.message_handler(lambda msg: "NO WASTE BIN" in msg.text.upper(), state='*')
async def no_waste_bin_error(message: types.Message):
    await message.answer(
        "🗑 Обнаружена ошибка: NO WASTE BIN\n\n"
        "❗ Аппарат не видит лоток для отходов.\n\n"
        "🔍 Проверьте пошагово:\n"
        "1. 📦 Убедитесь, что лоток установлен внутри\n"
        "   — Иногда его забывают вернуть после очистки\n\n"
        "2. 🔄 Выньте лоток и вставьте обратно до упора\n"
        "   — Лоток должен плотно войти по направляющим\n\n"
        "3. 🧼 Проверьте контактную площадку и сам лоток:\n"
        "   • Контакты чистые, без порошка и капель\n"
        "   • Лоток не перекошен, не забит остатками напитков\n\n"
        "⚙️ Если не уходит — сбросьте счётчик отходов:\n"
        "   • В сервисном меню (PROG/C) выберите Test Machine → пункт 114\n"
        "   • Нажмите D, затем кнопками A/B установите все цифры в 00000\n"
        "   • Подтвердите и выберите C несколько раз\n"
        "   • Перезагрузите автомат 2–3 раза\n\n"
        "📸 Если всё ещё нет — сфотографируйте экран и положение лотка."
    )


@dp.message_handler(lambda msg: "NO WATER" in msg.text.upper(), state='*')
async def no_water_error(message: types.Message):
    await message.answer(
        "💧 Обнаружена ошибка: NO WATER\n\n"
        "❗ Это означает, что автомат не может набрать воду.\n\n"
        "🔍 Проверьте пошагово:\n"
        "1. 📦 Убедитесь, что в канистре есть вода\n"
        "2. 🔍 Проверьте подачу:\n"
        "   • Трубка подачи не пережата (под ножкой или в мебельном отверстии)\n\n"
        "3. ⚡ Перезагрузите автомат\n"
        "   — Отключите/включите питание несколько раз\n"
        "   — Должны быть слышны звуки работающего насоса\n\n"
        "📸 Если даже после этого вода не идёт — пришлите фото канистры и трубок."
    )


# ==== HTTP для Render (keep-alive) ====
app = Flask(__name__)

@app.route("/")
def ping():
    return "OK", 200

def run_flask():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ==== Сброс webhook перед polling ====
async def on_startup(dp: Dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)

# ==== Точка входа ====
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )

