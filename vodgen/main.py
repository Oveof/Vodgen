"""Vodgen app"""
import sys
import json
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
    QFileDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget)

class MainWindow(QMainWindow):
    """Main UI window"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lmao")
        layout = QVBoxLayout()

        choose_file = QPushButton("Choose stream file")
        choose_file.clicked.connect(self.choose_file)
        choose_region = QComboBox()
        choose_game = QComboBox()

        #Adds regions form config to dropdown menu
        with open('config.json', encoding="utf-8") as file:
            config = json.load(file)
            for attribute, _ in config["tournament"].items():
                choose_region.addItem(attribute)
            for attribute, _ in config["game"].items():
                choose_game.addItem(attribute)

        only_thumbnails = QCheckBox("Only thumbnails")
        create_videos_button = QPushButton("Generate Video")

        layout.addWidget(choose_region)
        layout.addWidget(choose_game)
        layout.addWidget(choose_file)
        layout.addWidget(only_thumbnails)
        layout.addWidget(create_videos_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def choose_file(self):
        """Choose file helper method"""
        return QFileDialog.getOpenFileName(self, "Select File")
    def choose_dir(self):
        """Choose directory helper method"""
        return QFileDialog.getExistingDirectory(self, "Select Directory")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
