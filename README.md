# Telegram Sticker Helper

# change to pipenv

pipenv install
pipenv run python .\TeleRobot.py

# how to run unittest


**It is illegal to upload copyrighted stickers to telegram, please use at your own risk**

Telegram Sticker Helper is an Sticker Bot for the Telegram Messenger.   

## Demo
Send the sticker website's url to the robot, then the bot will automatic scratch all the stickers images, and upload as one sticker set.  

![](https://i.imgur.com/ob3Eqbe.png)

## Use

Python 3.7.3


```
git clone https://github.com/ddx000/LineStickers_toTelegram.git
```
```
pip install -r requirements.txt
```

Use telegram to create a robot first [Turtorial](https://medium.com/%E8%AA%A4%E9%97%96%E6%95%B8%E6%93%9A%E5%8F%A2%E6%9E%97%E7%9A%84%E5%95%86%E7%AE%A1%E4%BA%BAzino/telegram%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA%E8%B6%85%E8%A9%B3%E7%B4%B0%E6%87%B6%E4%BA%BA%E5%8C%85-%E5%95%86%E7%AE%A1%E4%BA%BA%E9%83%BD%E7%9C%8B%E5%BE%97%E6%87%82-%E9%99%84python%E7%A8%8B%E5%BC%8F%E7%A2%BC-1ec81a91ce48)  

In the same folder, please create key.json by yourself. The content example is as follows:

```
{"RobotToken": "Your robot TOKEN",
"RobotName": "Your robot Name"}
```
then directly run it
```
python TeleRobot.py
```
paste the url on chat windows and then you will get stickers

## Known issue
- If a user crawls many line-shop webpage in a short time, the IP will be blocked.
- Reduce the number of crawled pages by avoid async request to sync method instead.
- PR if you have already solved it

## Change Logs

### 1.1
2020/7/4  
- Refactor backend code
- Fixed crawler issues(Sync)  
- added unittest  
### 1.0
2020/4/14
- First Commit  

---


**Disclaimer**:
1. This code is for academic use only, you can learn python, async, web crawler from it
2. It is mentioned in Telegram's usage specifications that stickers cannot upload copyrighted things, so it is illegal to crawl Line stickers arbitrarily, and you are responsible for the consequences.
3. The design in scratch_tool.py is replaceable, you can inherit LineSticker class to overwrite get_parsed_urls this function, you can crawl uncopyright pictures for uploading

**免責聲明**:
1. 本程式碼僅供學術使用，您可以從其中學到python, async, web crawler
2. Telegram使用規範中有提到，貼圖不能上傳有版權的東西，所以任意爬取Line貼圖是違法的，後果請自行負責
3. scratch_tool.py中設計是可替換的，可以自行繼承LineSticker class 來複寫 sticker_img_set函式，即可爬取無版權的圖片作為上傳使用

