import json

from crawler.base_crawler import BaseCrawler
from crawler.scratch_tool import get_soup_by_url


class LineCrawler(BaseCrawler):
    @staticmethod
    def _get_sticker_img_set(url):
        soup = get_soup_by_url(url)
        sticker_img_set = set()
        li_tags = soup.find_all("li")
        for li_tag in li_tags:
            try:
                data_preview = li_tag.attrs.get("data-preview", {})
                if data_preview:
                    dict = json.loads(data_preview)
                    img_url = dict.get("staticUrl")
                    if img_url:
                        remove_string = ";compress=true"
                        if img_url.endswith(remove_string):
                            img_url = img_url[: -len(remove_string)]
                        sticker_img_set.add(img_url)
            except Exception as ex:
                print(f"Exception happend in parsing image {ex}")
        return sticker_img_set

    @staticmethod
    def get_sticker_name(url):
        soup = get_soup_by_url(url)
        p_tag = soup.find("p", {"data-test": "sticker-name-title"})
        if p_tag and p_tag.contents:
            return str(p_tag.contents[0])
        else:
            return "UnknownStickerName"
