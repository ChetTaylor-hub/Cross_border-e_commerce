import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QGroupBox, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt 

from passport import register_passport
from complaint import complaintsAndSales

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

        # 创建标签
        self.collect_money_result_label = QLabel("结果将显示在这里")
        self.fill_passport_result_label = QLabel("结果将显示在这里")
        self.file_complaint_result_label = QLabel("结果将显示在这里")

        # 创建按钮
        self.start_collect_money_button = QPushButton("开始")
        self.stop_collect_money_button = QPushButton("停止")
        self.start_fill_passport_button = QPushButton("开始")
        self.stop_fill_passport_button = QPushButton("停止")
        self.start_file_complaint_button = QPushButton("开始")
        self.stop_file_complaint_button = QPushButton("停止")

        # 创建延时输入框，当没有输入时显示《请输入发送间隔》，当输入时显示输入的数字
        self.collect_money_delay = QLineEdit()
        self.collect_money_delay.setPlaceholderText("请输入发送间隔")
        self.fill_passport_delay = QLineEdit()
        self.fill_passport_delay.setPlaceholderText("请输入发送间隔")
        self.file_complaint_delay = QLineEdit()
        self.file_complaint_delay.setPlaceholderText("请输入发送间隔")

        # 确认按钮
        self.collect_money_info_confirm_button = QPushButton("确认")
        self.fill_passport_info_confirm_button = QPushButton("确认")
        self.file_complaint_info_confirm_button = QPushButton("确认")


        # 设置布局
        self.setup_layout()

        # 连接按钮与函数
        self.start_collect_money_button.clicked.connect(self.start_collect_money)
        self.stop_collect_money_button.clicked.connect(self.stop_collect_money)
        self.start_fill_passport_button.clicked.connect(self.start_fill_passport)
        self.stop_fill_passport_button.clicked.connect(self.stop_fill_passport)
        self.start_file_complaint_button.clicked.connect(self.start_file_complaint)
        self.stop_file_complaint_button.clicked.connect(self.stop_file_complaint)
        
        self.collect_money_info_confirm_button.clicked.connect(self.collect_money_info_confirm_input)
        self.fill_passport_info_confirm_button.clicked.connect(self.fill_passport_info_confirm_input)
        self.file_complaint_info_confirm_button.clicked.connect(self.file_complaint_info_confirm_input)

        # 连接按钮到《点击成功槽函数》
        self.start_collect_money_button.clicked.connect(self.show_success_message)
        self.stop_collect_money_button.clicked.connect(self.show_success_message)
        self.start_fill_passport_button.clicked.connect(self.show_success_message)
        self.stop_fill_passport_button.clicked.connect(self.show_success_message)
        self.start_file_complaint_button.clicked.connect(self.show_success_message)
        self.stop_file_complaint_button.clicked.connect(self.show_success_message)
        self.collect_money_info_confirm_button.clicked.connect(self.show_success_message)
        self.fill_passport_info_confirm_button.clicked.connect(self.show_success_message)
        self.file_complaint_info_confirm_button.clicked.connect(self.show_success_message)

        # 添加一个确认按钮，将上面信息确认后，在进行线程初始化


        # 初始化线程对象
        # self.collect_money_thread = WorkerThread(collect_money, self.ClientId_input.text(), self.ApiKey_input.text())
        # self.fill_passport_thread = WorkerThread(fill_passport, self.ClientId_input.text(), self.ApiKey_input.text())
        # self.file_complaint_thread = WorkerThread(file_complaint, self.ClientId_input.text(), self.ApiKey_input.text())

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

        # 添加任务到主布局
        main_layout.addWidget(self.ClientId_input)
        main_layout.addWidget(self.ApiKey_input)
        main_layout.addWidget(self.collect_money_group)
        main_layout.addWidget(self.fill_passport_group)
        main_layout.addWidget(self.file_complaint_group)
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

        # 释放线程对象，重新创建
        self.file_complaint_thread = None
        if not self.file_complaint_thread:
            self.file_complaint_thread = WorkerThread(file_complaint, client_id, api_key, file_complaint_delay)

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
    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    register_passport(headers, delay)
    print("执行催收操作")
    return f"执行催收操"

def fill_passport(*args, **kwarg):
    # 实现填写护照功能的函数，使用传递的参数

    print("执行填写护照操作")
    return f"执行填写护照操"

def file_complaint(*args, **kwarg):
    # 实现投诉功能的函数，使用传递的参数
    headers = {
        "Client-Id": args[0],
        "Api-Key": args[1]
    }
    delay = args[2]
    complaintsAndSales(headers, delay)
    print("执行投诉操作")
    return f"执行投诉操作"

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
