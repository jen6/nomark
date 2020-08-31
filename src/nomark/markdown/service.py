from io import StringIO
from pathlib import Path
from typing import List
from shutil import copyfileobj


class LineFeeder:
    def read_line(self, line: str) -> str:
        pass


class MarkdownService:
    def __init__(self, line_feeders: List[LineFeeder] = None):
        self._line_feeders = line_feeders or []

    def add_line_feeder(self, line_feeder: LineFeeder):
        self._line_feeders.append(line_feeder)

    def process_file(
        self, markdown_file: Path, destination_file: Path = Path("./out.md")
    ):
        file_buffer = StringIO()
        with markdown_file.open("r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                for line_feeder in self._line_feeders:
                    line = line_feeder.read_line(line)
                file_buffer.write(line)

        with destination_file.open("w") as f:
            file_buffer.seek(0)
            copyfileobj(file_buffer, f)
