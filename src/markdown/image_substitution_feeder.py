import re
from typing import Dict
from urllib.parse import unquote
from src.markdown.service import LineFeeder


class ImageSubstitutionLineFeeder(LineFeeder):
    def __init__(self, img_mapping: Dict[str, str]):
        self._img_mapping = img_mapping
        self._img_pattern = re.compile(r"\!\[.*\]\((?!http)(.*)\)")

    def read_line(self, line: str) -> str:
        img_list = self._img_pattern.findall(line)
        for img in img_list:
            unquoted_img = unquote(img, encoding="utf-8")
            if unquoted_img not in self._img_mapping:
                continue
            line = line.replace(img, self._img_mapping[unquoted_img])
        return line
