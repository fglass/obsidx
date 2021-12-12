import os
import urllib.parse
from config import VAULT_DIRECTORY, OPEN_WITH_DEFAULT_EDITOR

OBSIDIAN_URL = rf"obsidian://open?path="


def load_files() -> list:
    paths = []

    for path, _, files in os.walk(VAULT_DIRECTORY):
        for name in files:
            file_path = os.path.join(path, name)
            if file_path.endswith(".md"):
                paths.append(file_path)

    return paths


def open_file(path: str):  # TODO: cross-platform
    if OPEN_WITH_DEFAULT_EDITOR:
        os.startfile(path)
    else:
        encoded_path = urllib.parse.quote(path)
        os.startfile(OBSIDIAN_URL + encoded_path)
