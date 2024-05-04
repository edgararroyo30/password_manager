import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QListWidget, QAction
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWinExtras import QtWin


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List - Modern Look")
        self.setGeometry(100, 100, 400, 500)  # Set window position and size

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a label for the title
        title_label = QLabel("To-Do List")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Create a text field for adding tasks
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task")
        self.task_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.task_input)

        # Create a button for adding tasks
        add_button = QPushButton("Add Task")
        add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        # Create a list widget to display tasks
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Create a menu bar
        self.menu_bar = self.menuBar()
        self.theme_menu = self.menu_bar.addMenu('Theme')

        # Add toggle action to the theme menu
        self.toggle_action = QAction('Toggle Dark Mode', self)
        self.toggle_action.triggered.connect(self.toggle_theme)
        self.theme_menu.addAction(self.toggle_action)

        # Initialize dark mode flag
        self.dark_mode = False

    def add_task(self):
        task_text = self.task_input.text()
        if task_text:
            self.task_list.addItem(task_text)
            self.task_input.clear()

    def toggle_theme(self):
        # Toggle between light and dark mode
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    def set_dark_mode(self):
        # Set dark color palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

        # Update menu item text
        self.toggle_action.setText('Toggle Light Mode')

    def set_light_mode(self):
        # Reset to default color palette
        self.setPalette(QPalette())

        # Update menu item text
        self.toggle_action.setText('Toggle Dark Mode')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
