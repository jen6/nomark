from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


class DownloadInfo:
    base_path: Path
    images: List[Path] = []
    markdwons: List[Path] = []

    def __init__(self, base_path_str: str, filelist: List[str]):
        self.base_path = Path(base_path_str)

        for filename in filelist:
            file_path = Path(filename)
            print(file_path, file_path.suffix)
            if file_path.suffix in [".jpg", ".png"]:
                self.images.append(file_path)
                print(self.images)
            elif ".md" in file_path.suffix:
                self.markdwons.append(file_path)
                print(self.markdwons)
