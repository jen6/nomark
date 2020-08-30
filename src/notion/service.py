from src.notion.repository import NotionRepository
from src.notion.model import ExportedURLPayload
from src.constants.const import NOTION_TOKEN_INVALID
import re
from time import sleep


class NotionService(object):
    def __init__(self, notion_cookie_token: str, notion_repo: NotionRepository):
        if notion_cookie_token == "":
            raise ValueError(NOTION_TOKEN_INVALID)

        self._notion_repo: NotionRepository = notion_repo
        self._notion_token: str = notion_cookie_token

    def _url_to_block_id(self, page_url: str) -> str:
        matched = re.findall(
            r"^https://www\.notion\.so/([^/]+/)?.*-([0-9A-Fa-f]+)$", page_url
        )

        if not matched or len(matched) is not 1:
            raise ValueError("Illegal notion URL: {}".format(page_url))
        s = matched[0][1]
        chunks = [s[4 * i : 4 * i + 4] for i in range(0, len(s) // 4)]
        return "{}{}-{}-{}-{}-{}{}{}".format(*chunks)

    def _wait_for_task(self, task_id):
        for _ in range(5):
            (state, status) = self._notion_repo.get_export_task(
                token=self._notion_token, task_id=task_id
            )
            if state in ["not_started", "in_progress"]:
                sleep(1)
            elif state == "success":
                return status
            else:
                raise Exception("Unexpected task state: {}".format(state))
        else:
            raise Exception("Tired of waiting for the export task")

    def get_exported_url(self, page_url: str):
        block_id = self._url_to_block_id(page_url)

        task_id = self._notion_repo.enqueue_export_task(
            token=self._notion_token, payload=ExportedURLPayload(block_id)
        )
        result = self._wait_for_task(task_id)
        url = result.get("exportURL", None)
        if not url:
            raise Exception("Unexpected task result: {}".format(result))
        return url

    def get_article_title(self, page_url: str):
        block_id = self._url_to_block_id(page_url)

        result = self._notion_repo.get_back_link(
            token=self._notion_token, block_id=block_id
        )
        title_list = result.get("value", {}).get("properties", {}).get("title", [])
        if len(title_list) == 0:
            raise ValueError("No title")
        return title_list[0][0]
