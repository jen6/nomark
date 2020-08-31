from googleapiclient.http import MediaFileUpload
from nomark.gdrive.query_builder import FileType, QueryBuilder
from nomark.config.gdrive_config import GdriveConfig
from urllib.parse import unquote, unquote_plus
import hashlib


from googleapiclient.discovery import build


class GdriveService:
    def __init__(self, config: GdriveConfig, api_service=None):
        self._credit = config.credit
        self._base_folder = f"{config.blog_folder}/{config.article_title}"
        self._service = api_service
        self._target_folder_id = None
        if self._service is None:
            self._service = build("drive", "v3", credentials=self._credit)

    def _check_create_folder(self, folder_path="", folder_id=None) -> str:
        if folder_path == "":
            return folder_id

        splited_path = folder_path.split("/", 1)
        result_folder_id = None
        # Call the Drive v3 API
        page_token = None
        while True:
            response = (
                self._service.files()
                .list(
                    q=QueryBuilder.build(
                        file_name=splited_path[0],
                        file_type=FileType.FOLDER,
                        parent_folder_id=folder_id,
                    ),
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )

            for file in response.get("files", []):
                result_folder_id = file.get("id")
                break

            if result_folder_id != None:
                break

            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        if result_folder_id == None:
            fname = {
                "name": unquote_plus(splited_path[0]),
                "mimeType": "application/vnd.google-apps.folder",
            }
            if folder_id is not None:
                fname["parents"] = [folder_id]

            folder = self._service.files().create(body=fname, fields="id").execute()
            folder_id = folder.get("id")

        if len(splited_path) > 1:
            return self._check_create_folder(
                folder_path=splited_path[1], folder_id=result_folder_id
            )

        return folder_id

    def _check_file_exists(self, file_name: str, folder_id: str, file_hash: str) -> str:
        page_token = None
        while True:
            response = (
                self._service.files()
                .list(
                    q=QueryBuilder.build(
                        file_name=file_name,
                        file_type=FileType.FILE,
                        parent_folder_id=folder_id,
                    ),
                    spaces="drive",
                    fields="nextPageToken, files(id, name, md5Checksum)",
                    pageToken=page_token,
                )
                .execute()
            )

            for file in response.get("files", []):
                if file_hash == file.get("md5Checksum"):
                    return file.get("id")

            if folder_id != None:
                break

            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        return ""

    @classmethod
    def _get_file_hash(cls, img_path, blocksize=65536):
        with open(img_path, "rb") as afile:
            hasher = hashlib.md5()
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
            return hasher.hexdigest()

    def upload_img(self, img: str, img_path: str) -> str:
        if self._target_folder_id == None:
            self._target_folder_id = self._check_create_folder(self._base_folder)

        file_hash = self._get_file_hash(img_path)
        upload_id = self._check_file_exists(
            img, folder_id=self._target_folder_id, file_hash=file_hash
        )
        if upload_id != "":
            return f"https://drive.google.com/uc?export=view&id={upload_id}"

        fmeta = {"name": img, "parents": [self._target_folder_id]}
        media = MediaFileUpload(
            "./" + unquote(img_path), mimetype="image/jpeg", resumable=True
        )
        upload = (
            self._service.files()
            .create(body=fmeta, media_body=media, fields="id")
            .execute()
        )
        upload_id = upload["id"]
        permission = {"type": "anyone", "role": "reader"}

        result = (
            self._service.permissions()
            .create(fileId=upload_id, body=permission, fields="id")
            .execute()
        )
        return f"https://drive.google.com/uc?export=view&id={upload_id}"
