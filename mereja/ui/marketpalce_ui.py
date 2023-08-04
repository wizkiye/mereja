from time import sleep

from jiji.types import User, Product
from rich import box
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from mereja.utils import make_qr, bold_numbers


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )

    layout["side"].split(
        Layout(name="seller"),
        Layout(
            name="qr",
            ratio=3,
        ),
    )
    return layout


def product_details(product: Product) -> Panel:
    attributes = Table(
        show_header=False,
        expand=True,
        box=box.ROUNDED,
        style="green",
    )
    attributes.add_column()
    for attr in product.attributes:
        attributes.add_row(
            f"[b]{attr.name}[/b]",
            f"[i blue]{attr.value}[/i blue]",
        )
    details = Table.grid()
    details.add_column(justify="left", ratio=1)
    details.add_row(
        f"[b]Description:[/b] ",
        f"[blue i]" + product.description.replace("<br>", " ").strip(),
    )
    details.add_row(
        f"[b]Location:[/b]",
        f"[blue]:earth_africa:{', '.join(product.regions_display).strip()}[/blue]",
    )
    details.add_row(
        f"[b]Posted:[/b] ",
        f"[blue b]:date: {product.date_created.strftime('%d %b %Y')}[/blue b]",
    )
    details.add_row(f"[b]Views:[/b]", f"[blue b]{product.page_views}[/blue b]")
    details.add_row(f"[b]Likes:[/b]", f"[blue b]:thumbsup:{product.fav_count}[/blue b]")
    details.add_row(f"[b]Price:[/b]", f"[blue b]:dollar:{product.price} ETB[/blue b]")
    details.add_row(f"[b]Category:[/b]", f"[blue]{product.category_slug}[/blue]")
    if product.price_valuation:
        details.add_row(
            f"[b]Price Range:[/b]",
            f"[blue]{bold_numbers(product.price_valuation.value)}[/blue]",
        )
        details.add_row(
            f"[b]Market:[/b]", f"[blue]{product.price_valuation.label}[/blue]"
        )
    return Panel(
        Group(
            Align.center(attributes, vertical="middle"),
            Align.center(details, vertical="middle"),
        ),
        border_style="green",
        box=box.ROUNDED,
    )


class Header:
    def __init__(self, title="JiJi"):
        self.title = title

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(self.title)
        return Panel(grid)


def user_details(user: User) -> Align:
    return Align.center(
        f"[b]Seller Name:[/b] [u blue]{user.name}[/u blue]\n"
        f"[b]Phone Number:[/b] [blue]{', '.join(user.phones)}[/blue]\n"
        f"[b]Email:[/b] [blue]{user.email}[/blue]\n"
        f"[b]lastSeen:[/b] [blue]{user.last_seen}[/blue]\n"
        f"[b]Registered at:[/b] [blue]{user.user_registered}[/blue] [b]ago\n",
        vertical="middle",
    )


def start_market_ui(product: Product):
    qr = make_qr(product.share_link)
    layout = make_layout()
    layout["header"].update(
        Header(
            f"[cyan]{product.title} - [b]{product.price} ETB[/b][/cyan] ({product.price_type or 'Fixed'})"
        )
    )
    layout["body"].update(product_details(product))
    layout["seller"].update(
        Panel(
            user_details(product.user),
            border_style="green",
            title="Seller Details",
            title_align="center",
        )
    )
    layout["qr"].update(
        Panel(
            Align.center(qr),
            border_style="cyan",
            title="QR Code",
            subtitle="Scan to view on your phone",
        )
    )
    with Live(layout, refresh_per_second=5, screen=True, auto_refresh=True):
        while True:
            try:
                sleep(1)
            except KeyboardInterrupt:
                break
