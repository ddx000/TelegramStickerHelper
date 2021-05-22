
from PIL import Image
from bs4 import BeautifulSoup
import requests
from io import BytesIO
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
    byte_io.seek(0)
    return byte_io






