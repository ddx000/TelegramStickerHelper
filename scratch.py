from PIL import Image
import os
from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO

# ver0.1

class Scratch:
    def __init__(self, url):
        self.stickerurl = url
        self.title = None
        self.sticker_amount = 0
        self.imgUrlLst   = []  # list contains
        self.imgBytesLst = []  # list contains img bytes

    def get_image(self):
        """main functions
        the processed image will be stored in self.imgBytesLst"""
        self.parse_html()
        for i in self.imgUrlLst:
            response = requests.get(i)
            self.imgBytesLst.append(self.resize(BytesIO(response.content)))

    def parse_html(self):
        """parse stickerurl, a little messy, can be modufy for better effiency
        added into self.imgUrlLst"""
        print('getting this url', self.stickerurl)
        try:
            req = requests.get(self.stickerurl)
            soup = BeautifulSoup(req.text, 'lxml')
        except Exception as e:
            print(e)
        self.title = soup.select('h3')[0].text
        for tag in soup.select('li'):
            string = str(tag)
            lst = re.split(';|"', string)
            for i in lst:
                if 'iPhone/sticker@2x.png' in i:
                    self.imgUrlLst.append(i)
        self.sticker_amount = len(self.imgUrlLst)

    def resize(self,byteIO):
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
        img2.save(byte_io, 'PNG')
        byte_io.seek(0)
        return byte_io
