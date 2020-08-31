from nomark.notion.service import NotionService
from nomark.notion.repository import NotionRepository
from unittest import TestCase
from uuid import uuid4
from unittest.mock import MagicMock, call


class ResponseMock:
    def __init__(self, body: dict):
        self.body = body

    def json(self) -> dict:
        return self.body


class NotionIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.token = str(uuid4())
        self.mock_session = MagicMock()
        self.notion_repo = NotionRepository()
        self.notion_service = NotionService(
            notion_cookie_token=self.token, notion_repo=self.notion_repo
        )

    def test_get_download_link(self):
        #  Given
        given_page_id = str(uuid4())
        given_task_id = str(uuid4())
        given_download_link = "http://google.com"

        mock_post = MagicMock()
        mock_post.side_effect = [
            ResponseMock({"taskId": given_task_id}),
            ResponseMock(
                {
                    "results": [
                        {
                            "state": "success",
                            "status": {"exportURL": given_download_link},
                        }
                    ]
                }
            ),
        ]
        self.mock_session.post = mock_post
        self.notion_repo.set_session(self.mock_session)

        #  When
        page_id_without_bar = given_page_id.replace("-", "")
        result_url = self.notion_service.get_exported_url(
            f"https://www.notion.so/jen6/{page_id_without_bar}"
        )

        #  Then
        self.assertEqual(
            [
                call(
                    NotionRepository.ENQUEUE_TASK_URL,
                    cookies={"token_v2": self.token},
                    json={
                        "task": {
                            "eventName": "exportBlock",
                            "request": {
                                "blockId": given_page_id,
                                "recursive": False,
                                "exportOptions": {
                                    "exportType": "markdown",
                                    "timeZone": "Asia/Seoul",
                                    "locale": "en",
                                },
                            },
                        }
                    },
                    timeout=10,
                ),
                call(
                    NotionRepository.GET_TASK_URL,
                    cookies={"token_v2": self.token},
                    json={"taskIds": [given_task_id]},
                    timeout=10,
                ),
            ],
            mock_post.call_args_list,
        )
        self.assertEqual(given_download_link, result_url)
