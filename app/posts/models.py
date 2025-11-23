from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from datetime import datetime
from enum import Enum
from app import db

class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

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

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post id={self.id} title='{self.title}' category='{self.category.value}'>"

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag id={self.id} name='{self.name}'>"
