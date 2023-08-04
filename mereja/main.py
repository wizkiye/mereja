import argparse
import asyncio
import sys

import questionary

from mereja import constants
from mereja.functions import forex, telebirr, market, news, jobs
from mereja.utils import awaitable

questions = [
    {
        "type": "select",
        "name": "answer",
        "message": "What do you want to do?",
        "choices": [
            "📈 Forex",
            "📝 News",
            "💼 Jobs",
            "🛍 Marketplace",
            "💳 Telebirr",
            "🛑 Exit",
        ],
    },
    {
        "type": "select",
        "name": "forex_choice",
        "message": "What do you want to do?",
        "choices": [
            "📈 Get forex",
            "📈 🚦 Get forex Live",
            "📂 Export forex data",
            "🔙 Back",
        ],
        "qmark": "📈",
        "when": lambda answers: answers.get("answer") == "📈 Forex",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with news?",
        "choices": ["📝 Get latest news", "🔍 Search for news", "🔙 Back"],
        "qmark": "📝",
        "when": lambda answers: answers.get("answer") == "📝 News",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with jobs?",
        "choices": ["Get latest jobs", "🔍 Search for jobs", "🔙 Back"],
        "qmark": "💼",
        "when": lambda answers: answers.get("answer") == "💼 Jobs",
    },
    {
        "type": "select",
        "name": "choice",
        "message": "What do you want to do with marketplace?",
        "choices": ["📈 Get trending products", "🔍 Search for products", "🔙 Back"],
        "qmark": "🛍",
        "when": lambda answers: answers.get("answer") == "🛍 Marketplace",
    },
    {
        "type": "select",
        "name": "telebirr_choice",
        "message": "What do you want to do with telebirr?",
        "choices": ["💳 Transaction Details", "📂 Export transaction data", "🔙 Back"],
        "qmark": "💳",
        "when": lambda answers: answers.get("answer") == "💳 Telebirr",
    },
    {
        "type": "text",
        "name": "transaction_id",
        "message": "💳 Enter your transaction ID:",
        "when": lambda answers: answers.get("telebirr_choice")
        in ["💳 Transaction Details", "📂 Export transaction data"],
    },
    {
        "type": "confirm",
        "name": "exit",
        "message": "Are you sure you want to exit?",
        "default": True,
        "when": lambda answers: answers.get("answer") == "🛑 Exit",
    },
    {
        "type": "text",
        "name": "search",
        "message": "Enter your search query:",
        "when": lambda answers: "Search" in answers.get("choice", ""),
    },
    {
        "type": "text",
        "name": "path",
        "message": "Enter the path to save the file:",
        "when": lambda answers: answers.get("forex_choice") in ["📂 Export forex data"]
        or answers.get("telebirr_choice") in ["📂 Export transaction data"],
        "validate": lambda val: (val and val.endswith(".json"))
        or "Path must end with .json",
    },
    {
        "type": "text",
        "name": "page",
        "message": "Enter the page number:",
        "when": lambda answers: answers.get("choice")
        in [
            "Get latest jobs",
            "📝 Get latest news",
            "📈 Get trending products",
            "🔍 Search for products",
        ],
        "validate": lambda val: val.isdigit() or "Page number must be a number",
        "filter": lambda val: int(val),
        "default": "1",
    },
]


@awaitable
def show_menu():
    ans = questionary.prompt(
        questions,
        style=constants.STYLE,
        qmark="📡",
    )
    return ans


async def parse_answers(answers):
    if answers.get("answer") == "📈 Forex":
        if answers.get("forex_choice") == "📈 Get forex":
            await forex.get_forex(False)

        elif answers.get("forex_choice") == "📈 🚦 Get forex Live":
            await forex.get_forex(live=True)

        elif answers.get("forex_choice") == "📂 Export forex data":
            await forex.export_forex_data(path=answers.get("path"))

        elif answers.get("forex_choice") == "🔙 Back":
            return
    elif answers.get("answer") == "📝 News":
        if answers.get("choice") == "📝 Get latest news":
            await news.get_news(page=answers.get("page"))

        elif answers.get("choice") == "🔍 Search for news":
            await news.search_news(
                query=answers.get("search"), page=answers.get("page")
            )

        elif answers.get("choice") == "🔙 Back":
            return

    elif answers.get("answer") == "💼 Jobs":
        if answers.get("choice") == "Get latest jobs":
            await jobs.get_latest_jobs()

        elif answers.get("choice") == "🔍 Search for jobs":
            await jobs.search_for_job()

        elif answers.get("choice") == "🔙 Back":
            return
    elif answers.get("answer") == "🛍 Marketplace":
        if answers.get("choice") == "📈 Get trending products":
            await market.get_trending_products()

        elif answers.get("choice") == "🔍 Search for products":
            await market.search_for_product(
                query=answers.get("search"), page=answers.get("page")
            )

        elif answers.get("choice") == "🔙 Back":
            return

    elif answers.get("answer") == "💳 Telebirr":
        if answers.get("telebirr_choice") == "💳 Transaction Details":
            await telebirr.check_transaction(
                transaction_id=answers.get("transaction_id")
            )

        elif answers.get("telebirr_choice") == "📂 Export transaction data":
            await telebirr.export_transaction(
                path=answers.get("path"),
                transaction_id=answers.get("transaction_id"),
            )

        elif answers.get("telebirr_choice") == "🔙 Back":
            return

    elif answers.get("answer") == "🛑 Exit":
        if answers.get("exit"):
            sys.exit(0)

    return await parse_answers(answers)


async def ask_questions():
    while True:
        try:
            answers = await show_menu()
            await parse_answers(answers)
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)


def runner(args):
    loop = asyncio.get_event_loop()
    try:
        if args.job:
            if args.search:
                loop.run_until_complete(jobs.search_for_job(query=args.search))
            # elif args.gov:
            #     loop.run_until_complete(jobs.get_government_jobs())
            elif args.latest:
                if args.export:
                    loop.run_until_complete(
                        jobs.export_latest_jobs(path=args.path, limit=args.limit)
                    )
                    return
                loop.run_until_complete(jobs.get_latest_jobs())

        elif args.news:
            if args.export:
                loop.run_until_complete(
                    news.export_news(
                        path=args.path,
                        limit=args.limit,
                        page=args.page + 1 if not args.page else args.page,
                    )
                )
                return
            if args.search:
                if args.export:
                    loop.run_until_complete(
                        news.export_news(
                            query=args.search, path=args.path, limit=args.limit
                        )
                    )
                loop.run_until_complete(
                    news.search_news(
                        query=args.search, page=args.page, limit=args.limit
                    )
                )
                return
            loop.run_until_complete(news.get_news(page=args.page))

        elif args.marketplace:
            if args.trending:
                if args.export:
                    loop.run_until_complete(
                        market.export_products(path=args.path, limit=args.limit)
                    )
                    return
                loop.run_until_complete(
                    market.get_trending_products(
                        page=args.page + 1 if not args.page else args.page,
                        limit=args.limit,
                    )
                )
            if args.search:
                loop.run_until_complete(
                    market.search_for_product(
                        query=args.search,
                        page=args.page + 1 if not args.page else args.page,
                        limit=args.limit,
                    )
                )

        elif args.telebirr:
            if args.transaction:
                if args.export:
                    loop.run_until_complete(
                        telebirr.export_transaction(args.transaction, args.path)
                    )
                    return
                loop.run_until_complete(telebirr.check_transaction(args.transaction))

        elif args.forex:
            if args.export:
                loop.run_until_complete(forex.export_forex_data(args.path))
                return
            loop.run_until_complete(forex.get_forex(args.live))

        elif args.export:
            loop.run_until_complete(
                telebirr.export_transaction(args.transaction, args.path)
            )
        else:
            loop.run_until_complete(ask_questions())
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Mereja is a versatile Python application that provides both a Command-Line Interface (CLI) and a "
            "Text-based User Interface (TUI). The app allows users to access and display various data, including the "
            "latest news, jobs, forex data, trending products for marketplaces, and telebirr transaction details. "
            "Additionally, it provides a search functionality for finding jobs, news articles, and marketplace "
            "products, making it a one-stop solution for information retrieval."
        ),
    )

    # main functions
    parser.add_argument("--job", "-j", action="store_true", help="Jobs")
    parser.add_argument("--marketplace", "-m", action="store_true", help="Marketplace")
    parser.add_argument("--telebirr", "-tb", action="store_true", help="Telebirr")
    parser.add_argument("--forex", "-f", action="store_true", help="Forex")
    parser.add_argument("--news", "-n", action="store_true", help="News")

    # job args
    # parser.add_argument("--gov", "-g", action="store_true", help="Get government jobs.")
    parser.add_argument("--latest", "-lt", action="store_true", help="Get latest jobs.")

    # market args
    parser.add_argument(
        "--trending", "-t", action="store_true", help="Get trending products"
    )
    # telebirr args
    parser.add_argument(
        "--transaction", "-tx", type=str, help="Telebirr Transaction ID"
    )

    # forex args
    parser.add_argument("--live", "-lv", action="store_true", help="Watch Live forex")

    # shared args
    parser.add_argument("--page", "-p", type=int, default=0, help="Page number")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Limit number")
    parser.add_argument("--search", "-s", help="Search for a job/product/news")
    parser.add_argument("--export", "-e", action="store_true", help="Export to file")
    parser.add_argument("--path", "-pa", help="Path to export file")

    args = parser.parse_args()

    runner(args)


if __name__ == "__main__":
    main()
