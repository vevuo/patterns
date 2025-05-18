"""
A Factory pattern example using protocol, decorators and dataclasses.
"""

import csv
import pathlib
import argparse
from dataclasses import dataclass
from typing import Type, Protocol, Dict


class Reader(Protocol):
    def open_file(self, file_path: pathlib.Path) -> None: ...


FACTORIES: Dict[str, Type[Reader]] = {}


def register_reader(file_extension: str):
    def decorator(cls: Type[Reader]):
        FACTORIES[file_extension] = cls
        return cls

    return decorator


@register_reader("csv")
@dataclass
class CsvReader:
    def open_file(self, file_path: pathlib.Path) -> None:
        """Opens a CSV file and prints the contents."""
        try:
            with open(file_path) as file_obj:
                for row in csv.DictReader(file_obj):
                    print(row)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")


@register_reader("txt")
@dataclass
class TxtReader:
    def open_file(self, file_path: pathlib.Path) -> None:
        """Opens a text file and prints the contents."""
        try:
            with open(file_path) as file_obj:
                content = file_obj.read()
                print(content)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")


def parse_args() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="File path")
    args = parser.parse_args()
    return pathlib.Path(args.file_path)


def get_file_extension(file_path: pathlib.Path) -> str:
    return file_path.suffix.replace(".", "")


def get_reader(file_path: pathlib.Path) -> Reader:
    try:
        file_extension = get_file_extension(file_path)
        reader_class = FACTORIES[file_extension]
    except KeyError:
        raise RuntimeError(f"No reader for the extension: {file_extension}. Aborting.")
    return reader_class()  # Laiska instanssiluonti


def main(reader: Reader, file_path: pathlib.Path) -> None:
    reader.open_file(file_path)


if __name__ == "__main__":
    file_path = parse_args()
    reader = get_reader(file_path)
    main(reader, file_path)
