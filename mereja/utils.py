import asyncio
import io
import random
import re
import time
from contextlib import contextmanager
from functools import wraps, partial
from pathlib import Path
from typing import Callable

import httpx
import qrcode
import questionary
from bs4 import BeautifulSoup
from httpcore import ConnectTimeout
from httpx import ConnectError
from questionary import Choice
from rich.console import Console
from rich.table import Table

from mereja import constants


class Back(Exception):
    pass


def random_spinner():
    return random.choice(constants.SPINNERS)


def rmv_etb(text: str) -> float:
    if isinstance(text, str):
        return round(float(re.search(r"(\d+\.\d+)", text).group(1)), 4)
    if isinstance(text, float):
        return round(text, 4)


@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * 0.04)


def bold_numbers(text: str) -> str:
    """Bold numbers in a string."""
    return re.sub(r"(\d+)", r"[b]\1[/b]", text)


async def get_forex_data() -> list[dict]:
    """Get forex data from CBE."""
    async with httpx.AsyncClient() as client:
        response = await client.get(constants.FOREX_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", attrs={"height": "8"})
        return [
            {
                "currency": f.find("td", attrs={"width": "130"}).get_text(strip=True),
                "buy": f.find("td", attrs={"width": "94"}).get_text(strip=True),
                "sell": f.find("td", attrs={"width": "102"}).get_text(strip=True),
            }
            for f in table
        ]


def loop_colum(table: Table, columns: list):
    for column in columns:
        with beat(5):
            table.add_column(column)


def loop_row(table: Table, rows: list[tuple]):
    for row in rows:
        with beat(5):
            table.add_row(*row)


async def ask(message: str, choice: list[Choice]):
    # choice.append(
    #     Choice(
    #         title="🔙 Back",
    #         value="back",
    #     )
    # )

    return await questionary.select(
        message=message,
        choices=choice,
        qmark="📝",
        style=constants.STYLE,
        use_arrow_keys=True,
        use_jk_keys=True,
        instruction="Use [enter] to confirm",
    ).ask_async()


def make_qr(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()


def with_live(text: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            console = Console()
            with console.status(
                f"[bold green] {text.format(**kwargs)}", spinner=random_spinner()
            ) as status:
                try:
                    await func(*args, **kwargs, status=status)
                except ConnectError:
                    console.print("[bold red]No internet connection.")
                    exit(1)
                except KeyboardInterrupt:
                    # print("Exiting...")
                    # exit(0)
                    return
                except ConnectTimeout:
                    console.print("[bold red]Connection timeout.")
                    exit(1)
                except Exception as e:
                    print(e)
                    exit(1)

        return wrapper

    return decorator


def save_file(file_name: str, content: str):
    Path(file_name).write_text(content)


def get_path(p: str | None, name: str) -> str:
    p = p or "."
    return p if p.endswith(".json") else p + f"/{name}.json"


def awaitable(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def no_ans_or_back(ans: str):
    if not ans:
        raise KeyboardInterrupt
