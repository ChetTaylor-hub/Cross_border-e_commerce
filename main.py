import time
from ozon_Api import OzonApi

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

delay_time = 10 # 延迟，单位是分钟


# response = SELLER_POSTINGS()
# report_info(response.json()["result"]["code"])

map = {
    "url": "https://api-seller.ozon.ru/v3/posting/fbs/get",
    "application": {
        "posting_number": "0118535500-0518-1",
        "with": {
        "analytics_data": False,
        "barcodes": False,
        "financial_data": False,
        "product_exemplars": False,
        "translit": False
        }
    }
}

map2 = {
    "url": "https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list",
    "application": {
        "dir": "ASC",
        "filter": {
            "cutoff_from": "2023-08-24T14:15:22Z",
            "cutoff_to": "2023-12-31T14:15:22Z",
            "delivery_method_id": [],
            # "provider_id": [],
            # "status": "awaiting_packaging",
            # "warehouse_id": []
        },
        "limit": 100,
        "offset": 0,
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "translit": True
        } 
    }
}


if __name__ == "__main__":

    delay_time *= 60 # 转换为分钟
    ozonapis = []
    for header in headers:
        ozonapis.append(OzonApi(header))

    while True:

        for ozonapi in ozonapis:
            print(f"{'-'*30}{ozonapi.getheader()}{'-'*30}")
            ozonapi.ReminderRegisterPassport()
        print(f"{'-'*30}等待{delay_time / 60}分钟{'-'*30}")
        time.sleep(delay_time)

