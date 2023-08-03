from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from ttxc.types import Transaction

from mereja.utils import beat, loop_colum, loop_row


def make_transaction_table(transaction: Transaction):
    console = Console()
    table = Table(
        show_header=False,
        header_style="bold magenta",
        title="Transaction information",
        title_style="bold green",
        box=box.ROUNDED,
        show_footer=False,
        show_lines=True,
    )
    with Live(
        Align.center(table), console=console, screen=False, refresh_per_second=20
    ):
        loop_row(
            table,
            [
                ("[b]Transaction ID", f"[b blue]{transaction.id}"),
                ("[b]Payer Name", f"[i cyan]{transaction.payer.name}"),
                ("[b]Payer Phone", f"[i cyan]{transaction.payer.phone}"),
                (
                    "[b]Payer Account Type",
                    f"[i cyan]{transaction.payer.account_type}",
                ),
                ("[b]Receiver Name", f"[i cyan]{transaction.receiver.name}"),
                ("[b]Receiver Phone", f"[i cyan]{transaction.receiver.phone}"),
                (
                    "[b]Receiver Account Type",
                    f"[b green]{transaction.status.upper()}",
                ),
            ],
        )
        #
    console.print("\n")
    table = Table(
        title="Transaction Details",
        title_style="bold green",
        box=box.ROUNDED,
        show_footer=False,
    )
    with Live(
        Align.center(table), console=console, screen=False, refresh_per_second=20
    ):
        loop_colum(
            table,
            [
                "Transaction ID",
                "Date",
                "Amount",
                "Discount",
                "VAT",
                "Total",
            ],
        )
        with beat(5):
            table.add_row(
                f"[b green]{transaction.id}",
                transaction.date.strftime("%d/%m/%Y %H:%M:%S"),
                f"[b blue]{transaction.total_sent} ETB",
                f"[b blue]{transaction.discount} ETB",
                f"[b blue]{transaction.vat} ETB",
                f"[b blue] {transaction.total_sent + transaction.discount + transaction.vat} ETB",
            )

    table = Table(
        show_lines=True,
    )
    with Live(
        Align.center(table), console=console, screen=False, refresh_per_second=20
    ):
        loop_colum(
            table,
            [
                "Total Amount in words",
                "Payment Mode",
                "Payment Reason",
                "Payment Channel",
            ],
        )
        table.add_row(
            f"[b u green]{transaction.total_amount_in_word}",
            f"[b u green]{transaction.mode}",
            f"[b u green]{transaction.reason}",
            f"[b u green]{transaction.channel.upper()}",
        )

        with beat(10):
            table.box = box.ROUNDED
