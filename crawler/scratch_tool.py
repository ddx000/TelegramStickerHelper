from PIL import Image
from bs4 import BeautifulSoup
import requests
from io import BytesIO
import base64
import logging as log

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log.FileHandler("debug.log"),
        log.StreamHandler()
    ]
)

def get_sticker_name_hash(name):
    try:
        name_b = name.encode("UTF-8")
        name_hash_b = base64.b64encode(name_b)
        name_hash = name_hash_b.decode("UTF-8")
        name_hash_filtered = filter_hash_name(name_hash)
        return name_hash_filtered
    except Exception as e:
        log.exception(f"error on get_sticker_name_hash {name} {e}")


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

    if len(filter_name)>15:
        filter_name = filter_name[:15]
    return filter_name


def get_soup_by_url(url):
    try:
        log.info(f"parsing_html{url}")
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
        return soup
    except Exception as e:
        log.exception(f"error on handling url {url} {e}")


def resize_img(byteIO):
    # Stickers telegram required must be 512*n or m*512
    try:
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
    except Exception as e:
        log.exception(f"error on resize_img{e}")
    
