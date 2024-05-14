import random
from asyncio import sleep


def powers_of(logbase, count, lower=0, include_zero=True):
    """Returns a list of count powers of logbase (from logbase**lower)."""
    if not include_zero:
        return [logbase**i for i in range(lower, count + lower)]
    else:
        return [0] + [logbase**i for i in range(lower, count + lower)]


sleep_timeout_choice = (
    0.02,
    0.02,
    0.03,
    0.03,
    0.04,
    0.04,
    0.05,
    0.05,
    0.05,
    0.05,
    0.06,
    0.06,
    0.07,
    0.07,
    0.08,
    0.08,
    0.1,
    0.2,
    0.4,
    0.5,
)


def get_random_sleep_timeout():
    return random.choice(sleep_timeout_choice)


async def sleep_random():
    await sleep(get_random_sleep_timeout())
