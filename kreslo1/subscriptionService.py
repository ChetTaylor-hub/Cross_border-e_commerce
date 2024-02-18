import datetime
import mysql.connector

class SubscriptionService:
    def __init__(self):
        cnx = mysql.connector.connect(user='username', password='password',
                                      host='127.0.0.1',
                                      database='database_name')

        self.subscribers = {}  # 存储订阅者信息，格式为 {subscriber_id: {'subscription_date': subscription_date}}

        self.subscription_fee = 10  # 每月订阅费用，以便后续计费使用

    def subscribe(self, subscriber_id):
        if subscriber_id in self.subscribers:
            print("已经订阅过了")
        else:
            self.subscribers[subscriber_id] = {'subscription_date': datetime.date.today()}
            print("订阅成功")

    def unsubscribe(self, subscriber_id):
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]
            print("退订成功")
        else:
            print("未找到订阅记录")

    def calculate_billing(self, subscriber_id):
        if subscriber_id in self.subscribers:
            subscription_date = self.subscribers[subscriber_id]['subscription_date']
            current_date = datetime.date.today()
            months_subscribed = (current_date.year - subscription_date.year) * 12 + current_date.month - subscription_date.month
            total_fee = months_subscribed * self.subscription_fee
            print(f"用户 {subscriber_id} 应付费用为 {total_fee} 元")
        else:
            print("未找到订阅记录")

# 使用示例
subscription_service = SubscriptionService()
subscription_service.subscribe("user1")
subscription_service.subscribe("user2")
subscription_service.calculate_billing("user1")
subscription_service.calculate_billing("user3")
subscription_service.unsubscribe("user2")
subscription_service.calculate_billing("user2")
