import re
import shutil
from pathlib import Path


def clean_title(title: str) -> str:
    # Remove anything inside () or []
    cleaned = re.sub(r"[\(\[].*?[\)\]]", "", title)
    # Collapse multiple spaces and strip leading/trailing
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def move_file(file_path, destination_folder):
    file_path = Path(file_path)
    destination_folder = Path(destination_folder)

    # Make sure the destination folder exists
    destination_folder.mkdir(parents=True, exist_ok=True)

    # Construct the destination path
    destination_path = destination_folder / file_path.name

    # Move the file
    shutil.move(str(file_path), str(destination_path))
