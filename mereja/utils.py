import asyncio
import io
import random
import re
import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable

import httpx
import qrcode
import questionary
from bs4 import BeautifulSoup
from httpx import ConnectError
from questionary import Choice
from rich.console import Console
from rich.status import Status
from rich.table import Table

from mereja import constants


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
                    print("Exiting...")
                    exit(0)
                except Exception as e:
                    print(e)
                    exit(1)

        return wrapper

    return decorator


@with_live("Getting forex data...")
async def show_forex_data(status: Status = None) -> None:
    await asyncio.sleep(5)
    forex_data = await get_forex_data()

    if not forex_data:
        status.console.print("[bold yellow]No forex found")
        return
    status.stop()
    return status.console.print(forex_data)


def save_file(file_name: str, content: str):
    with open(file_name, "w") as f:
        f.write(content)
