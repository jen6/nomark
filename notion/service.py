#!/usr/bin/env python3

# Fetches an archive with markdown using Notion API
#
# Expects a Notion token in the `NOTION_TOKEN` environment variable.
# Get this token from your browser’s cookies.
#
# Usage: NOTION_TOKEN=<token> ./notion.py <page-url>
#

from notion.model import ExportedURLPayload
from typing import Dict
from constants.const import NOTION_TOKEN_COOKIE_STR, NOTION_TOKEN_INVALID
import json
import re
import requests
from time import sleep


class NotionService(object):
    _cookie: Dict[str, str]

    def __init__(self, notion_cookie_token: str):
        if notion_cookie_token == "":
            raise ValueError(NOTION_TOKEN_INVALID)

        self._cookie = {
            NOTION_TOKEN_COOKIE_STR: notion_cookie_token,
        }

    def _url_to_block_id(self, page_url: str) -> str:
        matched = re.match(r"^https://www.notion.so/[^/]+/([0-9A-Fa-f]+)$", page_url)
        if not matched or not matched.group(1):
            raise ValueError("Illegal notion URL: {}".format(page_url))
        s = matched.group(1)
        chunks = [s[4 * i : 4 * i + 4] for i in range(0, len(s) // 4)]
        return "{}{}-{}-{}-{}-{}{}{}".format(*chunks)

    def _get_task_status(self, task_id):
        payload = {
            "taskIds": [task_id],
        }
        r = requests.post(
            "https://www.notion.so/api/v3/getTasks", cookies=self._cookie, json=payload,
        )
        result = r.json()["results"][0]
        return (result["state"], result.get("status", None))

    def _wait_for_task(self, task_id):
        for _ in range(5):
            (state, status) = self._get_task_status(task_id)
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
        payload = ExportedURLPayload(block_id).to_dict()
        r = requests.post(
            "https://www.notion.so/api/v3/enqueueTask",
            cookies=self._cookie,
            json=payload,
        )
        task_id = r.json().get("taskId", None)
        if not task_id:
            raise Exception("Could not get the scheduled task id: {}".format(r))

        result = self._wait_for_task(task_id)
        url = result.get("exportURL", None)
        if not url:
            raise Exception("Unexpected task result: {}".format(result))
        return url
