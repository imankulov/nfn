#!/usr/bin/env python
"""Generate the next filename."""
import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class Arguments:
    dir: str
    name: str
    touch: bool


def get_arguments() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dir",
        help=(
            "Directory to create a file. If not provided, "
            "the current directory is used."
        ),
        default=os.getcwd(),
    )
    parser.add_argument(
        "-t", "--touch", help="Touch the newly created file.", action="store_true"
    )
    parser.add_argument("name", help="Filename.")
    args = parser.parse_args()
    return Arguments(dir=args.dir, name=args.name, touch=args.touch)


def nfn(arguments: Arguments) -> str:
    """Create a new filename.

    Make up to 10 attempts to create a new file. The file creation may fail due to race
    conditions if the "touch" flag is set.
    """
    attempts = 100
    for _ in range(attempts):
        try:
            return try_nfn(arguments)
        except FileExistsError:
            pass
    raise ValueError(f"Could not create a new file after {attempts} attempts.")


def try_nfn(arguments: Arguments) -> str:
    """Create a new filename."""

    # Current directory.
    dir_path = Path(arguments.dir)
    if not dir_path.is_dir():
        raise ValueError(f"{dir_path} is not a directory.")

    prefix, suffix, digits = parse_filename_template(arguments.name)
    max_number = find_max_number(dir_path, prefix, suffix)
    next_number = format_next(max_number, digits)
    new_filename = f"{prefix}{next_number}{suffix}"

    # Create a new file if asked
    if arguments.touch:
        new_file = dir_path / new_filename
        new_file.touch(exist_ok=False)

    return new_filename


def parse_filename_template(filename: str) -> Tuple[str, str, int]:
    """Parse filename template.

    Return the tuple with prefix, suffix, and the number of digits in the output file.
    """
    if "/" in filename:
        raise ValueError("Filename cannot contain '/'.")

    try:
        prefix, suffix = re.split("N+", filename, maxsplit=1)
    except ValueError:
        raise ValueError(
            "Filename must contain at least one N as a placeholder for numbers."
        )
    digits = len(filename) - len(prefix) - len(suffix)
    return prefix, suffix, digits


def find_max_number(dir_path: Path, prefix: str, suffix: str) -> int:
    """Find the largest number in the directory.

    Explore other files and directories in the dir_path to find the largest current
    number.
    """
    max_number = 0
    for filename in dir_path.glob(f"{prefix}*{suffix}"):
        match = filename.name[len(prefix) : -len(suffix)]
        try:
            int_match = int(match)
        except ValueError:
            continue
        if int_match > max_number:
            max_number = int_match
    return max_number


def format_next(max_number: int, length) -> str:
    """Return the formatted version of the next number."""
    return f"{max_number + 1:0{length}}"


if __name__ == "__main__":
    args = get_arguments()
    try:
        print(nfn(args))
    except ValueError as error:
        raise SystemExit(f"Error: {error}")
