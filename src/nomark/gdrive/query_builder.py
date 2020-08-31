from enum import Enum, auto


class FileType(Enum):
    FOLDER = auto()
    FILE = auto()


_file_mapping = {
    FileType.FOLDER: "mimeType='application/vnd.google-apps.folder'",
    FileType.FILE: "mimeType!='application/vnd.google-apps.folder'",
}


class QueryBuilder:
    @classmethod
    def build(cls, file_name: str, file_type: FileType, parent_folder_id: str = None):
        file_type_query = _file_mapping.get(file_type, None)
        if file_type_query is None:
            raise ValueError("no mapped value")
        query = f"{file_type_query} and name='{file_name}'"

        if parent_folder_id is not None:
            query = f"{query} and '{parent_folder_id}' in parents"

        return query
