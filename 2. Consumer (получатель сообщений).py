import asyncio
import aio_pika
import json
from mela import Mela

# Инициализация Telegram-бота
bot = Mela("YOUR_TELEGRAM_BOT_TOKEN")

async def process_message(message):
    """
    Обработка полученного сообщения из RabbitMQ.
    """
    async with message.process():
        body = json.loads(message.body)
        chat_id = body["chat_id"]
        text = body["text"]

        # Отправляем сообщение в Telegram
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"Message sent to Telegram chat {chat_id}: {text}")

async def start_consumer(queue_name):
    """
    Запуск потребителя RabbitMQ.
    """
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()

        # Проверяем или создаем очередь
        queue = await channel.declare_queue(queue_name, durable=True)

        # Подписываемся на очередь
        await queue.consume(process_message)

        print(f"Waiting for messages in queue '{queue_name}'...")
        await asyncio.Future()  # Блокируем выполнение для обработки сообщений

# Запуск потребителя
if __name__ == "__main__":
    asyncio.run(start_consumer('telegram_bot'))
