import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QGroupBox, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt 

from passport import register_passport
from complaint import complaintsAndSales
from pickup import urgePickUp
from promotional import deleteAPromotionalItem
from update import updateProductInventory

class WorkerThread(QThread):
    task_completed = pyqtSignal(str)

    def __init__(self, task_function, *args, **kwargs):
        super(WorkerThread, self).__init__()
        self.task_function = task_function
        self.args = args
        self.kwargs = kwargs
        self.running = False  # 控制线程运行的标志位

    def run(self):
        while self.running:
            result = self.task_function(*self.args, **self.kwargs)
            self.task_completed.emit(result)

            time.sleep(1)  # 模拟任务执行，每隔1秒发送一次结果

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置主窗口标题
        self.setWindowTitle("任务处理界面")

        # 设置主窗口大小
        self.resize(1000, 1000)

        # 创建密匙元素
        self.ClientId_input = QLineEdit()  # 用于输入参数的文本框
        self.ClientId_input.setPlaceholderText("请输入 ClientId")
        self.ApiKey_input = QLineEdit()
        self.ApiKey_input.setPlaceholderText("请输入 ApiKey")

        # 创建GroupBoxes
        self.collect_money_group = QGroupBox("催收任务")
        self.fill_passport_group = QGroupBox("填写护照任务")
        self.file_complaint_group = QGroupBox("投诉任务")
        self.delete_promotional_item = QGroupBox("删除促销商品")
        self.update_product_inventory = QGroupBox("更新商品库存")

        # 创建标签
        self.collect_money_result_label = QLabel("结果将显示在这里")
        self.fill_passport_result_label = QLabel("结果将显示在这里")
        self.file_complaint_result_label = QLabel("结果将显示在这里")
        self.delete_promotional_item_result_label = QLabel("结果将显示在这里")
        self.update_product_inventory_result_label = QLabel("结果将显示在这里")

        # 创建按钮
        self.start_collect_money_button = QPushButton("开始")
        self.stop_collect_money_button = QPushButton("停止")
        self.start_fill_passport_button = QPushButton("开始")
        self.stop_fill_passport_button = QPushButton("停止")
        self.start_file_complaint_button = QPushButton("开始")
        self.stop_file_complaint_button = QPushButton("停止")
        self.start_delete_promotional_item_button = QPushButton("开始")
        self.stop_delete_promotional_item_button = QPushButton("停止")
        self.start_update_product_inventory_button = QPushButton("开始")
        self.stop_update_product_inventory_button = QPushButton("停止")

        # 创建延时输入框，当没有输入时显示《请输入发送间隔》，当输入时显示输入的数字
        self.collect_money_delay = QLineEdit()
        self.collect_money_delay.setPlaceholderText("请输入发送间隔")
        self.fill_passport_delay = QLineEdit()
        self.fill_passport_delay.setPlaceholderText("请输入发送间隔")
        self.file_complaint_delay = QLineEdit()
        self.file_complaint_delay.setPlaceholderText("请输入发送间隔")
        self.delete_promotional_item_delay = QLineEdit()
        self.delete_promotional_item_delay.setPlaceholderText("请输入发送间隔")
        self.update_product_inventory_delay = QLineEdit()
        self.update_product_inventory_delay.setPlaceholderText("请输入发送间隔")

        # 确认按钮
        self.collect_money_info_confirm_button = QPushButton("确认")
        self.fill_passport_info_confirm_button = QPushButton("确认")
        self.file_complaint_info_confirm_button = QPushButton("确认")
        self.delete_promotional_item_info_confirm_button = QPushButton("确认")
        self.update_product_inventory_info_confirm_button = QPushButton("确认")

        # 重置按钮
        self.init_button = QPushButton("重置")

        # 设置布局
        self.setup_layout()

        # 连接按钮与指定的函数
        self.start_collect_money_button.clicked.connect(self.start_collect_money)
        self.stop_collect_money_button.clicked.connect(self.stop_collect_money)
        self.start_fill_passport_button.clicked.connect(self.start_fill_passport)
        self.stop_fill_passport_button.clicked.connect(self.stop_fill_passport)
        self.start_file_complaint_button.clicked.connect(self.start_file_complaint)
        self.stop_file_complaint_button.clicked.connect(self.stop_file_complaint)
        self.start_delete_promotional_item_button.clicked.connect(self.start_delete_promotional_item)
        self.stop_delete_promotional_item_button.clicked.connect(self.stop_delete_promotional_item)
        self.start_update_product_inventory_button.clicked.connect(self.start_update_product_inventory)
        self.stop_update_product_inventory_button.clicked.connect(self.stop_update_product_inventory)

        
        self.collect_money_info_confirm_button.clicked.connect(self.collect_money_info_confirm_input)
        self.fill_passport_info_confirm_button.clicked.connect(self.fill_passport_info_confirm_input)
        self.file_complaint_info_confirm_button.clicked.connect(self.file_complaint_info_confirm_input)
        self.delete_promotional_item_info_confirm_button.clicked.connect(self.delete_promotional_item_info_confirm_input)
        self.update_product_inventory_info_confirm_button.clicked.connect(self.update_product_inventory_info_confirm_input)

        # 连接按钮到《点击成功槽函数》
        self.start_collect_money_button.clicked.connect(self.show_success_message)
        self.stop_collect_money_button.clicked.connect(self.show_success_message)
        self.start_fill_passport_button.clicked.connect(self.show_success_message)
        self.stop_fill_passport_button.clicked.connect(self.show_success_message)
        self.start_file_complaint_button.clicked.connect(self.show_success_message)
        self.stop_file_complaint_button.clicked.connect(self.show_success_message)
        self.start_delete_promotional_item_button.clicked.connect(self.show_success_message)
        self.stop_delete_promotional_item_button.clicked.connect(self.show_success_message)
        self.start_update_product_inventory_button.clicked.connect(self.show_success_message)
        self.stop_update_product_inventory_button.clicked.connect(self.show_success_message)

        # 确认按钮链接到《点击成功槽函数》
        self.collect_money_info_confirm_button.clicked.connect(self.show_success_message)
        self.fill_passport_info_confirm_button.clicked.connect(self.show_success_message)
        self.file_complaint_info_confirm_button.clicked.connect(self.show_success_message)
        self.delete_promotional_item_info_confirm_button.clicked.connect(self.show_success_message)
        self.update_product_inventory_info_confirm_button.clicked.connect(self.show_success_message)
        

        # 连接重置按钮有
        self.init_button.clicked.connect(self.init)
        # 添加一个确认按钮，将上面信息确认后，在进行线程初始化

        # 初始化线程对象
        self.collect_money_thread = WorkerThread(collect_money, self.ClientId_input.text(), self.ApiKey_input.text())
        self.fill_passport_thread = WorkerThread(fill_passport, self.ClientId_input.text(), self.ApiKey_input.text())
        self.file_complaint_thread = WorkerThread(file_complaint, self.ClientId_input.text(), self.ApiKey_input.text())
        self.delete_promotional_item_thread = WorkerThread(delete_promotional_item, self.ClientId_input.text(), self.ApiKey_input.text())
        self.update_product_inventory_thread = WorkerThread(update_product_inventory, self.ClientId_input.text(), self.ApiKey_input.text())

    def setup_layout(self):
        # 设置主布局
        main_layout = QVBoxLayout()

        # 设置每个任务的布局
        self.setup_task_layout(self.collect_money_group, "催收", self.collect_money_result_label,
                                self.start_collect_money_button, self.stop_collect_money_button, 
                                self.collect_money_delay, self.collect_money_info_confirm_button)

        self.setup_task_layout(self.fill_passport_group, "填写护照", self.fill_passport_result_label,
                                self.start_fill_passport_button, self.stop_fill_passport_button, 
                                self.fill_passport_delay, self.fill_passport_info_confirm_button)

        self.setup_task_layout(self.file_complaint_group, "投诉", self.file_complaint_result_label,
                                self.start_file_complaint_button, self.stop_file_complaint_button, 
                                self.file_complaint_delay, self.file_complaint_info_confirm_button)
        
        self.setup_task_layout(self.delete_promotional_item, "删除促销商品", self.delete_promotional_item_result_label,
                                self.start_delete_promotional_item_button, self.stop_delete_promotional_item_button, 
                                self.delete_promotional_item_delay, self.delete_promotional_item_info_confirm_button)
        
        self.setup_task_layout(self.update_product_inventory, "更新商品库存", self.update_product_inventory_result_label,
                                self.start_update_product_inventory_button, self.stop_update_product_inventory_button, 
                                self.update_product_inventory_delay, self.update_product_inventory_info_confirm_button)

        # 添加任务到主布局
        main_layout.addWidget(self.ClientId_input)
        main_layout.addWidget(self.ApiKey_input)
        main_layout.addWidget(self.collect_money_group)
        main_layout.addWidget(self.fill_passport_group)
        main_layout.addWidget(self.file_complaint_group)
        main_layout.addWidget(self.delete_promotional_item)
        main_layout.addWidget(self.update_product_inventory)
        main_layout.addWidget(self.init_button)
        # main_layout.addWidget(self.confirm_button)

        # 设置主窗口中央的 Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_task_layout(self, group_box, task_name, result_label, start_button, stop_button, delay_label, info_confirm_button):
        # 设置任务布局
        task_layout = QVBoxLayout()

        # 设置结果标签的样式
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("QLabel { background-color : #E0E0E0; padding: 5px; }")

        # 添加任务元素到任务布局
        task_layout.addWidget(start_button)
        task_layout.addWidget(stop_button)
        task_layout.addWidget(delay_label)
        task_layout.addWidget(info_confirm_button)
        task_layout.addWidget(result_label)

        # 设置任务GroupBox的布局
        group_box.setLayout(task_layout)

    # 确认点击成功槽函数
    def show_success_message(self):
        QMessageBox.information(self, "成功", "点击成功！")

    def init(self):
        self.collect_money_thread.stop()
        self.collect_money_thread = None
        self.file_complaint_thread.stop()
        self.file_complaint_thread = None
        self.fill_passport_thread.stop()
        self.fill_passport_thread = None
        self.delete_promotional_item_thread.stop()
        self.delete_promotional_item_thread = None

    def collect_money_info_confirm_input(self):
        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        collect_money_delay = self.collect_money_delay.text()

        self.collect_money_thread = None
        if not self.collect_money_thread:
            self.collect_money_thread = WorkerThread(collect_money, client_id, api_key, collect_money_delay)

    def fill_passport_info_confirm_input(self):
        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        fill_passport_delay = self.fill_passport_delay.text()

        self.fill_passport_thread = None
        if not self.fill_passport_thread:
            self.fill_passport_thread = WorkerThread(fill_passport, client_id, api_key, fill_passport_delay)

    def file_complaint_info_confirm_input(self):
        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        file_complaint_delay = self.file_complaint_delay.text()

        self.file_complaint_thread = None
        if not self.file_complaint_thread:
            self.file_complaint_thread = WorkerThread(file_complaint, client_id, api_key, file_complaint_delay)

    def delete_promotional_item_info_confirm_input(self):
        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        delete_promotional_item_delay = self.delete_promotional_item_delay.text()

        self.delete_promotional_item_thread = None
        if not self.delete_promotional_item_thread:
            self.delete_promotional_item_thread = WorkerThread(delete_promotional_item, client_id, api_key, delete_promotional_item_delay)

    def update_product_inventory_info_confirm_input(self):
        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        update_product_inventory_delay = self.update_product_inventory_delay.text()

        self.update_product_inventory_thread = None
        if not self.update_product_inventory_thread:
            self.update_product_inventory_thread = WorkerThread(update_product_inventory, client_id, api_key, update_product_inventory_delay)

    def start_collect_money(self):
        self.start_task(self.collect_money_thread, self.collect_money_result_label)

    def stop_collect_money(self):
        self.stop_task(self.collect_money_thread)

    def start_fill_passport(self):
        self.start_task(self.fill_passport_thread, self.fill_passport_result_label)

    def stop_fill_passport(self):
        self.stop_task(self.fill_passport_thread)

    def start_file_complaint(self):
        self.start_task(self.file_complaint_thread, self.file_complaint_result_label)

    def stop_file_complaint(self):
        self.stop_task(self.file_complaint_thread)

    def start_delete_promotional_item(self):
        self.start_task(self.delete_promotional_item_thread, self.delete_promotional_item_result_label)

    def stop_delete_promotional_item(self):
        self.stop_task(self.delete_promotional_item_thread)

    def start_update_product_inventory(self):
        self.start_task(self.update_product_inventory_thread, self.update_product_inventory_result_label)

    def stop_update_product_inventory(self):
        self.stop_task(self.update_product_inventory_thread)

    def start_task(self, thread, result_label):
        # 启动任务线程
        if not thread.isRunning():
            thread.running = True
            thread.task_completed.connect(result_label.setText)
            thread.start()

    def stop_task(self, thread):
        # 停止任务线程
        thread.stop()
        thread.wait()

def collect_money(*args, **kwarg):
    # 实现催收功能的函数，使用传递的参数
    res  = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    res = urgePickUp(headers, delay)
    print("执行催收操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->确认->开始"

def fill_passport(*args, **kwarg):
    # 实现填写护照功能的函数，使用传递的参数
    res = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    res = register_passport(headers, delay)

    print("执行填写护照操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->确认->开始"

def file_complaint(*args, **kwarg):
    # 实现投诉功能的函数，使用传递的参数
    res = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    res = complaintsAndSales(headers, delay)
    print("执行投诉操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->确认->开始"

def delete_promotional_item(*args, **kwarg):
    # 实现删除促销商品功能的函数，使用传递的参数
    res = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    res = deleteAPromotionalItem(headers, delay)
    print("执行删除促销商品操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->确认->开始"

def update_product_inventory(*args, **kwarg):
    # 实现更新商品库存功能的函数，使用传递的参数
    res = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    res = updateProductInventory(headers, delay)
    print("执行更新商品库存操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->确认->开始"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
