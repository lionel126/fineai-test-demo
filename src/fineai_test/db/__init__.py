from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fineai_test.config import settings

engines = {
    'app_store': create_async_engine(settings.postgresql_uri, echo=settings.sql_echo)
}

# class RoutingSession(Session):
    
#     def get_bind(self, mapper=None, clause=None, **kw):
#         if mapper and issubclass(mapper.class_, app.Base):
#             return engines['app_store'].sync_engine

# Sess = sessionmaker(class_=AsyncSession, sync_session_class=RoutingSession)

Sess = sessionmaker(bind=engines['app_store'], class_=AsyncSession) # type ignore

async def get_db():
    async with Sess() as db: # type ignore
        yield db
