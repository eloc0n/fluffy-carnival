import aio_pika
import json
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.universities import Country, University
from universities import fetch_university_data
from config.settings import settings

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def get_async_engine(database_url: str) -> AsyncEngine:
    """Creates and returns an asynchronous database engine."""
    return create_async_engine(database_url, echo=True)


async def insert_data_into_db(session: AsyncSession, country_name: str, data: list):
    # Ensure country exists
    result = await session.exec(select(Country).where(Country.name == country_name))
    country = result.scalar_one_or_none()
    if not country:
        country = Country(name=country_name, alpha_two_code=data[0]["alpha_two_code"])
        session.add(country)
        await session.commit()
        await session.refresh(country)

    # Insert universities
    for uni in data:
        university = University(
            name=uni["name"],
            country_id=country.id,
            web_pages=uni["web_pages"],
            domains=uni["domains"],
        )
        session.add(university)
    await session.commit()


async def process_task(message: aio_pika.IncomingMessage):
    async with message.process():
        task = json.loads(message.body)
        country = task["country"]

        try:
            url = "http://universities.hipolabs.com/search"
            data = await fetch_university_data(url, country)

            engine = get_async_engine(settings.SQLALCHEMY_DATABASE_URI)
            async with AsyncSession(engine) as session:
                await insert_data_into_db(session, country, data)

            print(f"Data inserted successfully for {country}")
        except Exception as e:
            print(f"Failed to process task for {country}: {e}")
            raise  # Let the message requeue automatically if using a DLX


async def start_worker():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672//")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("university_tasks", durable=True)

        print("Worker started, waiting for tasks...")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process_task(message)
