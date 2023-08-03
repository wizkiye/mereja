from markdownify import markdownify as md
from pyEthioNews.providers.voa import VoaNewsDetail
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import MarkdownViewer, Footer

from mereja.ui.widgets import Header


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
