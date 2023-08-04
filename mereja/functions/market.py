import json

from jiji import JiJi
from questionary import Choice
from rich.status import Status

from mereja.ui import start_market_ui
from mereja.utils import ask, with_live, save_file, get_path


@with_live("Searching for {query}...")
async def search_for_product(
    query: str,
    status: Status,
    page: int = 1,
    limit: int = -1,
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
                f"{product.title} - [{product.price} ETB] "
                f"{f' ({product.price_type})' if product.price_type else ' (Fixed)'}",
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
async def get_trending_products(status: Status, limit: int = -1, page: int = 1) -> None:
    jiji = JiJi()
    products = await jiji.get_trending(page)
    if not products:
        status.console.print("[bold yellow]No products found")
        return
    status.console.print(f"[bold green]Found {len(products)} products")
    products = products[:limit]
    status.stop()
    ans = await ask(
        message="Select a product",
        choice=[
            Choice(
                f"{product.title} - [{product.price} ETB]"
                f" {f' ({product.price_type})' if product.price_type else ' (Fixed)'}",
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
async def export_products(
    status: Status,
    limit: int,
    path: str,
    query: str = None,
    page: int = 1,
):
    jiji = JiJi()
    if query:
        products = await jiji.search(query, page)
    else:
        products = await jiji.get_trending(page)
    if not products:
        status.console.print("[bold yellow]No products found")
        return
    status.console.print(f"[bold green]Found {len(products)} products")
    products = products[:limit] if limit else products
    path = get_path(path, "products")
    status.update(f"Exporting {len(products)} products to {path}")
    products_dict = []
    for product in products:
        product = await product.get_product()
        products_dict.append(product.dict())
    save_file(path, json.dumps(products_dict, indent=4))
    return status.console.print(f"Products saved to {path}")
