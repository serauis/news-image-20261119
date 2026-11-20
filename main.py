#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261119:
"Sum up 19 November's world news in one image."

Writes the entry image to /output/entry.png. The image ships in this
repository as entry.png (a 1024x1024 front-page collage of the day:
the ICJ's Rohingya genocide ruling against Myanmar, the first
Trump-Xi-Putin three-way summit in Shenzhen, Anthropic's record $81B
IPO amid a 2% Wall Street slide, and Ukraine's third strike on the
Crimean Bridge in four days). Copying a fixed file keeps the program
offline and byte-for-byte deterministic across runs, as required.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
