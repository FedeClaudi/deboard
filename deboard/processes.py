import psutil
from rich.table import Table
from rich import box
from rich.panel import Panel

from myterial import green, green_light, orange

KEYS = 'pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads'
KEYS_FMT = 'pid', 'name', 'CPU %', 'MEM %', '# threads'

def fmt(obj):
    if isinstance(obj, str):
        return obj
    else:
        return str(round(obj, 2))

def sortkey(item):
    return item['cpu_percent'] if item['cpu_percent'] is not None else 0

class Processes:

    def __rich_console__(self, console, measurement):
        # make table
        table = Table(box=box.SIMPLE)
        for key in KEYS_FMT:
            table.add_column(key, header_style=f'bold {green}')

        # sort processes by CPU
        processes = [proc.as_dict() for proc in psutil.process_iter(['pid', 'name'])]
        processes = sorted(processes, key=sortkey, reverse=True,)

        # add to table
        for proc in processes:
            if proc['cpu_percent'] is None:
                continue
            if proc['cpu_percent'] < 1:
                continue
            
            table.add_row(*[fmt(proc[k]) for k in KEYS], style=green_light)

        yield Panel(table, title=f'[b {orange}]Processes', style='green', box=box.SIMPLE)