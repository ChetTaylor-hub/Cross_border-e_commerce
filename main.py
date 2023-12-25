import time
from ozon_Api import OzonApi, OzonApiForCommodityConversion

bossheader = {
    "Client-Id": "1590307",
    "Api-Key": "6e3bcfea-5b59-4997-a3ad-9c24a5611ccd",
}

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
        "Api-Key": "7a39519b-81c5-4dbc-a1a4-06998c462536",
    },
    {
        "Client-Id": "1564761",
        "Api-Key": "c1819cb6-75aa-41c4-aee6-61ccd4732e88",
    }
]

delay_time = 0.5 # 延迟，单位是分钟



if __name__ == "__main__":

    delay_time *= 60 # 转换为分钟
    ozonApis = []
    ozonApiForCommodityConversions = []
    for header in headers:
        ozonApis.append(OzonApi(header))
        ozonApiForCommodityConversions.append(OzonApiForCommodityConversion(header))

    while True:

        for ozonapi, ozonApiForCommodityConversion in zip(ozonApis, ozonApiForCommodityConversions):
            print(f"{'-'*30}{ozonapi.getheader()}{'-'*30}")
            ozonapi.ReminderRegisterPassport()
            ozonApiForCommodityConversion.run(bossheader)
        print(f"{'-'*30}等待{delay_time / 60}分钟{'-'*30}")
        time.sleep(delay_time)

