import inspect
from pathlib import Path
from rich.scope import render_scope
from rich.panel import Panel
from rich.table import Table
from rich.highlighter import ReprHighlighter
from rich.text import Text
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich import box

from myterial import indigo, orange

from deboard import _locals


class Locals:
    source = ''

    def to_table(self, scope):
        highlighter = ReprHighlighter()
        items_table = Table.grid(padding=(0, 1), expand=False)
        items_table.add_column(justify="right")

        def sort_items(item):
            """Sort special variables first, then alphabetically."""
            key, _ = item
            return (not key.startswith("__"), key.lower())

        items = sorted(scope.items(), key=sort_items)
        for key, value in items:
            if key.startswith("__"):
                continue
            key_text = Text.assemble(
                (key, "scope.key"),
                (" =", "scope.equals"),
            )
            items_table.add_row(
                key_text,
                Pretty(
                    value,
                    highlighter=highlighter,
                    indent_guides=True,
                    max_length=30,
                    max_string=30,
                ),
            )
        return items_table

    def get_frame(self):
        frames = _locals.get_clean_frames()

        if not frames:
            frame = self.source
        else:
            frame = frames[1]
            self.source = frame
        return frame

    def __rich_console__(self, console, measurement):
        frame = self.get_frame()
        yield Panel(self.to_table(frame.frame.f_locals), title=f'[bold {orange}]{Path(frame.filename).name}: LOCALS', style=f'bold {orange}', border_style=indigo)


class LocalsCode(Locals):
    def __init__(self):
        super(LocalsCode, self).__init__()

    def __rich_console__(self, console, measurement):
        frame = self.get_frame()
        code = Syntax.from_path(frame.filename, 
            line_numbers=True, line_range=(frame.lineno-6, frame.lineno+25),
            highlight_lines=[frame.lineno], indent_guides=True
            )

        yield Panel(code, box=box.SIMPLE, title=Path(frame.filename).name, style=f'bold {orange}')
