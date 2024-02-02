from hashlib import sha256

import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
import logging
from fastapi.templating import Jinja2Templates
from home05.task import Task

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="./home05/templates")
tasks = []


@app.get('/', response_class=HTMLResponse)
async def add_task_get(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/task', response_class=HTMLResponse)
async def add_task_post(request: Request):
    logger.info('Отработал POST запрос.')
    title = 'Задача'
    form = await request.form()
    form = jsonable_encoder(form)
    task = Task(id=len(tasks), title=form['title'], description=form['description'], completed=form['completed'])
    tasks.append(task)
    return templates.TemplateResponse('task.html', {'request': request, 'task': task, 'title': title})


@app.get('/task_get/{task_id}', response_class=HTMLResponse)
async def get_task(request: Request, task_id: int):
    title = f'Задача с id: {task_id}'
    for task in tasks:
        if task_id == task.id:
            return templates.TemplateResponse('task.html', {'request': request, 'task': task, 'title': title})
    return templates.TemplateResponse('task.html', {'request': request, 'task_id': task_id, 'title': title})


@app.get('/tasks', response_class=HTMLResponse)
async def get_all_tasks(request: Request):
    title = 'Все задачи'
    return templates.TemplateResponse('tasks.html', {'request': request, 'tasks': tasks, 'title': title})


# @app.get('/task_put/{task_id}', response_class=HTMLResponse)
# async def change_task_get(request: Request, task_id: int):
#     title = f'Задача с id {task_id}'
#     for task in tasks:
#         if task_id == task.id:
#             print(task.id)
#             return templates.TemplateResponse('tasks_put.html', {'request': request, 'task': task, 'title': title})
#     print('asfasgas')
#     return templates.TemplateResponse('task.html', {'request': request, 'task_id': task_id, 'title': title})


# @app.post('/task_put', response_class=HTMLResponse)
# async def change_task_put(request: Request):
#     form = await request.form()
#     form = jsonable_encoder(form)
#     print(form)
#     for task in tasks:
#         if task.id:
#             task_old = task.copy()
#             task.title = form['title']
#             task.description = form['description']
#             task.completed = form['completed']
#             return templates.TemplateResponse('task_old_new.html', {'request': request, 'task_old': task_old,
#                                                                  'task': task})


@app.put('/{task_id}', response_model=str | Task)
async def put_task(task_id: int, task_: Task):
    logger.info('Отработал PUT запрос.')
    for task in tasks:
        if task_id == task.id:
            task.title = task_.title
            task.description = task_.description
            task.completed = task_.completed
            return task
    return 'Нет такой задачи'


@app.delete('/{task_id/', response_model=str)
async def del_task(task_id: int):
    logger.info('Отработал DELETE запрос.')
    for task in tasks:
        if task_id == task.id:
            tasks.remove(task)
            return f'Удален пользователь с id: {task_id}'
    return 'Нет такого юзера'
