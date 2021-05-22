from PIL import Image
from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO
import json


def get_valid_sticker_name(url):
    """
    Valid_sticker_name must be only english alphabets
    The logic here is we convert sid (showed on urls - 5 digits)
    to alphabets (1->a 2->b )...and so on
    """
    sid = re.findall("/\d{5}/", url)[0][1:-1]
    ans = []
    for i in sid:
        ans.append(chr(int(i) + 97))

    return "".join(ans)


def get_soup_by_url(url):
    try:
        print("parsing_html", url)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
    except Exception as e:
        print("error on handling url", e)
    return soup


class LineSticker:
    # TODO have a base class
    def get_imgbytes(self, url):
        """Main Driver Functions -->  get_parsed_urls --> requests --> resize_img
        url: string(http_url)
        @return
        sticker_bytes_lst: lst of bytes
        """
        sticker_bytes_lst = []
        sticker_url_lst = self.get_parsed_urls(url)
        title = self.get_sticker_name(url)
        for one_url in sticker_url_lst:
            # TODO change to await request
            response = requests.get(one_url)
            sticker_bytes_lst.append(self.resize_img(BytesIO(response.content)))
        return sticker_bytes_lst, title

    def get_test_imgbytes(self):
        """for developer test on Telegram UI, input dev_test, return single resized google logo"""
        testurl = "https://www.google.com.tw/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
        response = requests.get(testurl)
        return [self.resize_img(BytesIO(response.content))]

    @staticmethod
    def get_sticker_img_set(url):
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
            return p_tag.contents[0]
        else:
            return "UnknownStickerName"

    @staticmethod
    def resize_img(byteIO):
        # CPU-Bound Functions
        # Stickers telegram required must be 512*n or m*512
        img = Image.open(byteIO)
        width, height = img.size[0], img.size[1]

        if width > height:
            resize_ratio = 512 / width
            img2 = img.resize((512, int(height * resize_ratio)), Image.BICUBIC)
        else:
            resize_ratio = 512 / height
            img2 = img.resize((int(width * resize_ratio), 512), Image.BICUBIC)
        byte_io = BytesIO()
        img2.save(byte_io, "PNG")
        byte_io.seek(0)
        return byte_io
