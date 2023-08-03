from jiji import JiJi
from questionary import Choice
from rich.status import Status

from mereja.ui import start_market_ui
from mereja.utils import ask, with_live


@with_live("Searching for {query}...")
async def search_for_product(
    query: str,
    status: Status,
    page: int = 1,
    limit: int = 10,
) -> None:
    jiji = JiJi()
    product = await jiji.search(query, page)
    if not product:
        status.console.print("[bold yellow]No products found")
        return
    products = product.products
    if limit:
        products = product.products[:limit]
    status.console.print(f"[bold green]Found {len(product.products)} products")
    status.stop()
    ans = await ask(
        message="Select a product",
        choice=[
            Choice(
                f"{product.title} - [{product.price}]",
                value=product.id,
            )
            for product in products
        ],
    )
    if not ans:
        return
    product = await jiji.get_product(ans)
    start_market_ui(product)


@with_live("Getting trending products...")
async def get_trending_products(status: Status, page: int = 1) -> None:
    jiji = JiJi()
    products = await jiji.get_trending(page)
    if not products:
        status.console.print("[bold yellow]No products found")
        return
    products = products[:10]
    status.console.print(f"[bold green]Found {len(products)} products")
    status.stop()
    ans = await ask(
        message="Select a product",
        choice=[
            Choice(
                f"{product.title} - [{product.price} ETB{f' ({product.price_type})' if product.price_type else ''}]",
                value=product.id,
            )
            for product in products
        ],
    )
    if not ans:
        return
    product = await jiji.get_product(ans)
    start_market_ui(product)
