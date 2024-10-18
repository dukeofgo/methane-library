from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .. database import Base
from .. books.models import Book

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True ) 
    name: Mapped[str] = mapped_column(String(64))
    age: Mapped[int] 
    registered_date: Mapped[Date] = mapped_column(default=Date.today)
    hashed__password: Mapped[str]
    borrowed_books: Mapped["Book"] = relationship(back_populates="loan_to_user")

    is_active: Mapped[Boolean] = mapped_column(default=True)
    is_borrower: Mapped[Boolean] = mapped_column(default=False)
    is_member: Mapped[Boolean] = mapped_column(default=False)