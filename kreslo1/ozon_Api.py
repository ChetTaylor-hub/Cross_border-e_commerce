import requests
import pandas as pd
import openpyxl
import time

class OzonApi():
    def __init__(self, headers):
        self.headers = headers

    def getheader(self):
        return self.headers

    def ShipmentList(self, status=""):
        """获取订单列表

        Args:
            status (str, optional): 订单状态. Defaults to "".
        """        
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
        """筛选订单

        Args:
            Self (_type_): _description_
            response (html——respnose): 获取到的全部订单
            substatus (str, optional): 订单状态. Defaults to "".

        Returns:
            list: 筛选后的订单
        """        
        postings = []
        # 筛选订单
        for i in response.json()["result"]["postings"]:
            if i["substatus"] == substatus:
                postings.append(i)
            # print(i["posting_number"])
        return postings
        

    def ChatBuyersStart(self, response, ChatContent):
        # 创建聊天窗口
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
        # 发送消息
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
        # 获取聊天记录
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
        # 获取商品列表
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
        # 获取商品网址
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
        # 促销活动列表
        url = "https://api-seller.ozon.ru/v1/actions"

        response = requests.get(url, headers=self.headers)

        return response.json()["result"]
    
    def aListOfParticipatingProducts(self, action_id):
        # 参与某促销活动的商品列表
        url = "https://api-seller.ozon.ru/v1/actions/products"

        application = {
            "action_id": action_id,
            # "limit": 100,
            # "offset": 0
        }

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]["products"]
    
    def removeTheItemFromTheEvent(self, action_id, product_ids):
        # 从促销活动中删除商品
        url = "https://api-seller.ozon.ru/v1/actions/products/deactivate"
        application = {
            "action_id": action_id,
            "product_ids": product_ids
        }

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]
    
    def updateYourInventory(self, offer_id, product_id, stock):
        # 更新库存
        url = "https://api-seller.ozon.ru/v1/product/import/stocks"

        application = {
            "stocks": [
                {
                    "offer_id": "PG-2404С1",
                    "product_id": 55946,
                    "stock": 4
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=application)
        
        return response.json()["result"]
    
    def updateTheNumberOfItemsInYourInventory(self, offer_id, product_id, stock, warehouse_id):
        """_summary_

        Args:
            offer_id (string): _description_
            product_id (int64): _description_
            stock (int64): _description_
            warehouse_id (int64): _description_

        Returns:
            list: 更新信息
        """        
        url = "https://api-seller.ozon.ru/v2/products/stocks"

        application = {
            "stocks": [
                {
                    "offer_id": offer_id,
                    "product_id": product_id,
                    "stock": stock,
                    "warehouse_id": warehouse_id
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=application)
        
        return response.json()["result"]
    
    def updateYourInventory(self, offer_id, product_id, stock):
        """_summary_

        Args:
            offer_id (string): _description_
            product_id (int64): _description_
            stock (int64): _description_

        Returns:
            list: 更新信息
        """        
        url = "https://api-seller.ozon.ru/v1/product/import/stocks"

        application = {
            "stocks": [
                {
                    "offer_id": offer_id,
                    "product_id": product_id,
                    "stock": stock
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=application)
        
        return response.json()["result"]
    
    def informationAboutTheNumberOfProducts(self, offer_id, product_id):
        """ 获取商品库存信息

        Args:
            offer_id (string): 卖家系统中的商品编号是 — 商品代码
            product_id (int64): 商品id

        Returns:
            list: 商品库存数量
        """        
        url = "https://api-seller.ozon.ru/v3/product/info/stocks"

        application = {
            "filter": {
                "offer_id": [
                    offer_id
                ],
                "product_id": [
                    product_id
                ],
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 1000
        }

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]["items"]
    
    def warehouseList(self):
        """ 获取仓库列表

        Returns:
            list: 仓库列表
        """
        url = "https://api-seller.ozon.ru/v1/warehouse/list"

        application = {}

        response = requests.post(url, headers=self.headers, json=application)

        return response.json()["result"]

def complaintsAndSales():
    # 投诉
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



def updateProductInventory():
    # 更新商品库存
    ozonapi = OzonApi(headers[0])
    # pd打开excel文件
    df = pd.read_excel(r"D:\Downloads\stock-update-template.xlsx")
    # 获取A，B，D列的数据
    products = ozonapi.getTheProductList()
    for product in products:
        items = ozonapi.informationAboutTheNumberOfProducts(product["offer_id"], product["product_id"])
        warehouses = ozonapi.warehouseList()
        for warehouse in warehouses:
            for stock in items[0]["stocks"]:
                result = ozonapi.updateTheNumberOfItemsInYourInventory(product["offer_id"], product["product_id"], stock["present"], warehouse["warehouse_id"])
                # result = ozonapi.updateYourInventory(product["offer_id"], product["product_id"], result[0]["stock"])
                print(f"商品id：{product['offer_id']} 已经更新库存，库存数量：{stock}, 仓库id：{warehouse['warehouse_id']}, 仓库名称：{warehouse['name']}")

if __name__ == "__main__":
    # text = "Здравствуйте, уважаемый клиент, наш склад был разрушен во время недавнего землетрясения в Ганьсу, Китай.Поэтому мы не можем отправить вам товар.Пожалуйста, закажете товар в другом из наших магазинов, и мы предоставим вам скидку.Еще раз, я хотел бы выразить вам свои самые искренние извинения, ссылка приведена ниже："
    # OzonApiForcopy = OzonApiForCommodityConversion(headers[0])
    # # OzonApiForcopy.run(headers[1], text)

    updateProductInventory()
    # OzonApiaaa.getTheProductList()

    