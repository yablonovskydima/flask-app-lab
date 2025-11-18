from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select"
    )

class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    category_id: Mapped[int | None] = mapped_column(
        db.ForeignKey('product_categories.id'), nullable=True
    )
    category: Mapped["ProductCategory"] = relationship(
        "ProductCategory",
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product id={self.id} name='{self.name}' price='{self.price}'>"
