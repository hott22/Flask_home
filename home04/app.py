import os
import threading
import multiprocessing
import asyncio
import time
import aiofiles

import aiohttp
import requests

url = ['https://gas-kvas.com/uploads/posts/2023-02/1675495569_gas-kvas-com-p-luchshie-kartinki-dlya-fonovogo-risunka'
       '-ra-31.jpg',
       'https://w.forfun.com/fetch/4a/4af0bcc2b0c34fd573eca9f1be9ab245.jpeg',
       'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666206241_12-mykaleidoscope-ru-p-kartinka-na-zastavku-oboi'
       '-12.jpg',
       'https://mobimg.b-cdn.net/v3/fetch/f4/f4e488ef69ea10573c0ce9cfbaf08643.jpeg',
       'https://gas-kvas.com/uploads/posts/2023-02/1675446644_gas-kvas-com-p-kartinki-na-fonovii-risunok-rabochego-11'
       '.jpg']


def download(url_img):
    response = requests.get(url_img).content
    return response


def timed(func):
    def wrapper():
        t_start = time.time()
        func()
        t_end = time.time()
        print(f'Method {func.__name__}. Downloaded in {t_end - t_start:.2f} seconds')

    return wrapper


def save_image(image: str, type_save_dir: str):
    image_name = image.split('/')[-1]
    if not os.path.exists(type_save_dir):
        os.mkdir(type_save_dir)
    with open(type_save_dir + '/' + image_name, 'wb') as handler:
        handler.write(download(image))


@timed
def sync_method():
    for image in url:
        save_image(image, 'sync')


@timed
def threaded():
    threads = []
    for image in url:
        thread = threading.Thread(target=save_image, args=(image, 'threaded',))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


@timed
def processed():
    processes = []
    for image in url:
        process = multiprocessing.Process(target=save_image, args=(image, 'processed',))
        processes.append(process)
        process.start()
    for proc in processes:
        proc.join()


async def async_download(url_img, type_save_dir):
    if not os.path.exists(type_save_dir):
        os.mkdir(type_save_dir)
    image_name = url_img.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        image = await session.request(method='GET', url=url_img)
        async with aiofiles.open(type_save_dir + '/' + image_name, mode='wb') as file:
            await file.write(await image.read())


async def async_main(ursl):
    tasks = []
    for url_ in ursl:
        task = asyncio.ensure_future(async_download(url_, 'async'))
        tasks.append(task)
    await asyncio.gather(*tasks)


@timed
def w_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(url))


if __name__ == '__main__':
    sync_method()
    threaded()
    processed()
    w_async()
