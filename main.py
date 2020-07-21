from src.notion.repository import NotionRepository
import os
import sys

from src.config.notion_config import NotionConfig
from src.notion.service import NotionService
from src.downloader.service import DownloaderService


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expecting a URL as a single argument")

    notion_url = sys.argv[1]

    config = NotionConfig(env=os.environ)
    notion_repo = NotionRepository()
    notion_service = NotionService(
        notion_cookie_token=config.token_v2, notion_repo=notion_repo
    )
    exported = notion_service.get_exported_url(notion_url)
    print(exported)

    download_service = DownloaderService()
    download_service.download_file(exported, download_path="./tmp")


if __name__ == "__main__":
    main()
