from googleapiclient.http import MediaFileUpload
from src.config.gdrive_config import GdriveConfig
from urllib.parse import unquote


from googleapiclient.discovery import build


class GdriveService:
    def __init__(self, config: GdriveConfig):
        self._credit = config.credit
        self._base_folder = config.blog_folder
        self._service = build("drive", "v3", credentials=self._credit)
        self._target_folder_id = self._check_create_folder()

    def _check_create_folder(self) -> str:
        folder_id = None
        # Call the Drive v3 API
        page_token = None
        while True:
            response = (
                self._service.files()
                .list(
                    q="mimeType='application/vnd.google-apps.folder' and name='%s'"
                    % self._base_folder,
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            for file in response.get("files", []):
                folder_id = file.get("id")
                break

            if folder_id != None:
                break

            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        if folder_id == None:
            fname = {
                "name": self._base_folder,
                "mimeType": "application/vnd.google-apps.folder",
            }
            folder = self._service.files().create(body=fname, fields="id").execute()
            folder_id = folder.get("id")
        return folder_id

    def upload_img(self, img: str) -> str:
        fmeta = {"name": img, "parents": [self._target_folder_id]}
        media = MediaFileUpload(
            "./" + unquote(img), mimetype="image/jpeg", resumable=True
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
        return "https://drive.google.com/uc?export=view&id=" + upload_id
