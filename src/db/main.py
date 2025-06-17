from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession  # Use sqlmodel's AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import Config

# Initialize the async database engine
engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))

# Function to initialize the database tables
async def init_db() -> None:
    try:
        async with engine.begin() as conn:
            from src.db.models import Book  # Lazy import to avoid circular dependencies
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Database initialization failed: {e}")

# Function to provide an async database session
async def get_session() -> AsyncSession:
    # Create session factory
    SessionFactory = sessionmaker(
        bind=engine,
        class_=AsyncSession,  # Use sqlmodel's AsyncSession
        expire_on_commit=False  # Avoid expiring objects after commit
    )
    # Provide session using async context manager
    async with SessionFactory() as session:
        yield session