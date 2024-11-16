from mela import Mela

bot = Mela("YOUR_TELEGRAM_BOT_TOKEN")

@bot.on_message()
async def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    # Логика обработки сообщения
    reply_text = f"Echo: {text}"
    await message.reply(reply_text)

    # Отправка данных в RabbitMQ
    await send_to_queue('telegram_bot', {'chat_id': chat_id, 'text': reply_text})

# Запуск бота
bot.run()
