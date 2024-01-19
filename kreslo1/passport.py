import time
from loguru import logger
from ozon_Api import OzonApi

logger.add("passport_log.log")


def register_passport(headers, delay):
    # 实现填写护照功能的函数
    ozonapi = OzonApi(headers)
    # 实现填写护照功能的函数
    substatus = "posting_awaiting_passport_data"
    text = "Your passport information has not been collected yet, please fill it out as soon as possible"

    try:
        postings = ozonapi.ShipmentList()
        postings = ozonapi.SelectFromShipmentList(postings, substatus)
        for posting in postings:
            chat_id = ozonapi.ChatBuyersStart(posting)
            res = ozonapi.ChatBuyersSend(chat_id, text)
            logger.info(f"货物号：{posting} 聊天标号：{chat_id} 发送消息：<{text}> {'成功' if res else '失败'}")
        time.sleep(delay)
    except Exception as e:
        logger.error(f"捕获到异常：{e} 异常类型：{type(e)} 异常详细信息：{str(e)}")

