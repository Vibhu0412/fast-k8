from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession

# Example implementation of BOOKDAO, assuming get_book_by_id and create_book methods
class BOOKDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_book_by_id(self, book_id: int):
        return self.db_session.query(models.Book).filter(models.Book.id == book_id).first()
    
    def create_book(self, book: schemas.BookCreate):
        db_book = models.Book(**book.dict())
        self.db_session.add(db_book)
        self.db_session.commit()
        self.db_session.refresh(db_book)
        return db_book
    
    def get_all_book(self):
        return self.db_session.query(models.Book).all()

class BOOKAsyncDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def get_book_by_id(self, book_id: int):
        query = select(models.Book).where(models.Book.id == book_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()
    
    async def create_book(self, book: schemas.BookCreate):
        db_book = models.Book(**book.dict())
        self.db_session.add(db_book)
        await self.db_session.commit()
        await self.db_session.refresh(db_book)
        return db_book
    
    async def get_all_books(self):
        query = select(models.Book)
        result = await self.db_session.execute(query)
        return result.scalars().all()