# Async notes

由於異步編程的邏輯實在太不一樣，所以特別寫了一篇網誌說明基本概念
https://medium.com/@jimmy_huang/python-asyncio-%E5%8D%94%E7%A8%8B-d84b5b945b5b

client發出request後，等待server回應的時間
其實就是類似IO-Bound的問題

傳統的寫法如果要取得A,B,C,D四個資料，就要A->B->C->D按照順序執行

如果是異步的寫法
A-->
B-->
C-->
D-->
基本上就是類似先丟出request 之後再去等response

基本上就是 **事件循環**
1.創建Event Loop 2.在Event Loop上註冊任務(Tasks)
3.定義前用async 4.釋放資源用await

## 事件迴圈(Event loop)

既然異步程式可以在多個任務之間切換，一定有個list包含所有的任務，而這個task list和機制就稱為event loop

![](https://i.imgur.com/YA39xFW.png)
![](https://i.imgur.com/H5VWxmv.png)

## 回調函數(Callback)

若是event loop在搜尋task list發現有事情要發生了，會過執行callback

以上圖為例 就會執行Callback_B

注意 這個Callback_B一定要是non-blocking的!!
(等待IO時必須await給event loop)


```python3
import asyncio
loop = asyncio.get_event_loop() #建立一個Event Loop

async def example1(): # 定義一個中間會被中斷的協程
    print("Start example1 coroutin.")
    await asyncio.sleep(1) # 中斷協程一秒
    print("Finish example1 coroutin.")

async def example2(): # 定義一個協程
    print("Start example2 coroutin.")
    await asyncio.sleep(2)
    print("Finish example2 coroutin.")

tasks = [ # 建立一個任務列表
    asyncio.ensure_future(example1()),
    asyncio.ensure_future(example2()),
]

loop.run_until_complete(asyncio.wait(tasks))

```
## 常用python API

- 定義協程async
先解釋協程的意義，協程可以看做是"能在中途中斷、中途返回值給其他協程、中途恢復、中途傳入參數的函數"，和一般的函數只能在起始傳入參數，不能中斷，而且最後返回值給父函數之後就結束的概念不一樣。
定義協程很簡單，只要在定義函數時再前面加入"async"這個關鍵字就行了

- asyncio.ensure_future(example1())
這函數把協程對象封裝成一個task對象
但經過task對象的包裝才能被Event Loop執行，所以說task對象負責作為Event Loop和協程對象的溝通介面

- asyncio.wait(tasks)
這函數的用處在於把兩個example1和example2的兩個協程對象包成一個大的協程對象，就是把兩個小任務包成一個大任務。

- await asyncio.sleep(1)
asyncio.sleep(1)簡單來說就是啟動一個只有一秒的倒數計時器，比較需要解釋的是await這個關鍵字。

- loop.run_until_complete(coroutine)
就是讓註冊參數裡的任務並執行，等到任務完成就關閉Event Loop

- loop.run_forever()
這個函數一執行，Event Loop就會永遠執行不會被關閉，除非在程式中出現loop.stop()就停止

## 事件驅動 await

```
def a_coroutine():
　　     # do something...
        await listen_event_happend()
        # do something after event happend...
```

因為當我們要在一個Coroutine裡中途監聽某一個Event發生後再執行後續行為時，只需要用await關鍵字來等待某個Event發生