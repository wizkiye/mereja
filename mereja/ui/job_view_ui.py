from markdownify import markdownify as md
from pyethiojobs.types import JobDetails
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import MarkdownViewer, Footer, Input, Button

from mereja.ui.widgets import Header


class FindScreen(ModalScreen):
    DEFAULT_CSS = """
    FindScreen {
        align: center middle;
    }

    FindScreen > Container {
        width: auto;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }

    FindScreen > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }

    FindScreen > Container > Horizontal {
        width: auto;
        height: auto;
    }

    FindScreen > Container > Horizontal > Button {
        margin: 2 4;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Input("Find: ", id="find"),
            Horizontal(
                Button("Find", variant="primary", id="find_button"),
                Button("Cancel", variant="primary", id="cancel"),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        elif event.button.id == "cancel":
            self.app.pop_screen()
        else:
            self.dismiss(self.query_one(Input).value)

    def on_input_submitted(self) -> None:
        self.dismiss(self.query_one(Input).value)


class JobView(App):
    def __init__(self, job: JobDetails = None):
        self.job = job
        super().__init__()

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding(
            action="open_link",
            key="o",
            description="Open link in browser",
        ),
        Binding(
            action="find",
            key="f",
            description="Find",
        ),
        # Binding(
        #     action="save",
        #     key="s",
        #     description="Save",
        # ),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, title=self.job.title, id="header")
        yield MarkdownViewer(
            md(self.job.description),
            show_table_of_contents=False,
            id="markdown_viewer",
        )
        yield Footer()

    def action_open_link(self):
        import webbrowser

        webbrowser.open(self.job.link)

    def action_find(self):
        self.push_screen(FindScreen(), callback=self.find_callback)

    # def action_save(self):
    #     pdfkit.from_url(self.job.print_link, "out.pdf")
    #     subprocess.Popen(["out.pdf"])
