#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
author: ingbyr
website: www.ingbyr.com
"""
import os

from PyQt5.QtWidgets import QDialog, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi

from app import log
from app.youget_helper import GetMediaInfoThread, get_itag


class FileListDialog(QDialog):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.dialog = loadUi(os.path.join("ui", "files_list_dialog.ui"), self)
        self.init_ui()

    def init_ui(self):
        default_item = QListWidgetItem(self.tr("Loading..."))
        self.dialog.list_widget.addItem(default_item)
        self.dialog.show()

        self.info_thread = GetMediaInfoThread("-i", self.url)
        self.info_thread.finish_signal.connect(self.show_info)
        self.info_thread.start()

    def show_info(self, result):
        self.dialog.list_widget.clear()
        for op in result:
            item = QListWidgetItem(self.tr(op))
            self.dialog.list_widget.addItem(item)
        self.dialog.list_widget.itemClicked.connect(self.start_download)

    def start_download(self, item):
        self.show_msg(item.text())
        tag = get_itag(item.text())
        print(tag)

    def show_msg(self, text, title="Debug"):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()