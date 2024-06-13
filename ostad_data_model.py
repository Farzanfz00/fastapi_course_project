from sqlalchemy import orm, MetaData
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db_connection_str = "postgresql://farzan:88775566@localhost:5432/new_sqlalchemy"
try:
    engine = create_engine(db_connection_str)
except Exception as e:
    print(e)
    raise Exception("Could not connect to database")


class Base(DeclarativeBase):
    metadata = MetaData(schema='public')
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class Publish(Base):
    __tablename__ = "publish"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id")
    )
    extra_data: Mapped[Optional[str]]
    author: Mapped["Author"] = relationship(back_populates="publishes")
    book: Mapped["Book"] = relationship(back_populates="publishes")


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    publishes: Mapped[List["Publish"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, email_address={self.email_address!r})"


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    publishes: Mapped[List[Publish]] = relationship(back_populates="book")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, name={self.name!r})"


Base.metadata.create_all(bind=engine)
