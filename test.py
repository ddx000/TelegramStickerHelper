import unittest
import io
from scratch_tool import *


class ScratchToolTest(unittest.TestCase):
    def test_parsed_urls(self):
        url = 'https://store.line.me/stickershop/product/10306/zh-Hant'
        expect_first_url = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/27533208/iPhone/sticker@2x.png'
        sticker_url_lst , _ = LineSticker().get_parsed_urls(url)
        self.assertEqual(expect_first_url, sticker_url_lst[0])

    def test_resize_func(self):
        result = LineSticker().get_test_imgbytes()[0]
        self.assertIsInstance(result, io.BytesIO)
        

if __name__ == '__main__':
    unittest.main()