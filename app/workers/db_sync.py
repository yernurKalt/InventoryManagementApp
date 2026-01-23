from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.config import settings


engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)

sessionLocal = sessionmaker(engine, autoflush=False)


def get_sync_session():
    return sessionLocal()