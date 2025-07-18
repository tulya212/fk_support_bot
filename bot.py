import os
import threading

from flask import Flask
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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
    "0010289071", "0010289697", "0010289699", "0010289310",
    "0010289690", "0010289070", "0010276287", "0010289230",
    "0010294124", "0010299304", "0010299303", "0010299305",
    "0010299306", "0010271325", "0010289062", "0010289233",
    "0010294125", "0010289067", "0010289693", "0010280734",
    "0010311211", "0010299302", "0010299297", "0010299307",
    "0010308787", "0010299328", "0010298017", "0010298018",
    "0010298101", "0010298019", "0010298102", "0010298020",
    "0010298016", "0010304011", "0010301717", "0010302157",
    "0010301716", "0010302153", "0010302156", "0010302154",
    "0010301192", "0010301720", "0010299329", "0010299330",
    "0010302155", "0010299327", "DCEC 21BBTEECU90", "0010276286",
    "0010308785", "0010305788", "0010306890", "0010305791",
    "0010305892", "0010305790", "0010306889", "0010306887",
    "0010308786", "0010306892", "0010308789", "0010311210",
    "0010311510", "0010311511", "0010311507", "0010306879",
    "0010311509", "0010311508", "0010313377", "0010313378",
    "0010311669", "0010289067", "0010289693", "10280734",
    "0010289071", "0010289697", "0010289699", "0010271325",
    "0010289062", "2024416002", "0010299302", "0010313904",
    "0010314805", "0010317827", "0010317828", "2411129852",
    "2411129856", "2411129848", "2411129845", "2411129850",
    "2411129855", "2411129842", "2411129851", "2411129841",
    "2411129837", "2411129847", "2411129838", "2411129857",
    "2411129853", "2411129859", "2411129846", "2411129839",
    "2411129858", "2411129844", "2411129860", "2411129861",
    "2411129854", "2411129849", "2411129843", "2411129840",
    "2402100642", "2402100618", "2410124638", "2410124599",
    "2410124590", "2410124595", "2410124587", "2503148242",
    "2503148230", "2503148239", "2503148217", "2503148219",
    "2503148237", "2503148226", "2503148228", "2503148227",
    "2503148218", "2503148234", "2503148235", "2503148238",
    "2503148216", "2412132984", "2412132780", "2412132847",
    "2412132983", "2412132947", "2412132875", "2412132981"
}

verified_users = set()

# ==== Handlers ====

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Бот успешно запущен! ✅")
    if message.from_user.id not in verified_users:
        await message.answer("👋 Введите серийный номер вашей кофемашины:")
    else:
        await message.answer("Выберите модель или действие:", reply_markup=main_menu)

@dp.message_handler(lambda m: m.from_user.id not in verified_users)
async def verify_serial(message: types.Message):
    if message.text.strip() in allowed_serials:
        verified_users.add(message.from_user.id)
        await message.answer("✅ Номер подтверждён.", reply_markup=main_menu)
    else:
        await message.answer("❌ Неверный серийный номер, попробуйте ещё раз:")

@dp.message_handler(lambda m: m.text == "☕ Выбрать модель кофемашины")
async def choose_model(message: types.Message):
    await message.answer("Выберите модель:", reply_markup=model_menu)

@dp.message_handler(lambda m: m.text.startswith(("Azkoyen", "Jetinno")))
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

@dp.message_handler(lambda m: m.text == "📛 У меня неисправность!")
async def problems_list(message: types.Message):
    await message.answer("Выберите проблему:", reply_markup=problem_menu)

@dp.message_handler(lambda msg: "F.ESPRSS.UNT.POS" in msg.text.upper() or "G.ESPRESSO UNIT" in msg.text.upper())
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

@dp.message_handler(lambda msg: "NO WASTE BIN" in msg.text.upper())
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
        "   • Подтвердите и выйдите — многократно нажмите C\n"
        "   • Перезагрузите автомат 2–3 раза\n\n"
        "📸 Если всё ещё нет — сфотографируйте экран и положение лотка."
    )

@dp.message_handler(lambda msg: "NO WATER" in msg.text.upper())
async def no_water_error(message: types.Message):
    await message.answer(
        "💧 Обнаружена ошибка: NO WATER\n\n"
        "❗ Это означает, что автомат не может набрать воду.\n\n"
        "🔍 Проверьте пошагово:\n"
        "1. 📦 Убедитесь, что в канистре есть вода\n"
        "2. 🔍 Проверьте подачу:\n"
        "   • Трубка подачи не пережата (под ножкой или в мебельном отверстии)\n\n"
        "3. ⚡ Перезагрузите автомат\n"
        "   — Отключите/включите питание\n"
        "   — Иногда требуется несколько попыток, чтобы насос «всосал» воду\n"
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
    # 1) HTTP-сервер для Render
    threading.Thread(target=run_flask, daemon=True).start()
    # 2) Запуск long-polling
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )
