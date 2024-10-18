from src.fastapi_admin import app
from src.fastapi_admin import app as admin_app
from src.fastapi_admin import setup_admin
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema="public"))


class Author(Base):
    __tablename__ = "authors"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True, nullable=True)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")


# Setup FastAPI Admin
setup_admin(app=app, admin_app=admin_app)

# Register your model with FastAPI Admin
admin_app.register("Items", Item)
