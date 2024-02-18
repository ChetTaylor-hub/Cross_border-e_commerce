import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QGroupBox, QMessageBox, QFileDialog, QTabWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt 

from passport import register_passport
from complaint import complaintsAndSales
from pickup import urgePickUp
from promotional import deleteAPromotionalItem
from update import updateProductInventory

from spider import SpiderShop

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

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置主窗口标题
        self.setWindowTitle("任务处理界面")

        # 设置主窗口大小
        self.resize(1000, 200)

        # 创建密匙元素
        self.ClientId_input = QLineEdit()  # 用于输入参数的文本框
        self.ClientId_input.setPlaceholderText("请输入 ClientId")
        self.ApiKey_input = QLineEdit()
        self.ApiKey_input.setPlaceholderText("请输入 ApiKey")

        self.init_task_name()

        # 创建GroupBoxes
        self.collect_money_group = QGroupBox(self.collect_money_name)
        self.fill_passport_group = QGroupBox(self.fill_passport_name)
        self.file_complaint_group = QGroupBox(self.file_complaint_name)
        self.delete_promotional_item = QGroupBox(self.delete_promotional_item_name)
        self.update_product_inventory = QGroupBox(self.update_product_inventory_name)

        # 创建标签
        self.collect_money_result_label = QLabel("结果将显示在这里")
        self.fill_passport_result_label = QLabel("结果将显示在这里")
        self.file_complaint_result_label = QLabel("结果将显示在这里")
        self.delete_promotional_item_result_label = QLabel("结果将显示在这里")
        self.update_product_inventory_result_label = QLabel("结果将显示在这里")

        # 创建按钮
        self.start_collect_money_button = QPushButton("开始")
        self.start_collect_money_button.setEnabled(False)
        self.stop_collect_money_button = QPushButton("停止")
        self.stop_collect_money_button.setEnabled(False)
        self.start_fill_passport_button = QPushButton("开始")
        self.start_fill_passport_button.setEnabled(False)
        self.stop_fill_passport_button = QPushButton("停止")
        self.stop_fill_passport_button.setEnabled(False)
        self.start_file_complaint_button = QPushButton("开始")
        self.start_file_complaint_button.setEnabled(False)
        self.stop_file_complaint_button = QPushButton("停止")
        self.stop_file_complaint_button.setEnabled(False)
        self.start_delete_promotional_item_button = QPushButton("开始")
        self.start_delete_promotional_item_button.setEnabled(False)
        self.stop_delete_promotional_item_button = QPushButton("停止")
        self.stop_delete_promotional_item_button.setEnabled(False)
        self.start_update_product_inventory_button = QPushButton("开始")
        self.start_update_product_inventory_button.setEnabled(False)
        self.stop_update_product_inventory_button = QPushButton("停止")
        self.stop_update_product_inventory_button.setEnabled(False)

        # 创建延时输入框，当没有输入时显示《请输入发送间隔》，当输入时显示输入的数字
        self.collect_money_delay = QLineEdit()
        self.collect_money_delay.setPlaceholderText("请输入发送间隔，单位：s")
        self.fill_passport_delay = QLineEdit()
        self.fill_passport_delay.setPlaceholderText("请输入发送间隔，单位：s")
        self.file_complaint_delay = QLineEdit()
        self.file_complaint_delay.setPlaceholderText("请输入发送间隔，单位：s")
        self.delete_promotional_item_delay = QLineEdit()
        self.delete_promotional_item_delay.setPlaceholderText("请输入发送间隔，单位：s")
        self.update_product_inventory_delay = QLineEdit()
        self.update_product_inventory_delay.setPlaceholderText("请输入发送间隔，单位：s")

        # 确认按钮
        self.collect_money_info_confirm_button = QPushButton("确认")
        self.collect_money_info_confirm_button.setEnabled(False)
        self.fill_passport_info_confirm_button = QPushButton("确认")
        self.fill_passport_info_confirm_button.setEnabled(False)
        self.file_complaint_info_confirm_button = QPushButton("确认")
        self.file_complaint_info_confirm_button.setEnabled(False)
        self.delete_promotional_item_info_confirm_button = QPushButton("确认")
        self.delete_promotional_item_info_confirm_button.setEnabled(False)
        self.update_product_inventory_info_confirm_button = QPushButton("确认")
        self.update_product_inventory_info_confirm_button.setEnabled(False)

        # 选择excel文件按钮
        self.file_name = None
        self.select_excel_button = QPushButton("选择Excel文件")
        self.select_excel_button.clicked.connect(self.select_excel_file)
        # 创建一个文本框来显示选择的文件的路径
        self.excel_file_path_input = QLineEdit()
        self.excel_file_path_input.setPlaceholderText("请先选择Excel文件")

        # 开启浏览器
        self.spider_shop_button = QPushButton("第一次使用，请点击此并登录ozon账号")
        self.spider_shop_button.clicked.connect(self.login_ozon)

        # 手动验证ozon网站
        self.verify_ozon_button = QPushButton("如果投诉任务出现验证界面并且程序无法自动验证，请先停止并点击此，手动验证ozon网站")
        self.verify_ozon_button.clicked.connect(self.verify_ozon)

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

    def init_task_name(self):
        self.collect_money_name = "催收"
        self.fill_passport_name = "填写护照"
        self.file_complaint_name = "投诉"
        self.delete_promotional_item_name = "删除促销商品"
        self.update_product_inventory_name = "更新商品库存"

    def setup_layout_1(self):
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
                                self.file_complaint_delay, self.file_complaint_info_confirm_button,
                                self.spider_shop_button, self.verify_ozon_button)
        
        self.setup_task_layout(self.delete_promotional_item, "删除促销商品", self.delete_promotional_item_result_label,
                                self.start_delete_promotional_item_button, self.stop_delete_promotional_item_button, 
                                self.delete_promotional_item_delay, self.delete_promotional_item_info_confirm_button)
        
        self.setup_task_layout(self.update_product_inventory, "更新商品库存", self.update_product_inventory_result_label,
                                self.start_update_product_inventory_button, self.stop_update_product_inventory_button, 
                                self.update_product_inventory_delay, self.update_product_inventory_info_confirm_button,
                                self.select_excel_button)


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

    def setup_layout(self):
         # 设置每个任务的布局
        self.setup_task_layout(self.collect_money_group, "催收", self.collect_money_result_label,
                                self.start_collect_money_button, self.stop_collect_money_button, 
                                self.collect_money_delay, self.collect_money_info_confirm_button)

        self.setup_task_layout(self.fill_passport_group, "填写护照", self.fill_passport_result_label,
                                self.start_fill_passport_button, self.stop_fill_passport_button, 
                                self.fill_passport_delay, self.fill_passport_info_confirm_button)

        self.setup_task_layout(self.file_complaint_group, "投诉", self.file_complaint_result_label,
                                self.start_file_complaint_button, self.stop_file_complaint_button, 
                                self.file_complaint_delay, self.file_complaint_info_confirm_button,
                                self.spider_shop_button, self.verify_ozon_button)
        
        self.setup_task_layout(self.delete_promotional_item, "删除促销商品", self.delete_promotional_item_result_label,
                                self.start_delete_promotional_item_button, self.stop_delete_promotional_item_button, 
                                self.delete_promotional_item_delay, self.delete_promotional_item_info_confirm_button)
        
        self.setup_task_layout(self.update_product_inventory, "更新商品库存", self.update_product_inventory_result_label,
                                self.start_update_product_inventory_button, self.stop_update_product_inventory_button, 
                                self.update_product_inventory_delay, self.update_product_inventory_info_confirm_button,
                                self.select_excel_button, self.excel_file_path_input)
        
        # 当密钥信息和延迟被填写时，将按钮设置为启用状态
        self.ApiKey_input.textChanged.connect(self.check_input)
        self.collect_money_delay.textChanged.connect(self.check_input)
        self.fill_passport_delay.textChanged.connect(self.check_input)
        self.file_complaint_delay.textChanged.connect(self.check_input)
        self.delete_promotional_item_delay.textChanged.connect(self.check_input)
        self.update_product_inventory_delay.textChanged.connect(self.check_input)
        self.excel_file_path_input.textChanged.connect(self.check_input)

        # 设置主布局
        main_layout = QVBoxLayout()

        # 创建一个标签页部件
        tab_widget = QTabWidget()

        # 创建标签页，并将窗口部件添加到标签页
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(self.ClientId_input)
        tab1_layout.addWidget(self.ApiKey_input)
        tab_widget.addTab(tab1, "密匙信息")

        collect_money_tab = QWidget()
        collect_money_tab_layout = QVBoxLayout(collect_money_tab)
        collect_money_tab_layout.addWidget(self.collect_money_group)
        tab_widget.addTab(collect_money_tab, "催收任务")

        fill_passport_tab = QWidget()
        fill_passport_tab_layout = QVBoxLayout(fill_passport_tab)
        fill_passport_tab_layout.addWidget(self.fill_passport_group)
        tab_widget.addTab(fill_passport_tab, "填写护照任务")

        file_complaint_tab = QWidget()
        file_complaint_tab_layout = QVBoxLayout(file_complaint_tab)
        file_complaint_tab_layout.addWidget(self.file_complaint_group)
        tab_widget.addTab(file_complaint_tab, "投诉任务")

        delete_promotional_item_tab = QWidget()
        delete_promotional_item_tab_layout = QVBoxLayout(delete_promotional_item_tab)
        delete_promotional_item_tab_layout.addWidget(self.delete_promotional_item)
        tab_widget.addTab(delete_promotional_item_tab, "删除促销商品")

        update_product_inventory_tab = QWidget()
        update_product_inventory_tab_layout = QVBoxLayout(update_product_inventory_tab)
        update_product_inventory_tab_layout.addWidget(self.update_product_inventory)
        tab_widget.addTab(update_product_inventory_tab, "更新商品库存")

        # 将标签页部件添加到主布局
        main_layout.addWidget(tab_widget)

        # 设置主窗口中央的 Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_task_layout(self, group_box, task_name, result_label, start_button, stop_button, delay_label, info_confirm_button, *args):
        # 设置任务布局
        task_layout = QVBoxLayout()

        # 设置结果标签的样式
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("QLabel { background-color : #E0E0E0; padding: 5px; }")

        # 添加任务元素到任务布局
        if delay_label:
            task_layout.addWidget(delay_label)

        # 添加额外的元素到任务布局
        for arg in args:
            task_layout.addWidget(arg)

        if info_confirm_button:
            task_layout.addWidget(info_confirm_button)
        if start_button:
            task_layout.addWidget(start_button)
        if stop_button:
            task_layout.addWidget(stop_button)
        if result_label:
            task_layout.addWidget(result_label)

        # 设置任务GroupBox的布局
        group_box.setLayout(task_layout)
    
    # 点击成功槽函数
    def show_success_message(self):
        QMessageBox.information(self, "成功", "操作成功")

    def check_input(self):
        # 检查密钥信息和各个任务的延迟是否已经填写吗，如果填写了，就启用相应任务的确认按钮
        if (self.ApiKey_input.text() and self.ClientId_input.text()) and self.collect_money_delay.text():
            self.collect_money_info_confirm_button.setEnabled(True)
        else:
            self.collect_money_info_confirm_button.setEnabled(False)
            self.start_collect_money_button.setEnabled(False)
            self.stop_collect_money_button.setEnabled(False)

        if (self.ApiKey_input.text() and self.ClientId_input.text()) and self.fill_passport_delay.text():
            self.fill_passport_info_confirm_button.setEnabled(True)
        else:
            self.fill_passport_info_confirm_button.setEnabled(False)
            self.start_fill_passport_button.setEnabled(False)
            self.stop_fill_passport_button.setEnabled(False)

        if (self.ApiKey_input.text() and self.ClientId_input.text()) and self.file_complaint_delay.text():
            self.file_complaint_info_confirm_button.setEnabled(True)
        else:
            self.file_complaint_info_confirm_button.setEnabled(False)
            self.start_file_complaint_button.setEnabled(False)
            self.stop_file_complaint_button.setEnabled(False)

        if (self.ApiKey_input.text() and self.ClientId_input.text()) and self.delete_promotional_item_delay.text():
            self.delete_promotional_item_info_confirm_button.setEnabled(True)
        else:
            self.delete_promotional_item_info_confirm_button.setEnabled(False)
            self.start_delete_promotional_item_button.setEnabled(False)
            self.stop_delete_promotional_item_button.setEnabled(False)

        if (self.ApiKey_input.text() and self.ClientId_input.text()) and self.update_product_inventory_delay.text():
            self.select_excel_button.setEnabled(True)
            if self.excel_file_path_input.text():
                self.update_product_inventory_info_confirm_button.setEnabled(True)
            else:
                self.update_product_inventory_info_confirm_button.setEnabled(False)
                self.start_update_product_inventory_button.setEnabled(False)
                self.stop_update_product_inventory_button.setEnabled(False)
        else:
            self.select_excel_button.setEnabled(False)
            self.update_product_inventory_info_confirm_button.setEnabled(False)
            self.start_update_product_inventory_button.setEnabled(False)
            self.stop_update_product_inventory_button.setEnabled(False)

    # 添加一个新的函数来处理按钮点击事件
    def select_excel_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xls *.xlsx)")
        if file_name:
            self.file_name = file_name
            self.excel_file_path_input.setText(file_name)

    # 登录ozon网站
    def login_ozon(self):
        SpiderShop.login_ozon()

    # 验证ozon网站
    def verify_ozon(self):
        SpiderShop.verify_ozon()

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
        # 点击确认按钮后，开启开始停止按钮
        self.start_collect_money_button.setEnabled(True)
        self.stop_collect_money_button.setEnabled(True)

        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        collect_money_delay = self.collect_money_delay.text()

        self.collect_money_thread = None
        if not self.collect_money_thread:
            self.collect_money_thread = WorkerThread(collect_money, client_id, api_key, collect_money_delay)

    def fill_passport_info_confirm_input(self):
        # 点击确认按钮后，开启开始停止按钮
        self.start_fill_passport_button.setEnabled(True)
        self.stop_fill_passport_button.setEnabled(True)

        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        fill_passport_delay = self.fill_passport_delay.text()

        self.fill_passport_thread = None
        if not self.fill_passport_thread:
            self.fill_passport_thread = WorkerThread(fill_passport, client_id, api_key, fill_passport_delay)

    def file_complaint_info_confirm_input(self):
        # 点击确认按钮后，开启开始停止按钮
        self.start_file_complaint_button.setEnabled(True)
        self.stop_file_complaint_button.setEnabled(True)

        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        file_complaint_delay = self.file_complaint_delay.text()

        self.file_complaint_thread = None
        if not self.file_complaint_thread:
            self.file_complaint_thread = WorkerThread(file_complaint, client_id, api_key, file_complaint_delay)

    def delete_promotional_item_info_confirm_input(self):
        # 点击确认按钮后，开启开始停止按钮
        self.start_delete_promotional_item_button.setEnabled(True)
        self.stop_delete_promotional_item_button.setEnabled(True)

        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        delete_promotional_item_delay = self.delete_promotional_item_delay.text()

        self.delete_promotional_item_thread = None
        if not self.delete_promotional_item_thread:
            self.delete_promotional_item_thread = WorkerThread(delete_promotional_item, client_id, api_key, delete_promotional_item_delay)

    def update_product_inventory_info_confirm_input(self):
        # 点击确认按钮后，开启开始停止按钮
        self.start_update_product_inventory_button.setEnabled(True)
        self.stop_update_product_inventory_button.setEnabled(True)

        client_id = self.ClientId_input.text()
        api_key = self.ApiKey_input.text()
        update_product_inventory_delay = self.update_product_inventory_delay.text()

        self.update_product_inventory_thread = None
        if not self.update_product_inventory_thread:
            self.update_product_inventory_thread = WorkerThread(update_product_inventory, client_id, api_key, update_product_inventory_delay, self.file_name)

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
        if thread.isRunning():
            thread.running = False
            # 停止任务线程
            # thread.stop()
            # thread.wait()

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
    return f"运行失败，输入的参数有误，重新点击停止->重新填写参数->确认->开始"

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
    return f"运行失败，输入的参数有误，重新点击停止->重新填写参数->确认->开始"

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
    return f"运行失败，输入的参数有误，重新点击停止->重新填写参数->确认->开始"

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
    return f"运行失败，输入的参数有误，重新点击停止->重新填写参数->确认->开始"

def update_product_inventory(*args, **kwarg):
    # 实现更新商品库存功能的函数，使用传递的参数
    res = False

    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    excel = args[3]
    res = updateProductInventory(headers, delay, excel)
    print("执行更新商品库存操作")
    if res:
        return f"运行成功，可以点击停止暂停，暂停后点击开始继续，如果想要修改配置，请先点击停止，修改相应参数后点击确认在点击开始"
    return f"运行失败，输入的参数有误，重新点击停止->重新填写参数->确认->开始"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
