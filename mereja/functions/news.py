import json

from pyEthioNews.providers import VOAAmharic
from questionary import Choice
from rich.status import Status

from mereja.ui import NewsView
from mereja.utils import ask, with_live, save_file, get_path


@with_live("Searching for {query}...")
async def search_news(
    query: str, status: Status, page: int = 1, limit: int = 10
) -> None:
    voa = VOAAmharic()
    news = await voa.search(query, page, limit)
    if not news:
        status.console.print("[bold yellow]No news found")
        return
    status.console.print(f"[bold green]Found {len(news)} news")
    status.stop()
    ans = await ask(
        message="Select a news",
        choice=[
            Choice(
                f"{news.title} - [{news.date}]",
                value=news.link,
            )
            for news in news
        ],
    )
    if not ans:
        return
    news = await voa.get(ans)
    await NewsView(news).run_async()


@with_live("Getting latest news...")
async def get_news(page: int, status: Status) -> None:
    voa = VOAAmharic()
    news = await voa.get_world_wide_news(page)
    if not news:
        status.console.print("[bold yellow]No news found")
        return
    status.console.print(f"[bold green]Found {len(news)} news")
    status.stop()
    ans = await ask(
        message="Select a news",
        choice=[
            Choice(
                f"{news.title} - [{news.date}]",
                value=news.link,
            )
            for news in news
        ],
    )
    if not ans:
        return
    news = await voa.get(ans)
    await NewsView(news).run_async()


@with_live("Getting latest news...")
async def export_news(
    status: Status, page: int, limit: int, path: str, query: str = None
) -> None:
    voa = VOAAmharic()
    if query:
        news = await voa.search(query, page, limit)
    else:
        news = await voa.get_world_wide_news(page)
    if not news:
        status.console.print("[bold yellow]No news found")
        return
    news = news[:limit] if limit else news
    status.console.print(f"[bold green]Found {len(news)} news")
    status.stop()
    path = get_path(path, f"latest_news_page_{page}")
    status.update(f"[bold green]Exporting to {path}")
    news_dict = []
    for news in news:
        news = await news.fetch()
        news_dict.append(news.dict())

    save_file(path, json.dumps(news_dict, indent=4))
    status.console.print(f"[bold green]Exported to {path}")
