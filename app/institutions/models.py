from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.users.models import User

class InstitutionType(db.Model):
    __tablename__ = "institution_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    institutions: Mapped[list["EducationInstitution"]] = relationship(
        back_populates="institution_type",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<InstitutionType id={self.id} type='{self.type_name}'>"


class EducationInstitution(db.Model):
    __tablename__ = "education_institutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("institution_types.id"),
        nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    institution_type: Mapped["InstitutionType"] = relationship(
        back_populates="institutions"
    )

    author: Mapped["User"] = relationship(
        back_populates="institutions"
    )

    def __repr__(self):
        return f"<EducationInstitution id={self.id} name='{self.name}'>"
