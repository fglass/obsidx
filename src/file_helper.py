import os
import urllib.parse

OBSIDIAN_URI = rf"obsidian://open?path="


def load_files(directory: str) -> list:
    paths = []

    for path, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(path, name)
            if file_path.endswith(".md"):
                paths.append(file_path)

    return paths


def open_file(path: str, use_default_editor: bool):
    if use_default_editor:
        os.startfile(path)
    else:
        encoded_path = urllib.parse.quote(path)
        os.startfile(OBSIDIAN_URI + encoded_path)
