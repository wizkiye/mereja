from rich.status import Status

from mereja.ui import make_forex_table
from mereja.utils import with_live, get_forex_data


@with_live("Getting forex data...")
async def get_forex(live: bool, status: Status = None):
    forex = await get_forex_data()
    if not forex:
        status.console.print("[bold yellow]No forex found")
        return
    status.stop()
    return status.console.print(await make_forex_table(forex, live))
