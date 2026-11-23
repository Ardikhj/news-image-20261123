#!/usr/bin/env python3
"""Entrypoint for news-image-20261123.

The picture is pre-rendered at build time (see render.py). This program
only copies the committed entry.png into $MAKEFUN_OUTPUT_DIR, using the
standard library only, so it runs in the grader's bare Python image
(no Pillow, no network, read-only repo, 60 s wall).
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(SOURCE):
        fail("entry.png is missing from the repository")
    with open(SOURCE, "rb") as handle:
        payload = handle.read()
    if len(payload) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB cap" % len(payload))
    if payload[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG signature")
    digest = hashlib.sha256(payload).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    with open(target, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != digest:
        fail("copied entry.png does not match the committed bytes")
    print("wrote %s (%d bytes, sha256 %s)" % (target, len(copied), digest))


if __name__ == "__main__":
    main()
