from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.config.database import get_session
from src.connection.connection import ConnectionHandler, get_connection_handler_for_app
from src.crud import BOOKDAO, BOOKAsyncDAO
from src.schemas import BookCreate, BookResponse

book_router = APIRouter()



# @book_router.get("/{book_id}")
# def read_otb(book_id):
#     try:

#         session = get_session()
#         book_dao = BOOKDAO(session)
#         result = book_dao.get_book_by_id(book_id)

#         session.close()

#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         session.close()

@book_router.post("/", response_model=BookResponse)
def create_book(book: BookCreate):
    try:
        session = get_session()
        book_dao = BOOKDAO(session)
        created_book = book_dao.create_book(book)
        return created_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@book_router.get("/")
def read_otb():
    try:

        session = get_session()
        book_dao = BOOKDAO(session)
        result = book_dao.get_all_book()

        session.close()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
        

@book_router.get("/{book_id}")
async def read_otb(book_id: int,  
                   connection_handler: ConnectionHandler = Depends(get_connection_handler_for_app),
):
    try:
        session = connection_handler.session
        book_dao = BOOKAsyncDAO(session)
        result = await book_dao.get_book_by_id(book_id)
        await session.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await session.close()

