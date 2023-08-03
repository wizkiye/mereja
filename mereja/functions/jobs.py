from pyethiojobs import EthioJobs
from questionary import Choice
from rich.status import Status

from mereja.ui import JobView
from mereja.utils import ask, with_live


@with_live("Searching for {query}...")
async def search_for_job(query: str, status: Status) -> None:
    jobs = await EthioJobs().search(query)
    if not jobs:
        status.console.print("[bold yellow]No jobs found")
        return
    status.console.print(f"[bold green]Found {len(jobs)} jobs")
    status.stop()
    ans = await ask(
        message="Select a job",
        choice=[Choice(job.title, value=job.job_id) for job in jobs],
    )
    if not ans:
        return
    job = await EthioJobs().get_job(ans)
    await JobView(job).run_async()


@with_live("Searching for government jobs...")
async def get_government_jobs(status: Status):
    jobs = await EthioJobs().get_gov_jobs()
    if not jobs:
        status.console.print("[bold yellow]No jobs found")
        return
    status.console.print(f"[bold green]Found {len(jobs)} jobs")
    status.stop()
    ans = await ask(
        message="Select a job",
        choice=[Choice(job.company, value=job.job) for job in jobs],
    )
    if not ans:
        return
    job = await EthioJobs().get_job(ans)
    await JobView(job).run_async()


@with_live("Searching for latest jobs...")
async def get_latest_jobs(status: Status):
    print("Getting latest jobs...")
    jobs = await EthioJobs().get_latest_jobs()
    if not jobs:
        status.console.print("[bold yellow]No jobs found")
        return
    status.console.print(f"[bold green]Found {len(jobs)} jobs")
    status.stop()
    ans = await ask(
        message="Select a job",
        choice=[Choice(job.title, value=job.job_id) for job in jobs],
    )
    if not ans:
        return
    job = await EthioJobs().get_job(ans)
    await JobView(job).run_async()
