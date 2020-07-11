from notion.repository import NotionRepository
import os
import sys

from config.notion_config import NotionConfig
from notion.service import NotionService


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


if __name__ == "__main__":
    main()
