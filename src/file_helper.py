import os
import urllib.parse
from config import VAULT_DIRECTORY, OPEN_WITH_DEFAULT_EDITOR
from typing import TextIO

OBSIDIAN_URL = rf"obsidian://open?path="


def load_files() -> list:
    paths = []

    for path, _, files in os.walk(VAULT_DIRECTORY):
        for name in files:
            file_path = os.path.join(path, name)
            if file_path.endswith(".md"):
                paths.append(file_path)

    return paths


def parse_file(path: str) -> tuple:
    with open(path, "r") as f:
        return _do_file_parse_strategy(f)


def _do_file_parse_strategy(f: TextIO) -> tuple:
    title = description = ""

    for line in f:
        if line.startswith("# "):
            title = line.replace("# ", "").replace("\n", "")
            description = next(f).replace("\n", "")

    return title, description


def open_file(path: str):  # TODO: cross-platform
    if OPEN_WITH_DEFAULT_EDITOR:
        os.startfile(path)
    else:
        encoded_path = urllib.parse.quote(path)
        os.startfile(OBSIDIAN_URL + encoded_path)
