from ozon_Api import OzonApi
import pandas as pd
import time
from loguru import logger

logger.add("update.log", filter=lambda record: record["extra"].get("name") == "update")
logger_update = logger.bind(name="update")

def updateProductInventory(headers, delay, excel="stock-update-template.xlsx"):
    # 更新商品库存
    ozonapi = OzonApi(headers)
    # api的请求内容
    stocks = []

    try:
        # pd打开excel文件，读取指定sheet的数据
        df = pd.read_excel(excel, sheet_name="仓库库存", usecols=[0, 1, 3])
        # 取出仓库名称，货号，数量的列，并转化为字典
        dfs = df.to_dict(orient="records")
        for i, df in enumerate(dfs):
            # 获取数量
            stock = df["数量"]
            # 获取货号
            offer_id = df["货号"]
            # 获取仓库id
            warehouse_id = df["仓库名称"].split(" ")[1].split("(")[1].split(")")[0]

            stocks.append({"offer_id": offer_id, "stock": stock, "warehouse_id": warehouse_id})

            # 循环100此或者到达列表最后一个元素，更新一次库存
            if (i % 99 == 0 and i != 0) or i == len(dfs) - 1:
                # 更新库存
                result = ozonapi.updateTheNumberOfItemsInYourInventory(stocks)
                # result = ozonapi.updateYourInventory(product["offer_id"], product["product_id"], result[0]["stock"])
                for result_ in result:
                    logger_update.info(f"商品货号：{result_['offer_id']} {'更新库存成功' if result_['updated'] else '更新库存失败'}，仓库id：{result_['warehouse_id']}")
                # 清空列表
                stocks.clear()
        return True
    except Exception as e:
        logger_update.error(f"捕获到异常：{e} 异常类型：{type(e)}")
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
            
        }
    ]
    updateProductInventory(headers[2], 10)