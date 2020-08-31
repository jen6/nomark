from typing import Mapping
from nomark.constants.const import NOTION_TOKEN_ENV_STR


class NotionConfig:
    token_v2: str

    def __init__(self, env: Mapping):
        self.token_v2 = env.get(NOTION_TOKEN_ENV_STR, "")
