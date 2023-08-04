import asyncio
from typing import List, Union

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.traceback import install

from mereja.utils import get_forex_data, rmv_etb

install()


async def make_forex_table(forex: List[dict], live: bool) -> Union[Align, Table, None]:
    if live:
        table = create_table(forex, "Live Forex Data")
        with Live(
            Align.center(table), refresh_per_second=20, console=Console()
        ) as live_table:
            while True:
                try:
                    new_forex = await get_forex_data()
                    forex = get_changes(forex, new_forex)
                    new_table = create_table(forex, "Live Forex Data")
                    live_table.update(Align.center(new_table))
                    forex = new_forex
                    await asyncio.sleep(5)
                except KeyboardInterrupt:
                    return

    return Align.center(create_table(forex, "Forex Data"))


def create_table(forex: List[dict], title: str) -> Table:
    """Make a table for forex data."""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title=title,
        title_style="bold green",
    )
    table.add_column("Currency")
    table.add_column("Buying RATE", justify="right")
    table.add_column("Selling RATE", justify="right")
    for f in forex:
        table.add_row(
            f'[blue]{f["currency"]}', f'[cyan]{f["buy"]} ETB', f'[green]{f["sell"]} ETB'
        )
    return table


def check_changes(forex: List[dict], new_forex: List[dict]) -> bool:
    """Check if there is a change in forex data."""
    for f, n in zip(forex, new_forex):
        if rmv_etb(f["buy"]) != rmv_etb(n["buy"]) or rmv_etb(f["sell"]) != rmv_etb(
            n["sell"]
        ):
            return True
    return False


def get_changes(forex: List[dict], new_forex: List[dict]) -> List[dict]:
    """Get the changes in forex data."""
    changes = []
    for f, n in zip(forex, new_forex):
        if check_changes(forex, new_forex):
            if rmv_etb(f["buy"]) > rmv_etb(n["buy"]):
                n["buy"] = f'[red]- {rmv_etb(n["buy"])}'

            elif rmv_etb(f["buy"]) < rmv_etb(n["buy"]):
                n["buy"] = f'[green]+ {rmv_etb(n["buy"])}'

            if rmv_etb(f["sell"]) > rmv_etb(n["sell"]):
                n["sell"] = f'[red]- {rmv_etb(n["sell"])}'

            elif rmv_etb(f["sell"]) < rmv_etb(n["sell"]):
                n["sell"] = f'[green]+ {rmv_etb(n["sell"])}'
        changes.append(n)
    return changes
