from sqlalchemy import create_engine, ForeignKey, String, Float, TIMESTAMP, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List, Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class SaleProduct(Base):
    __tablename__ = "sale_product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    sale_id: Mapped[int] = mapped_column(ForeignKey("sale.id"))

    extra_data: Mapped[Optional[str]]

    sales: Mapped["Sale"] = relationship(back_populates="product_association")
    products: Mapped["Product"] = relationship(back_populates="sale_association")


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[Optional[str]]

    sale_association: Mapped[List["SaleProduct"]] = relationship(secondary="sale_product", back_populates="products")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r}, description={self.description!r})"


class Sale(Base):
    __tablename__ = "sale"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    customer: Mapped[str] = mapped_column(String(255))

    product_association: Mapped[List["SaleProduct"]] = relationship(secondary="sale_product", back_populates="sales")

    def __repr__(self) -> str:
        return f"Sale(id={self.id!r}, date={self.date!r}, customer={self.customer!r})"


db_connection_str = 'postgresql://farzan:88775566@localhost:5432/new_sqlalchemy'
engine = create_engine(db_connection_str, echo=True)

Base.metadata.create_all(engine)

""" Inserting Values into Product """
with Session(engine) as session:

    smart_phone = Product(name="Smart Phone", price=149.99)
    laptop = Product(name="Laptop", price=329.99)
    sandwich = Product(name="Sandwich", price=2, description="It's not delicious!")

    sale1 = Sale(date=datetime(2024, 2, 23, 19, 38, 59), customer="Ali")
    sale2 = Sale(date=datetime(2024, 4, 29, 17, 57, 54), customer="Mohammad")
    sale3 = Sale(date=datetime(2024, 3, 21, 22, 30, 31), customer="Hasan")
    sale4 = Sale(date=datetime(2024, 4, 29, 8, 13, 13), customer="Farzan")

    sale_product1 = SaleProduct(product_id=smart_phone.id, sale_id=sale2.id, extra_data="Mohammad bought Smart Phone.")
    sale_product2 = SaleProduct(product_id=smart_phone.id, sale_id=sale1.id, extra_data="Ali bought Smart Phone.")
    sale_product3 = SaleProduct(product_id=laptop.id, sale_id=sale2.id, extra_data="Mohammad bought Laptop.")
    sale_product4 = SaleProduct(product_id=sandwich.id, sale_id=sale3.id, extra_data="Hasan bought Sandwich.")
    sale_product5 = SaleProduct(product_id=laptop.id, sale_id=sale4.id, extra_data="Farzan bought Laptop.")
    sale_product6 = SaleProduct(product_id=sandwich.id, sale_id=sale4.id, extra_data="Farzan bought Sandwich.")
    sale_product7 = SaleProduct(product_id=smart_phone.id, sale_id=sale3.id, extra_data="Hasan bought Smart Phone.")
    sale_product8 = SaleProduct(product_id=laptop.id, sale_id=sale1.id, extra_data="Ali bought Laptop.")

    session.add_all([smart_phone, laptop, sandwich, sale1, sale2, sale3, sale4, sale_product1, sale_product2,
                     sale_product3, sale_product4, sale_product5, sale_product6, sale_product7, sale_product8])

    session.commit()

# """ Inserting Values into Sale """
# with Session(engine) as session2:
#
#
#     session2.add_all([sale1, sale2, sale3, sale4])
#
#     session2.commit()
#
# """ Inserting Values into SaleProduct """
# with Session(engine) as session3:
#
#
#     session3.add_all([sale_product1, sale_product2, sale_product3, sale_product4, sale_product5, sale_product6,
#                       sale_product7, sale_product8])
#
#     session3.commit()

""" Simple SELECT """
session4 = Session(engine)

stmt = select(Product).where(Product.name.in_(["Laptop", "Smart Phone"]))

for product in session4.scalars(stmt):
    print(product)

""" SELECT with JOIN """
stmt2 = (
    select(Sale)
    .join(Sale.product_association)
    .where(Product.name.in_(["Sandwich"]))
    .where(Sale.customer.in_(["Farzan"]))
)
sandwich_of_farzan = session4.scalars(stmt2).one()

stmt4 = (
    select(Sale)
    .join(Sale.product_association)
    .where(Product.description.in_(["It's not delicious!"]))
)

sandwich_description = session4.scalars(stmt4).one()


""" Make Changes """
stmt3 = select(Product).where(Product.name.in_(["Laptop"]))
laptop = session4.scalars(stmt3).one()

laptop.sale.append(Sale(date=datetime(2024, 4, 29, 8, 13, 13), customer="Hasan"))

sandwich_of_farzan.date = datetime(2023, 4, 29, 8, 13, 13)

session4.commit()

""" Some Deletes """
session5 = Session(engine)
sandwich = session5.get(Product, 3)
sandwich.description.remove(sandwich_description)
session5.flush()
session5.delete(sandwich)
session5.commit()
