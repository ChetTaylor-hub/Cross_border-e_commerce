from ozon_Api import OzonApi
from loguru import logger
import time

logger.add("pickup.log", filter=lambda record: record["extra"].get("name") == "pickup")
logger_pickup = logger.bind(name="pickup")

def urgePickUp(headers, delay):
    ozonapi = OzonApi(headers)

    substatus = "posting_delivered"
    text = "Ваш курьер доставлен, пожалуйста, заберите товар как можно скорее"

    try:
        postings = ozonapi.ShipmentList()
        postings = ozonapi.SelectFromShipmentList(postings, substatus)
        for posting in postings:
            chat_id = ozonapi.ChatBuyersStart(posting)
            res = ozonapi.ChatBuyersSend(chat_id, text)
            logger_pickup.info(f"货物号：{posting} 聊天标号：{chat_id} 发送消息：<{text}> {'成功' if res else '失败'}")
        time.sleep(int(delay))
        return True
    except Exception as e:
        logger_pickup.error(f"捕获到异常：{e} 异常类型：{type(e)}")

        time.sleep(int(delay))
        return False