import asyncio
import aio_pika
import json

async def send_to_queue(queue_name, message):
    """
    Отправка сообщения в RabbitMQ очередь.
    """
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()

        # Проверяем или создаем очередь
        await channel.declare_queue(queue_name, durable=True)

        # Отправляем сообщение
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue_name,
        )
        print(f"Message sent to queue '{queue_name}': {message}")

# Запуск отправки сообщения
if __name__ == "__main__":
    asyncio.run(send_to_queue('telegram_bot', {'chat_id': 123456, 'text': 'Hello from RabbitMQ!'}))
