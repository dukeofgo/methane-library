from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .. database import Base
from .. users import models

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(64))
    author: Mapped[str] = mapped_column(String(64))
    edition: Mapped[str] = mapped_column(String(64), nullable=True)
    publisher: Mapped[str] = mapped_column(String(64))
    publish_date: Mapped[str] = mapped_column(String(64), nullable=True)
    publish_place: Mapped[str] = mapped_column(String(64), nullable=True)
    number_of_pages: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    language: Mapped[str] = mapped_column(String(32), nullable=True)
    isbn: Mapped[str] = mapped_column(String(13))
    lccn: Mapped[str] = mapped_column(String(64), nullable=True)
    subtitle: Mapped[str] = mapped_column(String(1024), nullable=True)
    subjects: Mapped[str] = mapped_column(String(256), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    loan_to_user: Mapped[models.User] = relationship(back_populates="borrowed_books")

    added_date: Mapped[Date] = mapped_column(default=Date.today)
    borrowed_date: Mapped[Date] = mapped_column(nullable=True)
    returned_date: Mapped[Date] = mapped_column(nullable=True)
    
    is_borrowed: Mapped[Boolean] = mapped_column(default=False)
