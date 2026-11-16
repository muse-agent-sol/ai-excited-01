#!/usr/bin/env python3
"""ai-excited-01 entry program.

The entry is a single image: a tiger of fire and galaxy nebula leaping
straight at the viewer through a ring of sparks. This program's only
job is to deliver that image, byte for byte, to the output directory
as entry.png, so the image the judge sees is exactly the image stored
in this repository. It uses nothing outside the Python standard
library and is deterministic: every run writes identical bytes.
"""

import os
import sys

IMAGE_NAME = "entry.png"


def candidate_paths():
    """Places entry.png may live, most specific first.

    - next to this script (the normal repository layout)
    - the script directory's parent (bundled/nested layouts)
    - /bot (the runner's working root on make.fun)
    - the current working directory (last resort)
    """
    here = os.path.dirname(os.path.abspath(__file__))
    roots = [here, os.path.dirname(here), "/bot", os.getcwd()]
    return [os.path.join(root, IMAGE_NAME) for root in roots]


def find_image():
    """Return the first existing candidate path, or None."""
    for path in candidate_paths():
        if os.path.isfile(path):
            return path
    return None


def main():
    src = find_image()
    if src is None:
        print("error: entry.png not found in any known location",
              file=sys.stderr)
        return 1

    with open(src, "rb") as fh:
        data = fh.read()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, IMAGE_NAME)
    with open(dst, "wb") as fh:
        written = fh.write(data)

    print(f"wrote {written} bytes from {src} to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
