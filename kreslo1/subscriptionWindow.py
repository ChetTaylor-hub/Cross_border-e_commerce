import numpy as np
import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QMessageBox
from subscriptionService import MysqlOperation, RandomSubscriptionData



# 用于显示订阅者信息的窗口，包括订阅者id和订阅日期，还可以随机生成订阅者信息，并插入到mysql中，还可以删除订阅者信息，刷新订阅者信息
class SubscriptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mysql_operation = MysqlOperation(table_name="test2")
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("订阅者信息")
        self.setGeometry(300, 300, 300, 300)
        
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        self.random_button = QPushButton("随机生成订阅者信息")
        self.random_button.clicked.connect(self.random_insert)
        self.layout.addWidget(self.random_button)
        
        self.query_all_button = QPushButton("查询所有订阅者信息")
        self.query_all_button.clicked.connect(self.query_all)
        self.layout.addWidget(self.query_all_button)

        self.update_button = QPushButton("更新数据库数据")
        self.update_button.clicked.connect(self.update)
        self.layout.addWidget(self.update_button)

        self.subscriber_id_label = QLabel("订阅者id")
        self.subscriber_id_line = QLineEdit()
        self.layout.addWidget(self.subscriber_id_label)
        self.layout.addWidget(self.subscriber_id_line)

        self.query_button = QPushButton("查询订阅者信息")
        self.query_button.clicked.connect(self.query)
        self.layout.addWidget(self.query_button)
        
        self.delete_button = QPushButton("删除订阅者信息")
        self.delete_button.clicked.connect(self.delete)
        self.layout.addWidget(self.delete_button)

        self.subscriber_data_label = QLabel("订阅截至日期（例如：2024-02-18），如果为空则默认为当前日期的下一个月")
        self.subscriber_data_line = QLineEdit()
        self.layout.addWidget(self.subscriber_data_label)
        self.layout.addWidget(self.subscriber_data_line)
        
        self.subscriber_mail_label = QLabel("填入邮箱地址")
        self.subscriber_mail_line = QLineEdit()
        self.layout.addWidget(self.subscriber_mail_label)
        self.layout.addWidget(self.subscriber_mail_line)

        self.refresh_button = QPushButton("更新订阅者信息")
        self.refresh_button.clicked.connect(self.refresh)
        self.layout.addWidget(self.refresh_button)

        self.subscription_result_label = QLabel("运行结果")
        self.subscription_result_line = QTextEdit()
        self.layout.addWidget(self.subscription_result_label)
        self.layout.addWidget(self.subscription_result_line)
        
    # 随机生成订阅者信息，并插入到mysql中
    def random_insert(self):
        subscriber_id, subscription_date = RandomSubscriptionData()
        subscriber_mail = "no mail address"
        if self.is_exist(subscriber_id):
            self.subscription_result_line.setText(f"订阅ID：{subscriber_id} 已经存在，请重新点击：随机生成订阅者信息按钮")
            return
        self.mysql_operation.insert(subscriber_id, subscriber_mail, subscription_date)
        self.subscription_result_line.setText(f"随机生成订阅者信息成功，订阅ID：{subscriber_id}，订阅日期: {subscription_date}, 邮箱地址：{subscriber_mail}")
    
    # 删除订阅者信息
    def delete(self):
        subscriber_id = self.subscriber_id_line.text()
        if not self.is_exist(subscriber_id):
            self.subscription_result_line.setText(f"订阅ID：{subscriber_id} 不存在，请重新输入")
            return
        self.mysql_operation.delete(subscriber_id)
        self.subscription_result_line.setText(f"删除订阅者信息成功，订阅ID：{subscriber_id}")


    # 判断订阅者id是否存在，并显示在订阅日期栏中
    def is_exist(self, subscriber_id):
        data = self.mysql_operation.query(subscriber_id)
        if not data:
            return False
        return True
    
    # 刷新订阅者的日期信息
    def refresh(self):
        subscriber_id = self.subscriber_id_line.text()
        subscriber_data = self.subscriber_data_line.text()
        subscriber_mail = self.subscriber_mail_line.text()
        if not self.is_exist(subscriber_id):
            return

        if not subscriber_data:
            current_date = datetime.date.today()
            subscriber_data = f"{current_date.year:04}-{current_date.month + 1:02}-{current_date.day:02}"
        self.mysql_operation.update(subscriber_id, subscriber_mail, subscriber_data)
        self.subscriber_id_line.setText(subscriber_id)
        self.subscription_result_line.setText(f"刷新成功，订阅ID：{subscriber_id}，订阅日期: {subscriber_data}，邮箱地址：{subscriber_mail}")

    # g更新数据库数据，去除没有邮箱地址的数据和过期的id
    def update(self):
        data = self.mysql_operation.update_all()
        tmp_str = "更新数据库数据成功，以下数据被删除：\n"
        for subscriber_id in data:
            tmp_str += f"订阅ID：{subscriber_id}，订阅日期: {data[subscriber_id]['subscription_date']}，邮箱地址：{data[subscriber_id]['mail']}\n"

        self.subscription_result_line.setText(tmp_str)

    # 查询所有订阅者信息
    def query_all(self):
        tmp = "所有订阅者信息（没有显示邮箱地址的 id 还未使用）：\n"
        data = self.mysql_operation.query_all()
        # 遍历data{}，显示所有订阅者信息
        for subscriber_id in data:
            tmp += f"订阅ID：{subscriber_id}，订阅日期: {data[subscriber_id]['subscription_date']}，邮箱地址：{data[subscriber_id]['mail']}\n"
        
        self.subscription_result_line.setText(tmp)

    # 查询订阅者信息
    def query(self):
        subscriber_id = self.subscriber_id_line.text()
        if not self.is_exist(subscriber_id):
            self.subscription_result_line.setText(f"订阅ID：{subscriber_id} 不存在，请重新输入")
            return
        data = self.mysql_operation.query(subscriber_id)
        self.subscription_result_line.setText(f"订阅ID：{subscriber_id}，订阅日期: {data[subscriber_id]['subscription_date']}，邮箱地址：{data[subscriber_id]['mail']}")

    # 点击成功槽函数
    def show_success_message(self):
        QMessageBox.information(self, "成功", "点击成功")

    def closeEvent(self, event):
        self.mysql_operation.close()
        event.accept()

        
if __name__ == "__main__":
    app = QApplication([])
    window = SubscriptionWindow()
    window.show()
    app.exec_()


