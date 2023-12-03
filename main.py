import time
from ozon_Api import OzonApi

headers = {
    "Client-Id": "1499102",
    "Api-Key": "d8c89da0-9caa-4d70-b034-54a2f21c94a2",
}


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

    ozonapi = OzonApi(headers)

    

        
    
    while True:

        ozonapi.ReminderRegisterPassport()
        time.sleep(10)

