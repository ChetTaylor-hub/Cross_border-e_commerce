import requests

class OzonApi():
    def __init__(self, headers):
        self.headers = headers


    def ShipmentList(self):
        map = {
        "url": "https://api-seller.ozon.ru/v3/posting/fbs/list",
        "application": {
            "dir": "ASC",
            "filter": {
                # "delivery_method_id": [
                # "string"
                # ],
                # "fbpFilter": "string",
                # "last_changed_status_date": {
                # "from": "2023-11-03T11:47:39.878Z",
                # "to": "2023-12-03T11:47:39.878Z"
                # },
                # "order_id": 0,
                # "provider_id": [
                # "string"
                # ],
                "since": "2023-11-03T11:47:39.878Z",
                # "status": "awaiting_registration",
                "to": "2023-12-04T11:47:39.878Z",
                # "warehouse_id": [
                # "string"
                # ]
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
        
        url = map["url"]
        application = map["application"]

        response = requests.post(url, headers=self.headers, json=application)

        print(response.json())
        # print(response.json()["result"]["status"])
        for i in response.json()["result"]["postings"]:
            print(i["status"])
        return response
    
    def SelectFromShipmentList(Self, response, substatus):
        postings = []
        # 筛选订单
        for i in response.json()["result"]["postings"]:
            if i["substatus"] == substatus:
                postings.append(i)
            print(i["posting_number"])
        return postings
        

    def ChatBuyersStart(self, response, ChatContent):
        chat_ids = []
        
        posting_numbers = [posting["posting_number"] for posting in self.SelectFromShipmentList(response, ChatContent["substatus"])]

        url = "https://api-seller.ozon.ru/v1/chat/start"

        # 逐个创建聊天窗口，返回聊天窗口id号
        for posting_number in posting_numbers:
            application = {
                "posting_number": posting_number
            }

            response = requests.post(url, headers=self.headers, json=application)

            chat_ids.append(response.json()["result"]["chat_id"])
            print(response.json())

        return chat_ids

    def ChatBuyersSend(self, chat_ids, text="no text"):
        url = "https://api-seller.ozon.ru/v1/chat/send/message"

        for chat_id in chat_ids:
            send_ret = False

            while send_ret == False: # 如果发送不成功，则一直发送
                application = {
                    "chat_id": chat_id,
                    "text": text
                }
                response = requests.post(url, headers=self.headers, json=application)
                print(response.json())
                if response.json()["result"] == "success":
                    send_ret = True

    def ReminderDelivered(self, text = "Your goods have been delivered!"):
        ChatContent = {
            "substatus": "Delivered",
            "text": text
        }

        response = self.ShipmentList()
        chat_ids = self.ChatBuyersStart(response, ChatContent)
        self.ChatBuyersSend(chat_ids, ChatContent["text"])

    def ReminderRegisterPassport(self, text):
        ChatContent = {
            "substatus": "posting_awaiting_passport_data",
            "text": "Your passport information has not been collected yet, please fill it out as soon as possible"
        }

        response = self.ShipmentList()
        chat_ids = self.ChatBuyersStart(response, ChatContent)
        self.ChatBuyersSend(chat_ids, ChatContent["text"])


    def CompetitorsList(self):
        map = {
            "url": "https://api-seller.ozon.ru/v1/pricing-strategy/competitors/list",
            "application": {
                "page": 1,
                "limit": 49
            }
        }

        url = map["url"]
        application = map["application"]

        response = requests.post(url, headers=self.headers, json=application)

        print(response.json())
        # print(response.json()["result"]["status"])
        for i in response.json()["competitor"]:
            print(i["name"])
        return response




