"""
How to run pytest

pipenv run pytest -s
"""

import pytest
import validators
import io
from scratch_tool import LineSticker


line_shop_sticker_urls = [
    "https://store.line.me/stickershop/product/10306/zh-Hant",
    "https://store.line.me/stickershop/product/14940212/zh-Hant",
    "https://store.line.me/stickershop/product/23558/zh-Hant",
    "https://store.line.me/stickershop/product/14801072/zh-Hant",
]


@pytest.mark.parametrize("url", line_shop_sticker_urls)
def test_get_sticker_img_set(url):
    sticker_urls = LineSticker.get_sticker_img_set(url)
    for uri in sticker_urls:
        assert validators.url(uri)


@pytest.mark.parametrize("url", line_shop_sticker_urls)
def test_get_sticker_name(url):
    name = LineSticker.get_sticker_name(url)
    print(name)


def test_resize_func():
    result = LineSticker().get_test_imgbytes()[0]
    assert isinstance(result, io.BytesIO)