from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from enum import Enum
from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(
        db.Enum(PostCategory, name="post_category_enum"),
        default=PostCategory.OTHER,
        nullable=False
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post id={self.id} title='{self.title}' category='{self.category.value}'>"
