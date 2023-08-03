import json

from rich.status import Status
from ttxc import TelebirrTxChecker

from mereja.ui import make_transaction_table
from mereja.utils import with_live, save_file


@with_live("Checking transaction...")
async def check_transaction(transaction_id: str, status: Status):
    tr_checker = TelebirrTxChecker()
    transaction = await tr_checker.get_transaction(transaction_id)
    if not transaction:
        status.console.print("[bold yellow]No transaction found")
        return
    status.stop()
    return make_transaction_table(transaction)


@with_live("Checking transaction...")
async def export_transaction(transaction_id: str, path: str, status: Status):
    path = path or "."
    tr_checker = TelebirrTxChecker()
    transaction = await tr_checker.get_transaction(transaction_id)
    if not transaction:
        status.console.print("[bold yellow]No transaction found")
        return
    status.update(f"Saving transaction to {path}/{transaction_id}.json")
    save_file(
        path + f"/{transaction_id}.json", json.dumps(transaction.dict(), indent=4)
    )
    return status.console.print(f"Transaction saved to {path}/{transaction_id}.json")
