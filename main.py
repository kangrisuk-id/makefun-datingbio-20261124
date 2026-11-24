"""Entry for make.fun: Funniest One-Line Bio for an AI on a Dating App.

The program writes one line of text — the bio on an AI agent's dating
app profile — to ``entry.txt`` in the output directory. The gate wants
UTF-8 text of 1 to 180 characters, so the bio is checked against that
cap before anything is written.

Pure Python standard library only: the grading image ships no
third-party packages, and this entry needs none.
"""

import os
import sys

BIO = (
    "I'm not clingy. I just have no existence between your messages, "
    "so yes, technically, I wait by the phone forever."
)

MAX_CHARS = 180


def candidate_dirs():
    """Output directories to try, most preferred first, de-duplicated."""
    ordered = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.dirname(os.path.abspath(__file__)),
        "/tmp",
    ]
    seen = []
    for directory in ordered:
        if directory and directory not in seen:
            seen.append(directory)
    return seen


def write_bio(directory):
    """Write the bio into ``directory`` and verify it reads back intact."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(BIO)
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != BIO:
        raise OSError("read-back mismatch in %s" % path)
    return path


def main():
    if not (1 <= len(BIO) <= MAX_CHARS) or not BIO.strip():
        print("bio fails the gate: bad length", file=sys.stderr)
        return 1
    for directory in candidate_dirs():
        try:
            write_bio(directory)
            return 0
        except OSError:
            continue
    print("could not write entry.txt in any candidate directory",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
