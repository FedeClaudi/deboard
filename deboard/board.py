from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from loguru import logger
import sys

from deboard.trace import Trace
from deboard.locals import Locals, LocalsCode
from deboard.processes import Processes

class Board:
    def __init__(self):
        self.layout = self.make_layout()

    def make_layout(self):
        layout = Layout()

        layout.split(
            Layout(Trace(), name='trace'),
            Layout(ratio=2, name='main'),
            direction='horizontal'
        )

        layout['main'].split(
            Layout(name='sysinfo'),
            Layout(name='locals')
        )

        layout['sysinfo'].split(
            Layout(ratio=1.2),
            Layout(Processes()),
            direction='horizontal'
        )

        layout['locals'].split(
            Layout(Locals(), ratio=1.2),
            Layout(LocalsCode()),
            direction='horizontal'
        )
        return layout

    def __enter__(self):
        logger.debug('Board starting - live')
        self.live = Live(self.layout, refresh_per_second=10)
        try:
            self.live.start(refresh=True)
        except Exception as e:
            logger.debug(f'Board live failed with exception: {e}')
            raise (e)
        return self

    def __exit__(self, e_typ, e_val, trcbak):
        logger.debug(f'Board stopped with args: {e_typ, e_val, trcbak}')
        self.live.stop()