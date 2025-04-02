import requests

TOKEN = "7629370028:AAF9TRgXD_wQNSpzG7_b0TJdvNOQRkK_iqc"  # Встав свій токен бота
CHAT_ID = "-1002403749647"  # Ідентифікатор групи
THREAD_ID = 8143  # Ідентифікатор підтеми
TEXT = "✅ Бот працює! Повідомлення у підтему."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
params = {
    "chat_id": CHAT_ID,
    "message_thread_id": THREAD_ID,
    "text": TEXT
}

response = requests.post(url, params=params)
print(response.json())  # Дивимося відповідь API
