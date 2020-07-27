from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


class DownloadInfo:
    download_files: List[Path]
    representative_file: Optional[Path]

    def __init__(self, base_path_str: str, filelist: List[str]):
        self.download_files = []
        self.representative_file = None
        base_path = Path(base_path_str)

        for filename in filelist:
            file_path = base_path.joinpath(Path(filename))
            self.download_files.append(file_path)
            if ".md" in filename and self.representative_file is None:
                self.representative_file = file_path
