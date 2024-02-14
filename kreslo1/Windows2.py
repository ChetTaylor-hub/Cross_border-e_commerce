import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtWidgets import QApplication

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)

        self.setLayout(self.main_layout)

        self.init_main_page()
        self.init_task_pages()

    def init_main_page(self):
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout()

        self.task_buttons = []
        for i in range(5):
            button = QPushButton(f'Task {i+1}')
            button.clicked.connect(lambda i=i: self.stacked_widget.setCurrentIndex(i+1))
            self.task_buttons.append(button)
            self.main_layout.addWidget(button)

        self.main_page.setLayout(self.main_layout)
        self.stacked_widget.addWidget(self.main_page)

    def init_task_pages(self):
        from PyQt5.QtWidgets import QLabel  # Import the QLabel class

        self.task_pages = []
        for i in range(5):
            page = QWidget()
            layout = QVBoxLayout()

            label = QLabel(f'This is task {i+1}')  # Fix the problem by importing QLabel
            back_button = QPushButton('Back to main page')
            back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

            layout.addWidget(label)
            layout.addWidget(back_button)
            page.setLayout(layout)

            self.task_pages.append(page)
            self.stacked_widget.addWidget(page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())