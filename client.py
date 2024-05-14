import os
from threading import Thread
from time import sleep

import requests


def make_requests(url: str, sleep_after_n_requests: int = 100, sleep_timeout: float = 2):
    while True:
        for i in range(sleep_after_n_requests):
            requests.get(url)

        sleep(sleep_timeout)


BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8000/').rstrip('/')


Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}', 'sleep_after_n_requests': 10, 'sleep_timeout': 1},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/items/1', 'sleep_after_n_requests': 20, 'sleep_timeout': 3.3},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/error', 'sleep_after_n_requests': 5, 'sleep_timeout': 7},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/exception/runtime', 'sleep_after_n_requests': 7, 'sleep_timeout': 4},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/exception/zero-division', 'sleep_after_n_requests': 15, 'sleep_timeout': 15},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/traffic?size=2048', 'sleep_after_n_requests': 50, 'sleep_timeout': 15},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/traffic?size=4096', 'sleep_after_n_requests': 25, 'sleep_timeout': 21},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/traffic?size=8192', 'sleep_after_n_requests': 15, 'sleep_timeout': 27},
).start()

Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/sleep', 'sleep_after_n_requests': 15, 'sleep_timeout': 1.7},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/sleep', 'sleep_after_n_requests': 20, 'sleep_timeout': 1.5},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/sleep', 'sleep_after_n_requests': 10, 'sleep_timeout': 0.5},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/sleep', 'sleep_after_n_requests': 100, 'sleep_timeout': 30},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/sleep', 'sleep_after_n_requests': 5, 'sleep_timeout': 5},
).start()
Thread(
    target=make_requests,
    kwargs={'url': f'{BASE_URL}/db/error', 'sleep_after_n_requests': 5, 'sleep_timeout': 30},
).start()
