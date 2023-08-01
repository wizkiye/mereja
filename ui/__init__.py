# encoding: utf-8

import html as h
import re

from markdownify import markdownify as md
from pyEthioNews.providers.voa import VoaNewsDetail
from pyethiojobs.types import JobDetails
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import MarkdownViewer, Footer

from ui.widgets import Header


def html_parser(html: str) -> str:
    """Parse HTML to Markdown."""
    html = h.unescape(html)
    html = re.sub(r"(\s.{,30}\:)", r"<br><br><strong>⚜️ \1</strong><br>", html)
    # html = re.sub(r"\s(\w)", "<br>🔶 \1", html)

    return md(html)


class JobView(App):
    def __init__(self, job: JobDetails = None):
        self.job = job
        super().__init__()

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl-s", "save_to_pdf", "Save"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, title=self.title)
        yield MarkdownViewer(f"# {self.job.title}" + html_parser(self.job.description))
        yield Footer()

    def save_to_pdf(self):
        """Save the current document."""
        f"# {self.job.title}"
        md(self.job.description)


class NewsView(App):
    def __init__(self, news: VoaNewsDetail = None):
        self.news = news
        super().__init__()

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield MarkdownViewer(
            f"# {self.news.title}\n![image info]({self.news.image})"
            + md(self.news.html),
            show_table_of_contents=False,
        )
        yield Footer()
