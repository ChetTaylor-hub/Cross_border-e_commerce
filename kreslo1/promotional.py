from ozon_Api import OzonApi
from loguru import logger
import time

logger.add("promotional.log", filter=lambda record: record["extra"].get("name") == "promotional")
logger_passport = logger.bind(name="promotional")


def deleteAPromotionalItem(headers, delay):
    # 删除所有促销活动中的商品
    ozonapi = OzonApi(headers)
    try:
        result = ozonapi.listOfActivities()
        for i in result:
            if i["participating_products_count"] == 0:
                print(f"活动id：{i['id']} 没有参加活动的商品")
                continue
            products = ozonapi.aListOfParticipatingProducts(i["id"])
            product_ids = []
            for product in products:
                product_ids.append(product["id"])
            result = ozonapi.removeTheItemFromTheEvent(i["id"], product_ids)
            logger_passport.info(f"活动id：{i['id']} 已经删除了参加活动的商品，商品id：{result['product_ids']}, 拒绝删除的商品id：{result['rejected']}")
            return True
            # ozonapi.removeTheItemFromTheEvent(i["id"])
    except Exception as e:
        logger_passport.error(f"捕获到异常：{e} 异常类型：{type(e)}")
        return False
    finally:
        time.sleep(int(delay))

if __name__ == "__mian__":
    
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
            
        }
    ]
    deleteAPromotionalItem(headers[0], 10)

