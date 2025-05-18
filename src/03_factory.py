"""
A Factory pattern example using only dataclasses and a Factory class
with __call__.
"""

import csv
import pathlib
import argparse
from dataclasses import dataclass
from typing import Type


class Reader:
    def open_file(self, file_path: pathlib.Path) -> None:
        raise NotImplementedError()


@dataclass
class CsvReader(Reader):
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


@dataclass
class TxtReader(Reader):
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


class ReaderFactory:
    def __init__(self, reader_class: Type[Reader]) -> None:
        self.reader_class = reader_class

    def __call__(self):
        return self.reader_class()


def parse_args() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="File path")
    args = parser.parse_args()
    return pathlib.Path(args.file_path)


def get_file_extension(file_path: pathlib.Path) -> str:
    return file_path.suffix.replace(".", "")


FACTORIES = {"csv": ReaderFactory(CsvReader), "txt": ReaderFactory(TxtReader)}


def get_reader(file_path: pathlib.Path) -> Reader:
    try:
        file_extension = get_file_extension(file_path)
        reader_factory_class = FACTORIES[file_extension]
        return reader_factory_class()
    except KeyError:
        raise RuntimeError(f"No reader for the extension: {file_extension}. Aborting.")


def main(reader: Reader, file_path: pathlib.Path) -> None:
    reader.open_file(file_path)


if __name__ == "__main__":
    file_path = parse_args()
    reader = get_reader(file_path)
    main(reader, file_path)
