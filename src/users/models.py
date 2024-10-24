from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from .. database import Base
from .. books import models


class UserStatus(enum.Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True) 
    name: Mapped[str] = mapped_column(String(64))
    age: Mapped[int] 
    status: Mapped[UserStatus] = mapped_column(nullable=False, default=UserStatus.USER)

    registered_date: Mapped[Date] = mapped_column(default=Date.today)
    hashed_password: Mapped[str]
    borrowed_books: Mapped[models.Book] = relationship(back_populates="loan_to_user")
    is_active: Mapped[Boolean] = mapped_column(default=True)
    is_borrower: Mapped[Boolean] = mapped_column(default=False)
    is_member: Mapped[Boolean] = mapped_column(default=False)