from PIL import Image
from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO
import json
import base64


def get_sticker_name_hash(name):
    name_b = name.encode("UTF-8")
    name_hash_b = base64.b64encode(name_b)
    name_hash = name_hash_b.decode("UTF-8")
    name_hash_filtered = filter_hash_name(name_hash)
    return name_hash_filtered

def filter_hash_name(name_hash):
    """
    Valid_sticker_name must be only english alphabets
    """
    filter_name = ""
    for char in name_hash:
        if char.isalpha():
            filter_name += char
        elif char.isdigit():
            filter_name += chr(int(char) + 97)
    return filter_name

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
    @classmethod
    def get_sticker_resized_bytes(cls, url):
        sticker_bytes_lst = []
        sticker_url_set = cls.get_sticker_img_set(url)
        for sticker_url in sticker_url_set:
            # TODO change to await request
            response = requests.get(sticker_url)
            sticker_bytes_lst.append(cls.resize_img(BytesIO(response.content)))
        return sticker_bytes_lst

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
            return str(p_tag.contents[0])
        else:
            return "UnknownStickerName"

    @staticmethod
    def resize_img(byteIO):
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
        print(img2.size)
        byte_io.seek(0)
        return byte_io
