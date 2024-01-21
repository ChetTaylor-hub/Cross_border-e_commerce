import time
from loguru import logger
from ozon_Api import OzonApi

logger.add("passport.log", filter=lambda record: record["extra"].get("name") == "passport")
logger_passport = logger.bind(name="passport")


def register_passport(headers, delay):
    # 实现填写护照功能的函数
    ozonapi = OzonApi(headers)
    # 实现填写护照功能的函数
    substatus = "posting_awaiting_passport_data"
    text = "Ваши паспортные данные еще не собраны, пожалуйста, заполните их как можно скорее"

    try:
        postings = ozonapi.ShipmentList()
        postings = ozonapi.SelectFromShipmentList(postings, substatus)
        for posting in postings:
            chat_id = ozonapi.ChatBuyersStart(posting)
            res = ozonapi.ChatBuyersSend(chat_id, text)
            logger_passport.info(f"货物号：{posting} 聊天标号：{chat_id} 发送消息：<{text}> {'成功' if res else '失败'}")
        time.sleep(int(delay))
        return True
        
    except Exception as e:
        logger_passport.error(f"捕获到异常：{e} 异常类型：{type(e)}")

        time.sleep(int(delay))

        return False

