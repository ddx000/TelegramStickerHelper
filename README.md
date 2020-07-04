# Telegram Sticker Helper

**純研究用途，請勿用於不當用途**

此程式提供一個簡易的Telegram聊天機器人，能附帶網頁爬取功能，
將指定網址上的貼圖轉換成Telegram上的貼圖(如: 您有購買的Line貼圖轉換至Telegram貼圖)

## 版本紀錄

2020/4/14: First Commit  
2020/7/4 : Refactor backend code, fixed crawler issues, added unittest  

## 已知問題:
- 使用者若短時間大量爬取Line網頁的貼圖，該IP會被block一段時間，目前是先將原先async的爬取改為sync一次抓一個網頁的作法


## 執行

本程式有用到python內帶的asyncio功能，建議python安裝版本為3.7或以上  
首先先將程式碼下載到本機，執行以下指令或是直接按右上方的下載按鈕  

```
git clone https://github.com/ddx000/LineStickers_toTelegram.git
```
安裝必要的套件
```
pip install -r requirements.txt
```

使用telegram先創立robot [教學](https://medium.com/%E8%AA%A4%E9%97%96%E6%95%B8%E6%93%9A%E5%8F%A2%E6%9E%97%E7%9A%84%E5%95%86%E7%AE%A1%E4%BA%BAzino/telegram%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA%E8%B6%85%E8%A9%B3%E7%B4%B0%E6%87%B6%E4%BA%BA%E5%8C%85-%E5%95%86%E7%AE%A1%E4%BA%BA%E9%83%BD%E7%9C%8B%E5%BE%97%E6%87%82-%E9%99%84python%E7%A8%8B%E5%BC%8F%E7%A2%BC-1ec81a91ce48)  
於同資料夾內，請自行創建key.json，內容範例如下:

```
{"RobotToken": "您的機器人TOKEN",
"RobotName": "您的機器人NAME"}
```

最後啟動程式
```
python TeleRobot.py
```

啟動程式後，即可於telegram Robot上貼上網址，讓機器人進行爬取

**免責聲明**:
1. 本程式碼僅供學術使用，您可以從其中學到python, async, web crawler
2. Telegram使用規範中有提到，貼圖不能上傳有版權的東西，所以任意爬取Line貼圖是違法的，後果請自行負責
3. scratch_tool.py中設計是可替換的，可以自行繼承LineSticker Class後 overwrite get_parsed_urls這個函式，即可爬取無版權的圖片作為上傳使用


### English Version

Notice: DON'T UPLOAD COPYRIGHTED STICKERS TO TELEGRAM !!!  

move your stickers from line to telegram by a telegram robot.  
just paste the sticker url on line shop, then it will generate a new stickerset  

This project is research-used purpose only, so we won't provide a robot url,  
please apply the robot from telegram and replace the robot name by yourself  
