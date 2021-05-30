from crawler.scratch_tool import resize_img
from io import BytesIO
import requests
import logging as log

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log.FileHandler("debug.log"),
        log.StreamHandler()
    ]
)

class BaseCrawler:
    @classmethod
    def get_sticker_resized_bytes(cls, url):
        sticker_bytes_lst = []
        sticker_url_set = cls._get_sticker_img_set(url)
        for sticker_url in sticker_url_set:
            # TODO change to await request
            response = requests.get(sticker_url)
            sticker_bytes_lst.append(resize_img(BytesIO(response.content)))
        return sticker_bytes_lst

    @staticmethod
    def _get_sticker_img_set(url):
        pass

    @staticmethod
    def get_sticker_name(url):
        pass
