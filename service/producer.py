import aio_pika
import json


async def send_task_to_queue(country: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672//")
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"country": country}).encode()),
            routing_key="university_tasks",
        )
        print(f"Task sent for country: {country}")
