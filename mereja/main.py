import argparse
import asyncio
import sys

from mereja.functions import forex, telebirr, market, news, jobs


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
            loop.run_until_complete(news.get_news(args.page))

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
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit()


def main():
    parser = argparse.ArgumentParser()

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
