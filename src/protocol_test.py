from typing import Protocol


class Readable(Protocol):
    def read(self) -> str: ...


def read_content(reader: Readable):
    reader.read()


class DataReader:
    def __init__(self, data: str) -> None:
        self.data = data

    def read(self):
        print(self.data)


def main():
    data = "Hello World!"
    data_reader = DataReader(data)
    read_content(data_reader)


if __name__ == "__main__":
    main()
