from home06.db import products, users, orders, database, metadata, engine
from home06.user import User, UserIn
from home06.product import Product, ProductIn
from home06.order import Order, OrderIn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="home06/templates")
metadata.create_all(engine)


@app.get('/', response_class=HTMLResponse)
async def add(request: Request):
    '''Главная страница'''
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/user/', response_class=HTMLResponse)
async def add_user_get(request: Request):
    '''Форма добавление пользователя'''
    return templates.TemplateResponse('user_add.html', {'request': request})


@app.get('/product/', response_class=HTMLResponse)
async def add_product_get(request: Request):
    '''Форма добаления товара'''
    return templates.TemplateResponse('product_add.html', {'request': request})


@app.get('/order/', response_class=HTMLResponse)
async def add_order_get(request: Request):
    '''Форма добаления заказа'''
    return templates.TemplateResponse('oder_add.html', {'request': request})


@app.get('/user_get_id/', response_class=HTMLResponse)
async def user_get_id(request: Request):
    '''Форма получение пользователя по ID'''
    return templates.TemplateResponse('user_get_id.html', {'request': request})


@app.get('/product_get_id/', response_class=HTMLResponse)
async def product_get_id(request: Request):
    '''Форма получение товара по ID'''
    return templates.TemplateResponse('product_get_id.html', {'request': request})


@app.get('/order_get_id/', response_class=HTMLResponse)
async def order_get_id(request: Request):
    '''Форма получение заказа по ID'''
    return templates.TemplateResponse('order_get_id.html', {'request': request})


# @app.get('/user_del_id/', response_class=HTMLResponse)
# async def user_del_id(request: Request):
#     return templates.TemplateResponse('user_del_id.html', {'request': request})


@app.post('/user_add/', response_class=HTMLResponse)
async def add_user(request: Request):
    '''Добавление пользователя'''
    title = 'Пользователь'
    form = await request.form()
    form = jsonable_encoder(form)
    userIn = UserIn(user_name=form['user_name'], user_surname=form['user_surname'], user_email=form['user_email'],
                    user_password=form['user_password'])
    query = users.insert().values(**userIn.model_dump())
    last_record_id = await database.execute(query)
    user = {**userIn.model_dump(), 'user_id': last_record_id}
    return templates.TemplateResponse('user.html', {'request': request, 'user': user, 'title': title})


@app.post('/product_add/', response_class=HTMLResponse)
async def add_product(request: Request):
    '''Добавление товара'''
    title = 'Товар'
    form = await request.form()
    form = jsonable_encoder(form)
    productIn = ProductIn(product_title=form['product_title'], product_description=form['product_description'],
                          product_price=form['product_price'])
    query = products.insert().values(**productIn.model_dump())
    last_record_id = await database.execute(query)
    product = {**productIn.model_dump(), 'product_id': last_record_id}
    return templates.TemplateResponse('product.html', {'request': request, 'product': product, 'title': title})


@app.post('/order_add/', response_class=HTMLResponse)
async def add_order(request: Request):
    '''Добавление заказа'''
    title = 'Заказ'
    form = await request.form()
    form = jsonable_encoder(form)
    orderIn = OrderIn(user=form['user'], product=form['product'], order_date=form['order_date'],
                      order_status=form['order_status'])
    query = orders.insert().values(**orderIn.model_dump())
    print(query)
    last_record_id = await database.execute(query)
    order = {**orderIn.model_dump(), 'order_id': last_record_id}
    return templates.TemplateResponse('order.html', {'request': request, 'order': order, 'title': title})


@app.get('/users/', response_class=HTMLResponse)
async def get_all_users(request: Request):
    '''Получения всех пользователей'''
    title = 'Все пользователи'
    query = users.select()
    all_users = await database.fetch_all(query)
    return templates.TemplateResponse('users.html', {'request': request, 'users': all_users, 'title': title})


@app.get('/products/', response_class=HTMLResponse)
async def get_all_products(request: Request):
    '''Получения всех товаров'''
    title = 'Все товары'
    query = products.select()
    all_products = await database.fetch_all(query)
    return templates.TemplateResponse('products.html', {'request': request, 'products': all_products, 'title': title})


@app.get('/orders/', response_class=HTMLResponse)
async def get_all_orders(request: Request):
    '''Получения всех заказов'''
    title = 'Все заказы'
    query = orders.select()
    all_orders = await database.fetch_all(query)
    return templates.TemplateResponse('orders.html', {'request': request, 'orders': all_orders, 'title': title})


@app.get('/user_id/', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int = 0):
    '''Получение пользователя по ID'''
    title = f"Пользователь с id: {user_id}"
    query = users.select().where(users.c.user_id == user_id)
    user = await database.fetch_one(query)
    return templates.TemplateResponse('user.html',
                                      {'request': request, 'user': user, 'title': title, 'user_id': user_id})


@app.get('/product_id/', response_class=HTMLResponse)
async def get_product(request: Request, product_id: int = 0):
    '''Получение товара по ID'''
    title = f"Товар с id: {product_id}"
    query = products.select().where(products.c.product_id == product_id)
    product = await database.fetch_one(query)
    return templates.TemplateResponse('product.html',
                                      {'request': request, 'product': product, 'title': title,
                                       'product_id': product_id})


@app.get('/order_id/', response_class=HTMLResponse)
async def get_order(request: Request, order_id: int = 0):
    '''Получение заказа по ID'''
    title = f"Заказ с id: {order_id}"
    query = orders.select().where(orders.c.order_id == order_id)
    order = await database.fetch_one(query)
    return templates.TemplateResponse('order.html',
                                      {'request': request, 'order': order, 'title': title,
                                       'order_id': order_id})


@app.delete('/user_delete/{user_id}', response_model=str)
async def del_user(user_id: int):
    '''Удаление пользователя'''
    query = users.delete().where(users.c.user_id == user_id)
    await database.execute(query)
    return f'Пользователь с ID {user_id} удален'


@app.delete('/product_delete/{product_id}', response_model=str)
async def del_product(product_id: int):
    '''Удаление товара'''
    query = products.delete().where(products.c.product_id == product_id)
    await database.execute(query)
    return f'Товар с ID {product_id} удален'


@app.delete('/order_delete/{order_id}', response_model=str)
async def del_order(order_id: int):
    '''Удаление заказа'''
    query = orders.delete().where(orders.c.order_id == order_id)
    await database.execute(query)
    return f'Заказ с ID {order_id} удален'


@app.put('/user_put/{user_id}', response_model=User)
async def user_put(user_id: int, new_user: UserIn):
    '''Изменение пользователя'''
    query = users.update().where(users.c.user_id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), 'user_id': user_id}


@app.put('/product_put/{product_id}', response_model=Product)
async def product_put(product_id: int, new_product: ProductIn):
    '''Изменение товара'''
    query = products.update().where(products.c.product_id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), 'product_id': product_id}


@app.put('/order_put/{order_id}', response_model=Order)
async def order_put(order_id: int, new_order: OrderIn):
    '''Изменение заказа'''
    query = orders.update().where(orders.c.order_id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), 'order_id': order_id}
