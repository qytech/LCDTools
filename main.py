#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from Ui_MainWindow import Ui_MainWindow
from bmp2hex import bmp2hex
from image2bmp import image_to_bmp
from text2image import ImageGenerate

logging.basicConfig(level=logging.DEBUG)


class MainWindow(QMainWindow):
    RESOURCE_DIR = 'res'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.create_folder()

        self.message = ""
        self.image_size = (48, 32)
        self.font_size = None
        self.font_family = None
        self.imageGenerate = ImageGenerate()
        self.register_listener()
        self.set_up_ui()

    def set_up_ui(self):
        self.ui.menubar.setNativeMenuBar(False)
        self.ui.tv_lcd.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.ui.spinBox.setEnabled(False)

    def register_listener(self):
        self.ui.btn_transform.clicked.connect(self.text_to_image)
        self.ui.btn_select_font.clicked.connect(self.select_font_file)
        self.ui.action_select_image.triggered.connect(self.select_image_file)
        self.ui.spinBox.valueChanged.connect(self.on_value_changed)
        self.ui.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.ui.cb_font_size.stateChanged.connect(self.on_state_changed)

    def copy_to_clipboard(self):
        logging.debug('copy_to_clipboard')
        self.ui.tv_lcd.selectAll()
        self.ui.tv_lcd.copy()

    def on_value_changed(self):
        self.font_size = self.ui.spinBox.value()

    def on_state_changed(self):
        if self.ui.cb_font_size.isChecked():
            self.ui.spinBox.setEnabled(True)
            self.font_size = self.ui.spinBox.value()
        else:
            self.ui.spinBox.setEnabled(False)
            self.font_size = None

    def select_image_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Select Image', '',
            'Image files (*.jpg *.gif *.png *.bmp *.jpeg *.webp *.ico *.svg)',
            options=options)
        logging.debug(f'select_image_file {filename}')

        if filename:
            dist = image_to_bmp(filename, self.image_size)
            self.ui.et_message.clear()
            self.ui.et_font_path.clear()
            self.ui.cb_font_size.setChecked(False)
            self.display_dist_image(dist)
            self.image_to_lcd(dist)

    def select_font_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Select Font', '', 'Font files (*.ttc *.ttf)', options=options)
        logging.debug(f'select_font_file {filename}')

        if filename:
            self.ui.et_font_path.setText(filename)
            self.ui.cb_font_size.setChecked(True)
            self.font_family = filename
            self.font_size = self.ui.spinBox.value()

    def text_to_image(self):
        self.message = self.ui.et_message.text()

        logging.debug(
            f'message {self.message} fontsize {self.font_size} fontFamily {self.font_family}')
        # noinspection PyBroadException
        try:
            image_name = self.imageGenerate.generate(
                self.message, self.font_family, self.font_size)

            self.display_dist_image(image_name)
            self.image_to_lcd(image_name)
        except Exception as _:
            QMessageBox(QMessageBox.NoIcon, 'Open File failed',
                        'Unable to open the file').exec()
            pass

    def image_to_lcd(self, image_name):
        result = bmp2hex(image_name, 8, 0,
                         False, False, False, False, False)
        self.ui.tv_lcd.setPlainText(result)

    def display_dist_image(self, file):
        pixmap = QPixmap(file)
        self.ui.iv_image.setPixmap(pixmap)

    def closeEvent(self, event):
        self.clean_cache()
        event.accept()

    @staticmethod
    def clean_cache():
        for item in os.listdir(MainWindow.RESOURCE_DIR):
            if item.endswith('bmp'):
                os.remove(f'{MainWindow.RESOURCE_DIR}/{item}')

    @staticmethod
    def create_folder():
        if not os.path.exists(MainWindow.RESOURCE_DIR):
            os.mkdir(MainWindow.RESOURCE_DIR)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
