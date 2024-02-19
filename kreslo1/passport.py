import time, os
from loguru import logger
from ozon_Api import OzonApi

if not os.path.exists("log"):
    os.makedirs("log")
logger.add("log/passport.log", filter=lambda record: record["extra"].get("name") == "passport")
logger_passport = logger.bind(name="passport")


def register_passport(headers, delay):
    # 实现填写护照功能的函数
    ozonapi = OzonApi(headers)
    # 实现填写护照功能的函数
    status = "awaiting_packaging"
    substatus = "posting_awaiting_passport_data"
    text = "Ваши паспортные данные еще не собраны, пожалуйста, заполните их как можно скорее"

    try:
        postings = ozonapi.ShipmentList(status=status)
        postings = ozonapi.SelectFromShipmentList(postings, substatus)
        for posting in postings:
            chat_id = ozonapi.ChatBuyersStart(posting)
            res = ozonapi.ChatBuyersSend(chat_id, text)
            logger_passport.info(f"货物号：{posting} 聊天标号：{chat_id} 发送消息：<{text}> {'成功' if res else '失败'}")
        return True
        
    except Exception as e:
        logger_passport.error(f"捕获到异常：{e} 异常类型：{type(e)}")
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
        },
        {
            "Client-Id": "1314849",
            "Api-Key": "88bf1c90-674b-4ac8-8e48-fd1421c4d4f4"
        }
    ]
    delay = 1
    while True:
        register_passport(headers[-2], delay)
        # time.sleep(60)

