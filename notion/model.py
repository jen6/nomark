from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ExportOptions:
    exportType: str = "markdown"
    timeZone: str = "Asia/Seoul"
    locale: str = "en"


class ExportedURLPayload:
    _block_id: str
    _recursive: bool
    _export_option: ExportOptions

    def __init__(
        self,
        block_id: str,
        recursive: bool = False,
        export_option: Optional[ExportOptions] = None,
    ):
        self._block_id = block_id
        self._recursive = recursive
        self._export_option = export_option or ExportOptions()

    def to_dict(self):
        payload = {
            "task": {
                "eventName": "exportBlock",
                "request": {
                    "blockId": self._block_id,
                    "recursive": self._block_id,
                    "exportOptions": asdict(self._export_option),
                },
            }
        }
        return payload
