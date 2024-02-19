'''
Author: TaoChen 2575394301@qq.com
Date: 2024-01-22 15:58:20
LastEditors: TaoChen 2575394301@qq.com
LastEditTime: 2024-01-23 16:40:20
FilePath: \kreslo1\pickup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from ozon_Api import OzonApi
from loguru import logger
import time
import os

if not os.path.exists("log"):
    os.makedirs("log")
logger.add("log/pickup.log", filter=lambda record: record["extra"].get("name") == "pickup")
logger_pickup = logger.bind(name="pickup")

def urgePickUp(headers, delay):
    ozonapi = OzonApi(headers)
    status = 'delivering'
    substatus = "posting_in_pickup_point"
    text = "Ваш курьер доставлен, пожалуйста, заберите товар как можно скорее"

    try:
        postings = ozonapi.ShipmentList(status=status)
        postings = ozonapi.SelectFromShipmentList(postings, substatus)
        for posting in postings:
            chat_id = ozonapi.ChatBuyersStart(posting)
            res = ozonapi.ChatBuyersSend(chat_id, text)
            logger_pickup.info(f"货物号：{posting} 聊天标号：{chat_id} 发送消息：<{text}> {'成功' if res else '失败'}")
        return True
    except Exception as e: 
        logger_pickup.error(f"捕获到异常：{e} 异常类型：{type(e)}")
        return False
    finally:
        time.sleep(int(delay))

if __name__ == "__main__":
    headers = [
        {
            "Client-Id": "1499102",
            "Api-Key": "d8c89da0-9caa-4d70-b034-54a2f21c94a2",
        },
        {
            "Client-Id": "1590307",
            "Api-Key": "6e3bcfea-5b59-4997-a3ad-9c24a5611ccd",
        },
        {
            "Client-Id": "1549760",
            "Api-Key": "dd1fc6b2-ab2f-4f4c-8f3f-de0c35576f18"
            
        },
        {
            "Client-Id": "1590307",
            "Api-Key": "584b7497-e27e-4c41-91f4-abf67a4a33e5"
        }
    ]
    delay = 1
    while True:
        urgePickUp(headers[-1], delay)
        # time.sleep(60)