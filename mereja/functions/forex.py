import json

from rich.status import Status

from mereja.ui import make_forex_table
from mereja.utils import with_live, get_forex_data, save_file


@with_live("Getting forex data...")
async def get_forex(live: bool, status: Status = None):
    forex = await get_forex_data()
    if not forex:
        status.console.print("[bold yellow]No forex found")
        return
    status.stop()
    return status.console.print(await make_forex_table(forex, live))


@with_live("Getting forex data...")
async def export_forex_data(path: str, status: Status):
    path = path or "."
    forex = await get_forex_data()
    if not forex:
        status.console.print("[bold yellow]No forex found")
        return
    status.update(f"Saving forex data to {path}/forex.json")
    save_file(path + f"/forex.json", json.dumps(forex, indent=4))
    return status.console.print(f"Forex data saved to {path}/forex.json")
