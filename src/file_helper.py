import os
from config import VAULT_NAME, VAULT_DIRECTORY, OPEN_WITH_DEFAULT_EDITOR

OBSIDIAN_URL = rf"obsidian://open?vault={VAULT_NAME}&file"


def load_files() -> list:
    return [f for f in os.listdir(VAULT_DIRECTORY) if f.endswith(".md")]  # TODO: nested directories


def parse_file(filename: str) -> tuple:
    path = rf"{VAULT_DIRECTORY}\{filename}"
    title = description = ""

    with open(path, "r") as f:
        for line in f.readlines():
            if "#" in line and title == "":
                title = line.replace("# ", "").replace("\n", "")
            elif "##" in line:
                description = line.replace("## ", "").replace("\n", "")
                break

    return title, description


def open_file(filename: str):  # TODO: cross-platform
    if OPEN_WITH_DEFAULT_EDITOR:
        path = rf"{VAULT_DIRECTORY}\{filename}"
        os.startfile(path)
    else:
        url = f"{OBSIDIAN_URL}={filename.replace('.md', '')}"
        os.startfile(url)
