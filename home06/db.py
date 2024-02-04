import databases
import sqlalchemy
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///home06/shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'user',
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String(10)),
    sqlalchemy.Column("user_surname", sqlalchemy.String(20)),
    sqlalchemy.Column("user_email", sqlalchemy.String(50)),
    sqlalchemy.Column("user_password", sqlalchemy.String(10)),
)

products = sqlalchemy.Table(
    'product',
    metadata,
    sqlalchemy.Column('product_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('product_title', sqlalchemy.String(50)),
    sqlalchemy.Column('product_description', sqlalchemy.String),
    sqlalchemy.Column('product_price', sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    'order',
    metadata,
    sqlalchemy.Column('order_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey("user.user_id"), nullable=False),
    sqlalchemy.Column('product', sqlalchemy.Integer, sqlalchemy.ForeignKey("product.product_id"), nullable=False),
    sqlalchemy.Column('order_date', sqlalchemy.DateTime),
    sqlalchemy.Column('order_status', sqlalchemy.Boolean),
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

