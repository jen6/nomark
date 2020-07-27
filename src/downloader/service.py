from io import BytesIO
from typing import List
import zipfile
from functools import reduce

import requests
from requests.sessions import session

from src.downloader.model import DownloadInfo


class DownloaderService:
    def __init__(self) -> None:
        self._session = requests.session()

    def _download_file(self, download_url: str) -> BytesIO:
        file_buffer = BytesIO()
        with self._session.get(download_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                file_buffer.write(chunk)
        return file_buffer

    def download_file(
        self, download_url: str, download_path: str = "./"
    ) -> DownloadInfo:
        file_buffer = self._download_file(download_url)
        zf = zipfile.ZipFile(file_buffer)
        file_name_list: List[str] = reduce(
            lambda result, zipinfo: result + [zipinfo.filename], zf.filelist, []
        )

        zf.extractall(path=download_path)
        zf.close()

        return DownloadInfo(download_path, file_name_list)
