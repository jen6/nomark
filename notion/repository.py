from constants.const import NOTION_TOKEN_COOKIE_STR
import requests
from notion.model import ExportedURLPayload
from typing import Dict, Optional


class NotionRepository:
    def __init__(
        self, requests_session: Optional[requests.Session] = None, timeout: int = 10
    ):
        self._session = requests_session or requests.session()
        self._timeout = timeout

    def enqueue_export_task(self, token: str, payload: ExportedURLPayload):
        resp = self._session.post(
            "https://www.notion.so/api/v3/enqueueTask",
            cookies={NOTION_TOKEN_COOKIE_STR: token,},
            json=payload.to_dict(),
            timeout=self._timeout,
        )
        task_id = resp.json().get("taskId", None)
        if not task_id:
            raise Exception(f"Could not get the scheduled task id: {resp}")
        return task_id

    def get_export_task(self, token: str, task_id: str):
        payload = {
            "taskIds": [task_id],
        }
        resp = self._session.post(
            "https://www.notion.so/api/v3/getTasks",
            cookies={NOTION_TOKEN_COOKIE_STR: token,},
            json=payload,
            timeout=self._timeout,
        )
        result = resp.json()["results"][0]
        return (result["state"], result.get("status", None))
