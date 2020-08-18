import os
import requests
import shutil
import json

from zipfile import ZipFile

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QAbstractButton, QButtonGroup
from PyQt5.QtCore import QProcess

from helper.helper_ytdl import YTDLHelper

from .ui_mainwindow import Ui_MainWindow

USER_CFG = 'config.json'


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, config):
        self.config = config

        super().__init__(None)

        # Setup UI
        self.setupUi(self)
        self.save_to.setText(self.config['download_path'])

        checkbox_group = QButtonGroup(self)
        checkbox_group.setExclusive(True)
        checkbox_group.addButton(self.normal)
        checkbox_group.addButton(self.split)
        checkbox_group.addButton(self.audio_only)

        # Setup subprocess
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.process.started.connect(self.on_process_started)
        self.process.readyReadStandardOutput.connect(
            self.on_process_readyReadStandardOutput)
        self.process.finished.connect(self.on_process_finished)

        # Setup program helper
        self.ytdl_helper = YTDLHelper(
            self.config['ytdl_path'], self.config['ffmpeg_path'], self.process)

    def on_process_started(self):
        [btn.setEnabled(False) for btn in self.findChildren(QAbstractButton)]
        self.abort.setEnabled(True)

    def on_process_readyReadStandardOutput(self):
        outputBytes = self.process.readAll().data()
        outputUnicode = outputBytes.decode('big5', errors='replace')
        self.log.appendPlainText(outputUnicode)

    def on_process_finished(self, exitCode, exitStatus):
        [btn.setEnabled(True) for btn in self.findChildren(QAbstractButton)]
        self.abort.setEnabled(False)

        if exitStatus == 0:
            self.log.appendPlainText('[info] Done.')

    def on_download_released(self):
        url = self.url.text()

        folder = self.save_to.text()
        file_temp = self.filename_template.text()
        file_temp = self.template_process(file_temp)
        file_path = os.path.join(folder, file_temp)

        if self.split.isChecked():
            self.ytdl_helper.split()
        elif self.audio_only.isChecked():
            self.ytdl_helper.audio_only()

        self.ytdl_helper.output(file_path).exec(url)

    def template_process(self, template):
        if template == '':
            template = '%(title)s.%(id)s'

        if self.split.isChecked() and '.%(format)s' not in template:
            template += '.%(format)s'

        template += '.%(ext)s'

        return template

    def on_abort_released(self):
        self.process.kill()
        self.log.appendPlainText('[info]' 'The process has been aborted.')

    def on_browse_released(self):
        self.config['download_path'] = QFileDialog.getExistingDirectory(
            self, 'Open Directory', self.config['download_path'],  QFileDialog.ShowDirsOnly)

        self.save_to.setText(self.config['download_path'])

    def showEvent(self, event):
        super().showEvent(event)

        self.log.appendPlainText(
            '[info] Updating youtube-dl to latest version.')
        self.ytdl_helper.update()

    def closeEvent(self, event):
        super().closeEvent(event)

        with open(USER_CFG, 'w') as fp:
            json.dump(self.config, fp)
