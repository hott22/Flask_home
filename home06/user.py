from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    user_name: str = Field(..., title='Name', max_length=10)
    user_surname: str = Field(..., title='Surname', max_length=20)
    user_email: str = Field(..., title='Email', max_length=50)
    user_password: str = Field(..., title='Password', max_length=10)


class UserIn(BaseModel):
    user_name: str = Field(..., title='Name', max_length=10)
    user_surname: str = Field(..., title='Surname', max_length=20)
    user_email: str = Field(..., title='Email', max_length=50)
    user_password: str = Field(..., title='Password', max_length=10)
