from pathlib import Path
import inspect

def _name(fpath):
    return Path(fpath).parent.name


def get_clean_frames():
    locs = inspect.currentframe()

    frames = inspect.getouterframes(locs)[::-1]

    frames = [f for f in frames 
                if 'rich' not in _name(f.filename) 
                and 'python' not in _name(f.filename)
                and 'locals.py' not in Path(f.filename).name]  

    return frames