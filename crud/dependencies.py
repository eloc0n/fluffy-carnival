from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings


# Create the engine and sessionmaker
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=True, future=True
)

# AsyncSession instance
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency to get the session
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        return session
