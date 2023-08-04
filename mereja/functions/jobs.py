import json

from pyethiojobs import EthioJobs
from questionary import Choice
from rich.status import Status

from mereja.ui import JobView
from mereja.utils import ask, with_live, save_file, get_path


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


@with_live("Searching for latest jobs...")
async def export_latest_jobs(path: str, status: Status, limit: int):
    jobs = await EthioJobs().get_latest_jobs()
    if not jobs:
        status.console.print("[bold yellow]No jobs found")
        return
    status.console.print(f"[bold green]Found {len(jobs)} jobs")
    jobs = jobs[:limit] if limit else jobs
    dict_jobs = []
    path = get_path(path, "latest_jobs")
    status.update(f"[bold green]Exporting {len(jobs)} jobs to {path}")
    for job in jobs:
        jop_de = await job.get_details()
        dict_jobs.append(jop_de.dict())
    save_file(path, json.dumps(dict_jobs, indent=4))
    status.console.print(
        f"[bold green]Successfully exported {len(dict_jobs)} jobs to {path}"
    )
