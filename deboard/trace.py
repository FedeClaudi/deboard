import traceback
from rich.tree import Tree
from pathlib import Path
from rich.panel import Panel

from myterial import orange, pink_light, pink, grey, blue_light, teal_light, green_light, orange_light

from deboard import _locals

class TraceItem:
    def __init__(self, trace_signature):
        (top, codeline, _) = trace_signature.split("\n")

        self.path = Path(top.split('", line')[0].split('File "')[1])
        self.package = self.path.parent.name
        self.fname = self.path.name
        self.lineno = int(top.split('", line ')[1].split(', in ')[0])
        self.func = top.split(', in ')[-1]


class Trace:
    def label_in_tree(self, label, tree=None):
        tree = tree or self.tree
        return label in [n.label for n in tree.children]

    def get_with_label(self, label, tree=None):
        tree = tree or self.tree
        return [n for n in tree.children if n.label==label]

    def __rich_console__(self, console, measure):
        frame = _locals.get_clean_frames()[1].frame

        self.tree = Tree(f'[{pink}]Call stack', guide_style=pink_light)

        for trace_signature in traceback.format_stack(frame)[::-1]:
            item = TraceItem(trace_signature)

            # get package node
            label = f'[b {orange}]{item.package}'
            if self.label_in_tree(label):
                node = self.get_with_label(label)[0]
            else:
                node = self.tree.add(label, guide_style=orange_light)

            # get file node
            file_label = f'[{green_light}]{item.fname}'
            if self.label_in_tree(file_label, tree=node):
                node = self.get_with_label(file_label, tree=node)[0]
            else:
                node = node.add(file_label, guide_style=teal_light)

            # add to noe
            node.add(f'[b {blue_light}]{item.func} [{grey}](line: {item.lineno})[/{grey}]')



        yield Panel(self.tree)
