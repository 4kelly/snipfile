import os
from pathlib import Path

from snipfile._parser import snip


def snipfiles(input_dir: str, output_dir: str, pattern: str):
    for path_obj in Path(input_dir).rglob(pattern):
        # * patterns will match directories as well.
        if path_obj.is_file():
            out_file = Path(output_dir, *path_obj.parts)
            os.makedirs(out_file.parent, exist_ok=True)

            f = open(path_obj, "r")
            o = open(out_file, "w")

            snip(f, o)

            f.close()
            o.close()
