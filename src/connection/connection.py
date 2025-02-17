from asyncio import current_task
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from src.config.db_config import loaded_config
from src.utills.metaclasses import Singleton

# TODO - extract from env variables or args
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ConnectionManager(metaclass=Singleton):
    def __init__(self):
        self._db_engine, self._db_session_factory = self._setup_db()

    def get_session_factory(self):
        return self._db_session_factory

    @staticmethod
    def _setup_db():
        db_url = str(loaded_config.db_url)
        async_db_url = db_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")

        engine = create_async_engine(async_db_url)
        session_factory = async_scoped_session(
            sessionmaker(
                engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )
        return engine, session_factory

    async def close_connections(self):
        await self._db_engine.dispose() 


class ConnectionHandler:
    def __init__(self):
        self._session: Optional[AsyncSession] = None
        self._connection_manager = ConnectionManager()

    @property
    def session(self):
        if not self._session:
            session_factory = self._connection_manager.get_session_factory()
            self._session = session_factory()
        return self._session

    async def session_commit(self):
        await self.session.commit()

    async def close(self):
        if self._session:
            await self._session.close()


async def get_connection_handler_for_app():
    connection_handler = ConnectionHandler()
    try:
        yield connection_handler
    finally:
        await connection_handler.close()


# async def get_current_user(token: str = Depends(oauth2_bearer)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get('username')
#         user_id = payload.get('id')
#         if username is None or user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
#         return {'username': username, 'id': user_id}
#     except ExpiredSignatureError:
#         # Handle token expiration
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Token has expired. Please reauthenticate.') from None
#     except JWTError as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate user. error: {e}')
