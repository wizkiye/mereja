import random

import questionary
from pyEthioNews.providers import VOAAmharic
from pyethiojobs import EthioJobs
from questionary import Choice
from rich.console import Console

from ui import JobView, NewsView

console = Console()


style = questionary.Style(
    [
        ("qmark", "fg:#673ab7 bold"),
        ("question", "bold"),
        ("answer", "fg:#27781e italic"),
        ("pointer", "fg:#27781e bold"),
        ("highlighted", "fg:#27781e italic"),
        ("selected", "fg:#cc5454"),
        ("separator", "italic fg:#7c7d6b"),
        ("instruction", ""),
        ("text", "bold fg:#5cedd5"),
        ("disabled", "fg:#858585 italic"),
    ]
)


def random_spinner():
    spinners = [
        "dots",
        "dots2",
        "dots3",
        "dots4",
        "dots5",
        "dots6",
        "dots7",
        "dots8",
        "dots9",
        "dots10",
        "dots11",
        "dots12",
        "dots8Bit",
        "line",
        "line2",
        "pipe",
        "simpleDots",
        "simpleDotsScrolling",
        "star",
        "star2",
        "flip",
        "hamburger",
        "growVertical",
        "growHorizontal",
        "balloon",
        "balloon2",
        "noise",
        "bounce",
        "boxBounce",
        "boxBounce2",
        "triangle",
        "arc",
        "circle",
        "squareCorners",
        "circleQuarters",
        "circleHalves",
        "squish",
        "toggle",
        "toggle2",
        "toggle3",
        "toggle4",
        "toggle5",
        "toggle6",
        "toggle7",
        "toggle8",
        "toggle9",
        "toggle10",
        "toggle11",
        "toggle12",
        "toggle13",
        "arrow",
        "arrow2",
        "arrow3",
        "bouncingBar",
        "bouncingBall",
        "smiley",
        "monkey",
        "hearts",
        "clock",
        "earth",
        "material",
        "moon",
        "runner",
        "pong",
        "shark",
        "dqpb",
        "weather",
        "christmas",
        "grenade",
        "point",
        "layer",
        "betaWave",
        "aesthetic",
    ]
    return random.choice(spinners)


async def ask(message: str, choice: list[Choice]):
    return await questionary.select(
        message=message,
        choices=choice,
        qmark="📝",
        style=style,
        use_arrow_keys=True,
        use_indicator=True,
        use_jk_keys=True,
        instruction="Use [enter] to confirm",
    ).ask_async()


async def search_for_job(query: str):
    with console.status(
        f"[bold green] Searching for {query}...", spinner=random_spinner()
    ) as status:
        jobs = await EthioJobs().search(query)
        if not jobs:
            console.log("[bold yellow]No jobs found")
            return
        console.log(f"[bold green]Found {len(jobs)} jobs")
        status.stop()
        ans = await ask(
            message="Select a job",
            choice=[Choice(job.title, value=job.job_id) for job in jobs],
        )
        console.log(ans)
        job = await EthioJobs().get_job(ans)
        await JobView(job).run_async()


async def get_government_jobs():
    with console.status(
        f"[bold green] Searching for government jobs...", spinner=random_spinner()
    ) as status:
        jobs = await EthioJobs().get_gov_jobs()
        if not jobs:
            console.log("[bold yellow]No jobs found")
            return
        console.log(f"[bold green]Found {len(jobs)} jobs")
        status.stop()
        ans = await ask(
            message="Select a job",
            choice=[Choice(job.company, value=job.job) for job in jobs],
        )
        console.log(ans)
        # job = await EthioJobs().get_job(ans)
        # await JobView(job).run_async()


async def get_news(page: int) -> None:
    with console.status(
        f"[bold green] Getting latest news...", spinner=random_spinner()
    ) as status:
        voa = VOAAmharic()
        news = await voa.get_world_wide_news(page)
        if not news:
            console.log("[bold yellow]No news found")
            return
        console.log(f"[bold green]Found {len(news)} news")
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
        console.log(ans)
        news = await voa.get(ans)
        await NewsView(news).run_async()


async def search_news(query: str, page: int = 1, limit: int = 10) -> None:
    with console.status(
        f"[bold green] Searching for {query}...", spinner=random_spinner()
    ) as status:
        voa = VOAAmharic()
        news = await voa.search(query, page, limit)
        if not news:
            console.log("[bold yellow]No news found")
            return
        console.log(f"[bold green]Found {len(news)} news")
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
        console.log(ans)
        news = await voa.get(ans)
        await NewsView(news).run_async()


if __name__ == "__main__":
    import argparse
    import asyncio

    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", "-j", action="store_true")
    parser.add_argument("--search", "-s", help="Search for a job.")
    parser.add_argument("--gov", "-g", action="store_true", help="Get government jobs.")

    parser.add_argument("--news", "-n", action="store_true")
    parser.add_argument("--page", "-p", type=int, default=0, help="Page number")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Limit number")

    args = parser.parse_args()
    if args.job:
        if args.search:
            print(args.search)
            loop.run_until_complete(search_for_job(args.search))
        elif args.gov:
            loop.run_until_complete(search_for_job("government"))

    elif args.news:
        if args.page:
            loop.run_until_complete(get_news(args.page))
        elif args.search:
            loop.run_until_complete(search_news(args.search, args.page, args.limit))

        loop.run_until_complete(get_news(0))
