import datetime
import mysql.connector
import numpy as np

class SubscriptionService:
    def __init__(self, subscription_month_fee=10):
        # 实例化mysql类
        self.mysql_operation = MysqlOperation()

        self.subscribers = self.mysql_operation.query_all() # 存储订阅者信息，格式为 {subscriber_id: {'subscription_date': subscription_date}}

        self.subscription_fee = subscription_month_fee  # 每月订阅费用，以便后续计费使用

    def subscribe(self, subscriber_id):
        if self.mysql_operation.is_exist(subscriber_id):
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

    # 检查订阅者状态，超过一个月未付费的自动退订
    def check_subscribers(self, subscriber_id):
        if subscriber_id not in self.subscribers:
            return False, "未找到订阅记录"
        current_date = datetime.date.today()
        subscription_date = self.subscribers[subscriber_id]['subscription_date']
        months_subscribed = (current_date.year - subscription_date["year"]) * 12 + current_date.month - subscription_date["month"]
        if months_subscribed >= 1:
            self.unsubscribe(subscriber_id)
            return False, "已超过一个月未付费，已自动退订"
        return True, "正常"
    
# 操作mysql的类
class MysqlOperation:
    def __init__(self, user="username", password="password", host="47.115.205.226", database="subscription", table_name="subscriptionService"):
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           host=host, database=database,
                                           auth_plugin='caching_sha2_password')
        self.cursor = self.cnx.cursor()

        self.create_table(table_name)

    # 新建一个表格
    def create_table(self, table_name="subscriptionService"):
        # 检查表格是否存在，如果存在则跳过
        self.table_name = table_name
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if self.cursor.fetchone():
            return

        self.cursor.execute(f"CREATE TABLE {table_name} (subscriber_id VARCHAR(255), mail VARCHAR(255), subscription_date DATE)")

    def insert(self, subscriber_id, mail, subscription_date):
        add_subscriber = (f"INSERT INTO {self.table_name} "
                          "(subscriber_id, mail, subscription_date) "
                          "VALUES (%s, %s, %s)")
        data_subscriber = (subscriber_id, mail, subscription_date)
        self.cursor.execute(add_subscriber, data_subscriber)
        self.cnx.commit()

    def delete(self, subscriber_id):
        delete_subscriber = (f"DELETE FROM {self.table_name} WHERE subscriber_id = %s")
        data_subscriber = (subscriber_id,)
        self.cursor.execute(delete_subscriber, data_subscriber)
        self.cnx.commit()

    def query(self, subscriber_id):
        data = {}
        query = (f"SELECT * FROM {self.table_name} WHERE subscriber_id = %s")
        data_subscriber = (subscriber_id,)
        self.cursor.execute(query, data_subscriber)
        for (subscriber_id, mail, subscription_date) in self.cursor:
            data[subscriber_id] = {"subscription_date": f"{subscription_date.year:04}-{subscription_date.month:02}-{subscription_date.day:02}",
                                   "mail": mail}
            print(f"subscriber_id: {subscriber_id}, mail: {mail}, subscription_date: {subscription_date}")
        
        return data
    
    # 返回所有订阅者信息
    def query_all(self):
        data = {}
        query = (f"SELECT * FROM {self.table_name}")
        self.cursor.execute(query)
        for (subscriber_id, mail, subscription_date) in self.cursor:
            data[subscriber_id] = {"subscription_date": f"{subscription_date.year:04}-{subscription_date.month:02}-{subscription_date.day:02}",
                                   "mail": mail}
            print(f"subscriber_id: {subscriber_id}, mail: {mail}, subscription_date: {subscription_date}")
        
        return data

    # 判断订阅者id是否存在
    def is_exist(self, subscriber_id):
        data = self.query(subscriber_id)
        if not data:
            return False
        return True
    
    # 更新订阅者信息
    def update(self, subscriber_id, mail, subscription_date):
        update_subscriber = (f"UPDATE {self.table_name} SET mail = %s, subscription_date = %s WHERE subscriber_id = %s")
        data_subscriber = (mail, subscription_date, subscriber_id)
        self.cursor.execute(update_subscriber, data_subscriber)
        self.cnx.commit()

    # 更新数据库数据，去除没有邮箱地址的数据和过期的id
    def update_all(self):
        tmp_data = {}
        data = self.query_all()
        current_date = datetime.date.today()
        for subscriber_id in data:
            if data[subscriber_id]["mail"] == "no mail address":
                self.delete(subscriber_id)
                tmp_data[subscriber_id] = data[subscriber_id]
                continue
            subscription_date = data[subscriber_id]["subscription_date"]
            tmp = (int(subscription_date.split('-')[0]) - current_date.year) * 12 * 30 + (int(subscription_date.split('-')[1]) - current_date.month) * 30 + (int(subscription_date.split('-')[2]) - current_date.day)
            if tmp <= 0:
                self.delete(subscriber_id)
                tmp_data[subscriber_id] = data[subscriber_id]

        return tmp_data
        
    def close(self):
        self.cursor.close()
        self.cnx.close()

# 随机生成订阅者信息
def RandomSubscriptionData():
    # 随机生成，字母大小写数字的组合
    subscriber_id = ''.join(np.random.choice(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"), 50))
    current_date = datetime.date.today()
    subscription_date = f"{current_date.year:04}-{current_date.month + 1:02}-{current_date.day:02}"

    return subscriber_id, subscription_date
        
        
if __name__ == "__main__":
    subscription_service = SubscriptionService()
    # subscription_service.subscribe("123")
    # subscription_service.calculate_billing("123")
    # subscription_service.check_subscribers("123")
    mysql_operation = MysqlOperation()
    # mysql_operation.create_table()
    # mysql_operation.insert("123", "2024-02-18")
    mysql_operation.query("123")
    mysql_operation.update("123", "2024-03-19")
    mysql_operation.query("123")
    # mysql_operation.query("123")
    # mysql_operation.delete("123")
    mysql_operation.close()
