"""
A Factory pattern example using abc (Abstract Base Classes) module.
"""

import csv
import pathlib
import argparse
from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def open_file(self, file_path: pathlib.Path):
        """Opens a file from the specific path"""


class CsvReader(Reader):
    def open_file(self, file_path: pathlib.Path):
        """Opens a csv file and prints the contents"""
        with open(file_path) as file_obj:
            for row in csv.DictReader(file_obj):
                print(row)


class TxtReader(Reader):
    def open_file(self, file_path: pathlib.Path):
        """Opens a txt file and prints the contents"""
        with open(file_path) as file_obj:
            content = file_obj.read()
            print(content)


class ReaderFactory(ABC):
    @abstractmethod
    def get_reader(self) -> Reader:
        """Returns a new reader"""


class CsvReaderFactory(ReaderFactory):
    def get_reader(self) -> Reader:
        return CsvReader()


class TxtReaderFactory(ReaderFactory):
    def get_reader(self) -> Reader:
        return TxtReader()


FACTORIES = {"csv": CsvReaderFactory, "txt": TxtReaderFactory}


def parse_args() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="File path")
    args = parser.parse_args()
    return pathlib.Path(args.file_path)


def get_file_extension(file_path) -> str:
    return file_path.suffix.replace(".", "")


def get_factory(file_path: pathlib.Path) -> ReaderFactory:
    try:
        file_extension = get_file_extension(file_path)
        reader_factory_class = FACTORIES[file_extension]
        reader_factory = reader_factory_class()
    except KeyError:
        raise RuntimeError(f"No reader for the extension: {file_extension}. Aborting.")
    return reader_factory


def main(fac: ReaderFactory, file_path: pathlib.Path):
    reader = fac.get_reader()
    reader.open_file(file_path)


if __name__ == "__main__":
    file_path = parse_args()
    factory = get_factory(file_path)
    main(factory, file_path)
