import json
from unittest.mock import MagicMock, Mock
from googleapiclient.discovery import build
from googleapiclient.http import HttpMock, HttpMockSequence
from nomark.config.gdrive_config import GdriveConfig

from nomark.gdrive.service import GdriveService


class TestGdrive:
    def test_gdrive(self):
        image_folder = "imagehosting"
        api_key = "your_api_key"
        folder_id = "givne_folder_id"
        image_file_name = "image_0.png"
        image_ids = [f"given_image_id_{i}" for i in range(10)]
        article_title = "test_article"
        article_folder_id = "test-article-id"
        http = HttpMockSequence(
            [
                ({"status": "200"}, open("tests/data/drive.json", "rb").read()),
                ({"status": "200"}, json.dumps({"files": [{"id": folder_id}]})),
                ({"status": "200"}, json.dumps({"files": [{"id": article_folder_id}]})),
                # (
                #    {"status": "200"},
                #    json.dumps(
                #        {
                #            "files": [
                #                {"id": image_ids[0], "md5Checksum": "asdf0"},
                #                {"id": image_ids[1], "md5Checksum": "asdf1"},
                #            ]
                #        }
                #    ),
                # ),
                (
                    {"status": "200", "location": "location"},
                    json.dumps({"id": image_ids[0]}),
                ),
                ({"status": "200"}, json.dumps({"id": image_ids[0]})),
                ({"status": "200"}, "{}"),
            ]
        )
        mock_gdrive_config = MagicMock()
        mock_gdrive_config.article_title = article_title
        mock_gdrive_config.blog_folder = image_folder
        mock_gdrive_config.credit = api_key

        service = build("drive", "v3", http=http, developerKey=api_key)
        gdrive_service = GdriveService(config=mock_gdrive_config, api_service=service)
        result = gdrive_service.upload_img(
            image_file_name, f"tests/data/{image_file_name}"
        )
        assert result == f"https://drive.google.com/uc?export=view&id={image_ids[0]}"

    def test_check_create_folder(self):
        api_key = "your_api_key"

        image_folder = "imagehosting"
        image_folder_id = "imagehosting-id"

        article_title = "test_article"
        article_folder_id = "test-article-id"

        http = HttpMockSequence(
            [
                ({"status": "200"}, open("tests/data/drive.json", "rb").read()),
                ({"status": "200"}, json.dumps({})),
                ({"status": "200"}, json.dumps({"id": image_folder_id})),
                ({"status": "200"}, json.dumps({})),
                ({"status": "200"}, json.dumps({"id": article_folder_id})),
            ]
        )
        mock_gdrive_config = MagicMock()
        mock_gdrive_config.article_title = article_title
        mock_gdrive_config.blog_folder = image_folder
        mock_gdrive_config.credit = api_key

        service = build("drive", "v3", http=http, developerKey=api_key)
        gdrive_service = GdriveService(config=mock_gdrive_config, api_service=service)

        result = gdrive_service._check_create_folder()
        assert result == article_folder_id

    def test_check_create_folder_exists(self):
        api_key = "your_api_key"

        image_folder = "imagehosting"
        image_folder_id = "imagehosting-id"

        article_title = "test_article"
        article_folder_id = "test-article-id"

        http = HttpMockSequence(
            [
                ({"status": "200"}, open("tests/data/drive.json", "rb").read()),
                ({"status": "200"}, json.dumps({"files": [{"id": image_folder_id}]})),
                ({"status": "200"}, json.dumps({})),
                ({"status": "200"}, json.dumps({"id": article_folder_id})),
            ]
        )
        mock_gdrive_config = MagicMock()
        mock_gdrive_config.article_title = article_title
        mock_gdrive_config.blog_folder = image_folder
        mock_gdrive_config.credit = api_key

        service = build("drive", "v3", http=http, developerKey=api_key)
        gdrive_service = GdriveService(config=mock_gdrive_config, api_service=service)

        result = gdrive_service._check_create_folder()
        assert result == article_folder_id
