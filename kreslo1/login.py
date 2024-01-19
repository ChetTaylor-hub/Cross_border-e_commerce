import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from Windows import MainWindow

from ozon_Api import OzonApi

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # 设置主窗口标题
        self.setWindowTitle("登录界面")

        # 创建界面元素
        self.client_id_label = QLabel("Client-ID:")
        self.client_id_line_edit = QLineEdit()

        self.api_key_label = QLabel("API-Key:")
        self.api_key_line_edit = QLineEdit()

        self.login_button = QPushButton("登录")

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.client_id_label)
        layout.addWidget(self.client_id_line_edit)
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_line_edit)
        layout.addWidget(self.login_button)

        # 设置主窗口中央的 Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 连接按钮与登录函数
        self.login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        client_id = self.client_id_line_edit.text()
        api_key = self.api_key_line_edit.text()

        # 调用你提供的验证函数
        # TODO: validate_login 函数需要你自己实现
        if self.validate_login(client_id, api_key):
            # 验证成功，进入主界面
            self.close()  # 关闭登录窗口
            main_window = MainWindow()
            main_window.show()
        else:
            # 验证失败，显示错误消息
            error_label = QLabel("登录失败，请检查Client-ID和API-Key")
            error_label.setStyleSheet("color: red")
            self.layout().addWidget(error_label)

    def validate_login(self, client_id, api_key):
        headers = {"Client-Id": client_id, "Api-Key": api_key}
        ozon = OzonApi(headers)
        try:
            if ozon.ShipmentList():
                return True
            else:
                return False
        except KeyError:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
