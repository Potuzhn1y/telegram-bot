import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties

TOKEN = "7629370028:AAF9TRgXD_wQNSpzG7_b0TJdvNOQRkK_iqc"
GROUP_ID = -1002403749647  # ID твого чату
THREAD_ID = 8143  # ID теми "Заявки на ремонт"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Стан для обробки заявки
class RequestForm(StatesGroup):
    name = State()  # Етап 1 - Ім'я
    phone = State()  # Етап 2 - Номер телефону
    device = State()  # Етап 3 - Модель пристрою та проблема
    location = State()  # Етап 4 - Локація

# Кнопки для вибору локацій
location_buttons = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Retroville🛍️"), types.KeyboardButton(text="Smart Plaza Polytech🛍️")],
        [types.KeyboardButton(text="Не в Києві – відправлю через Нову Пошту🚚")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(RequestForm.name)
    await message.answer("Вітаю! Введіть Ваше ім'я: 👋")

@dp.message(RequestForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RequestForm.phone)
    await message.answer("Тепер введіть Ваш номер телефону📱:")

@dp.message(RequestForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(RequestForm.device)
    await message.answer("Вкажіть модель Вашого пристрою та розкажіть в чому проблема🖥️:")

@dp.message(RequestForm.device)
async def process_device(message: types.Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(RequestForm.location)
    await message.answer("Виберіть локацію для звернення🏙️:", reply_markup=location_buttons)

@dp.message(RequestForm.location)
async def process_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    phone = data["phone"]
    device_info = data["device"]
    location = message.text

    text = (
        f"<b>Нова заявка від {name}:</b>\n\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"📱 <b>Пристрій:</b> {device_info}\n"
        f"🏙️ <b>Локація:</b> {location}"
    )

    # Надсилаємо заявку в чат
    await bot.send_message(chat_id=GROUP_ID, text=text, message_thread_id=THREAD_ID)

    # Відповідь користувачеві + прибираємо кнопки локацій
    await message.answer("✅ Заявку надіслано менеджерам! Дякуємо!😊 (Для того, щоб створити нову заявку напишіть в чат /start)", reply_markup=types.ReplyKeyboardRemove())

    await state.clear()  # Очистити стан

async def main():
    print("Бот успішно запущений! 🚀")  # Повідомлення про успішний запуск
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


