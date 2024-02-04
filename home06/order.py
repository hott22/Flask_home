from pydantic import BaseModel, Field
from home06.user import User
from home06.product import Product
import datetime


class Order(BaseModel):
    order_id: int
    user: User = Field(...,)
    product: Product = Field(...,)
    order_date: datetime.date = Field(..., title='Order date')
    order_status: bool = Field(..., title='Status')


class OrderIn(BaseModel):
    user: int
    product: int
    order_date: datetime.date = Field(..., title='Order date')
    order_status: bool = Field(..., title='Status')



