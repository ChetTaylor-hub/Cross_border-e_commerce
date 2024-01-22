import requests

class OzonApi():
    def __init__(self, headers):
        self.headers = headers

    def getheader(self):
        return self.headers

    def ShipmentList(self, status=""):
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
                "status": status,
                "to": "2023-12-24T11:47:39.878Z",
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

        # print(response.json())
        # print(response.json()["result"]["status"])
        print(f"-------------total: {len(response.json()['result']['postings'])}-------------")
        for i in response.json()["result"]["postings"]:
            print(f"order: {i['order_id']}, status: {i['status']}, substatus: {i['substatus']}")
        return response
    
    def SelectFromShipmentList(Self, response, substatus=""):
        postings = []
        # 筛选订单
        for i in response.json()["result"]["postings"]:
            if i["substatus"] == substatus:
                postings.append(i)
            # print(i["posting_number"])
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
            # print(response.json())

        return chat_ids

    def ChatBuyersSend(self, chat_ids, text="no text"):
        url = "https://api-seller.ozon.ru/v1/chat/send/message"

        for chat_id in chat_ids:
            print(f"---------chat_id: {chat_id}正在被发送---------")

            send_ret = False

            while send_ret == False: # 如果发送不成功，则一直发送
                application = {
                    "chat_id": chat_id,
                    "text": text
                }
                response = requests.post(url, headers=self.headers, json=application)
                # print(response.json())
                if response.json()["result"] == "success":
                    print(f"---------chat_id: {chat_id}发送成功---------")
                    send_ret = True

    def chatHistory(self, chat_id):
        url = "https://api-seller.ozon.ru/v2/chat/history"
        applacation = {
            "chat_id": chat_id,
            # "direction": "Forward",
            # "from_message_id": 3000000000118032000,
            # "limit": 1
        }
        response = requests.post(url, headers=self.headers, json=applacation)
        return response.json()
    
    def getTheProductList(self):
        url = "https://api-seller.ozon.ru/v2/product/list"
        application = {
            "filter": {
                # "offer_id": [
                #     "136748"
                # ],
                # "product_id": [
                #     "223681945"
                # ],
                "visibility": "IN_SALE"
            },
            "last_id": "",
            # "limit": 100
        }
        response = requests.post(url,
                                 headers=self.headers,
                                 json=application)


        return response.json()["result"]["items"]
    
    def getTheProductWebsite(self, offer_id):
        url = "https://api-seller.ozon.ru/v2/product/info"

        application = {
            "offer_id": offer_id,
            # "product_id": 137208233,
            # "sku": 0
        }
        response = requests.post(url,
                                 headers=self.headers,
                                 json=application)
        website = f"https://www.ozon.ru/product/{response.json()['result']['sku']}/"

        return website

    def ReminderRegisterPassport(self):
        print(f"{'-'*30}{self.getheader()} 开始发送提醒注册护照的信息{'-'*30}")
        ChatContent = {
            "substatus": "posting_awaiting_passport_data",
            "text": "Your passport information has not been collected yet, please fill it out as soon as possible"
        }

        response = self.ShipmentList()
        chat_ids = self.ChatBuyersStart(response, ChatContent)
        self.ChatBuyersSend(chat_ids, ChatContent["text"])

    def listOfActivities(self):
        url = "https://api-seller.ozon.ru/v1/actions"

        response = requests.get(url, headers=self.headers)

        return response.json()["result"]
    
    def aListOfParticipatingProducts(self, action_id):
        url = "https://api-seller.ozon.ru/v1/actions/products"

        application = {
            "action_id": action_id,
            # "limit": 100,
            # "offset": 0
        }

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]["products"]
    
    def removeTheItemFromTheEvent(self, action_id, product_ids):
        url = "https://api-seller.ozon.ru/v1/actions/products/deactivate"
        application = {
            "action_id": action_id,
            "product_ids": product_ids
        }

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]

def complaintsAndSales():
    Ozinapi = OzonApi(headers[2])
    while True:
        productlist = Ozinapi.getTheProductList()
        for product in productlist:
            try:
                url = Ozinapi.getTheProductWebsite(product["offer_id"])
                Complaint.complaint(url)
            except:
                continue

class OzonApiForCommodityConversion(OzonApi):
    def __init__(self, header) -> None:
        super(OzonApiForCommodityConversion, self).__init__(header)
        self.url = {
            "productList": "https://api-seller.ozon.ru/v2/product/list",
            "productInformation": "https://api-seller.ozon.ru/v2/product/info",
            "productDetails": "https://api-seller.ozon.ru/v1/product/info/description"
        }

    def getTheProductList(self, header):
        products = []
        application = {
            "filter": {
                # "offer_id": [
                #     "136748"
                # ],
                # "product_id": [
                #     "223681945"
                # ],
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 100
        }

        response = requests.post(self.url["productList"],
                                 headers=header,
                                 json=application)


        return response.json()["result"]["items"]
    

    
    def getTheProductWebsite(self, header):
        products = {
            "website": [],
            "info": []
        }

        GoodsSale = self.ShipmentList()
        postings = self.SelectFromShipmentList(GoodsSale, substatus="posting_awaiting_passport_data")

        for posting in postings:
            application = {
                "offer_id": posting["products"][0]["offer_id"],
                # "product_id": 137208233,
                # "sku": 0
            }
            response = requests.post(self.url["productInformation"],
                                     headers=header,
                                     json=application)
            products["website"].append(f"https://www.ozon.ru/product/{response.json()['result']['sku']}/")
            products["info"].append(posting)


        return products["info"], products["website"]
    
    def ChatBuyersStart(self, infos):
        chat_ids = []
        url = "https://api-seller.ozon.ru/v1/chat/start"
        
        for info in infos:
            # 逐个创建聊天窗口，返回聊天窗口id号
            application = {
                "posting_number": info["posting_number"]
            }

            response = requests.post(url, headers=self.headers, json=application)

            chat_ids.append(response.json()["result"]["chat_id"])
            # print(response.json())

        return chat_ids
    
    def ChatBuyersSend(self, chat_ids, websites, text="no text"):
        url = "https://api-seller.ozon.ru/v1/chat/send/message"

        for chat_id, website in zip(chat_ids, websites):
            print(f"---------chat_id: {chat_id} 正在被发送---------")

            send_ret = False

            while send_ret == False: # 如果发送不成功，则一直发送
                application = {
                    "chat_id": chat_id,
                    "text": f"{text}{website}"
                }
                response = requests.post(url, headers=self.headers, json=application)
                # print(response.json())
                if response.json()["result"] == "success":
                    print(f"---------chat_id: {chat_id} 发送成功---------")
                    send_ret = True



    def run(self, header, text="no text"):
        print(f"{'-'*30}{self.getheader()} 开始发送提醒网址的信息{'-'*30}")
        text = "Здравствуйте, уважаемый клиент, наш склад был разрушен во время недавнего землетрясения в Ганьсу, Китай.Поэтому мы не можем отправить вам товар.Пожалуйста, закажете товар в другом из наших магазинов, и мы предоставим вам скидку.Еще раз, я хотел бы выразить вам свои самые искренние извинения, ссылка приведена ниже："

        infos, websites = self.getTheProductWebsite(header)
        chat_ids = self.ChatBuyersStart(infos)

        # 去除已发送的chat_id
        for chat_id in chat_ids:
            chat_history = self.chatHistory(chat_id)
            for message in chat_history["messages"]:
                if text in message["data"][0]:
                    chat_ids.remove(chat_id)
                    break
        self.ChatBuyersSend(chat_ids, websites, text)

url = "https://www.ozon.ru/product/1356525140/"


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


def deleteAPromotionalItem():
    ozonapi = OzonApi(headers[2])
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
        # logger.info(f"活动id：{i['id']} 已经删除了参加活动的商品，商品id：{result['product_ids']}, 拒绝删除的商品id：{result['rejected']}")
        print(f"活动id：{i['id']} 已经删除了参加活动的商品，商品id：{result['product_ids']}, 拒绝删除的商品id：{result['rejected']}")
        # ozonapi.removeTheItemFromTheEvent(i["id"])

if __name__ == "__main__":
    # text = "Здравствуйте, уважаемый клиент, наш склад был разрушен во время недавнего землетрясения в Ганьсу, Китай.Поэтому мы не можем отправить вам товар.Пожалуйста, закажете товар в другом из наших магазинов, и мы предоставим вам скидку.Еще раз, я хотел бы выразить вам свои самые искренние извинения, ссылка приведена ниже："
    # OzonApiForcopy = OzonApiForCommodityConversion(headers[0])
    # # OzonApiForcopy.run(headers[1], text)

    deleteAPromotionalItem()
    # OzonApiaaa.getTheProductList()

    