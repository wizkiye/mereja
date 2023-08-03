from datetime import datetime

import emoji
from rich.text import Text
from textual import events
from textual.app import RenderResult
from textual.events import Mount
from textual.reactive import Reactive
from textual.widget import Widget


class HeaderIcon(Widget):
    def __init__(self, icon: str = emoji.emojize(":memo:")) -> None:
        super().__init__()
        self.icon = icon

    DEFAULT_CSS = """
    HeaderIcon {
        dock: left;
        padding: 0 1;
        width: 8;
        content-align: left middle;
    }
    """

    def render(self) -> RenderResult:
        return self.icon


class HeaderClockSpace(Widget):
    DEFAULT_CSS = """
    HeaderClockSpace {
        dock: right;
        width: 10;
        padding: 0 1;
    }
    """

    def render(self) -> RenderResult:
        return ""


class HeaderClock(HeaderClockSpace):
    DEFAULT_CSS = """
    HeaderClock {
        background: $foreground-darken-1 5%;
        color: $text;
        text-opacity: 85%;
        content-align: center middle;
    }
    """

    def _on_mount(self, _: Mount) -> None:
        self.set_interval(1, callback=self.refresh, name=f"update header clock")

    def render(self) -> RenderResult:
        return Text(datetime.now().time().strftime("%X"))


class HeaderTitle(Widget):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    DEFAULT_CSS = """
    HeaderTitle {
        content-align: center middle;
        width: 100%;
    }
    """

    def render(self) -> RenderResult:
        text = Text(self.text, no_wrap=True, overflow="ellipsis", style="bold blue")
        return text


class Header(Widget):
    DEFAULT_CSS = """
    Header {
        dock: top;
        width: 100%;
        background: $foreground 5%;
        color: $text;
        height: 1;
    }
    Header.-tall {
        height: 3;
    }
    """

    DEFAULT_CLASSES = ""

    tall: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        show_clock: bool = False,
        title: str = "</> with ❤️ by @wizkiye",
        *,
        classes: str | None = None,
        id: str | None = None,
    ):
        super().__init__(classes=classes, id=id)
        self._show_clock = show_clock
        self.title = title

    def compose(self):
        yield HeaderIcon()
        yield HeaderTitle(self.title)
        yield HeaderClock() if self._show_clock else HeaderClockSpace()

    def watch_tall(self, tall: bool) -> None:
        self.set_class(tall, "-tall")

    def _on_click(self, event: events.Click):
        self.toggle_class("-tall")
