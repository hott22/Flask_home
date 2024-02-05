from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: int
    product_title: str = Field(..., title='Title', max_length=50)
    product_description: str = Field(..., title='Description')
    product_price: int = Field(..., title='Price', gt=0)


class ProductIn(BaseModel):
    product_title: str = Field(..., title='Title', max_length=50)
    product_description: str = Field(..., title='Description')
    product_price: int = Field(..., title='Price', gt=0)
