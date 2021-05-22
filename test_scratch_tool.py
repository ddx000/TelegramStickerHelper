"""
How to run pytest

pipenv run pytest -s
"""

from re import U
import pytest
import validators
from bs4 import BeautifulSoup
import requests
import re
import json 

from scratch_tool import LineSticker 


@pytest.mark.parametrize("sticker_url",['https://store.line.me/stickershop/product/10306/zh-Hant'])
def test_get_parsed_urls(sticker_url):
    sticker_urls, name = LineSticker.get_parsed_urls(sticker_url)
    for uri in sticker_urls:
        if not validators.url(uri):
            print("####")
            print(type(uri))
            print(uri)
        else:
            print("pass")
        


def test_crawler():
    url = 'https://store.line.me/stickershop/product/14940212/zh-Hant'
    try:
        print('parsing_html', url)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
    except Exception as e:
        print('error on handling url', e)
    # sticker_url_lst = []
    results = soup.find_all("li")
    for res in results:
        image_url = res.attrs.get('data-preview',{})
        if image_url:
            dict = json.loads(image_url)
            print(dict.get("staticUrl"))

    # for tag in soup.select('li'):
    #     print("----------")
    #     print(tag)