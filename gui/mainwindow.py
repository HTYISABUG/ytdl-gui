import os
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QProcess

from .ui_mainwindow import Ui_MainWindow

YTDL_EXE = "youtube-dl.exe"


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, config):
        self.config = config

        super().__init__(None)
        self.setupUi(self)

        self.abort.setEnabled(False)

        # Setup subprocess
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        def on_process_finished(exitCode: int, exitStatus):
            self.download.setEnabled(True)
            self.abort.setEnabled(False)

        self.process.finished.connect(on_process_finished)

        def on_process_readyReadStandardOutput():
            outputBytes = self.process.readAll().data()
            outputUnicode = outputBytes.decode('big5', errors='replace')
            self.log.appendPlainText(outputUnicode)

        self.process.readyReadStandardOutput.connect(
            on_process_readyReadStandardOutput)

    def get_ytdl_path(self):
        if os.path.exists(self.config['ytdl_path']):
            # Check for path in config
            return self.config['ytdl_path']
        elif os.path.exists(YTDL_EXE):
            # Check for path in current directory
            return YTDL_EXE
        else:
            self.log.appendPlainText(
                '[info] youtube-dl not found, starting download automatically.')
            QApplication.processEvents()

            # Download youtube-dl
            url = 'https://youtube-dl.org/downloads/latest/youtube-dl.exe'
            r = requests.get(url, allow_redirects=True)

            with open(YTDL_EXE, 'wb') as fp:
                fp.write(r.content)

            return YTDL_EXE

    def on_download_released(self):
        url = self.url.text()
        self.download.setEnabled(False)
        self.abort.setEnabled(True)

        self.config['ytdl_path'] = self.get_ytdl_path()
        self.process.start(self.config['ytdl_path'],
                           ['-o', "%(title)s.%(id)s.%(ext)s", f"{url}"])

    def on_abort_released(self):
        self.process.kill()
        self.log.appendPlainText('[info]' 'The download has been aborted.')

    def on_browse_released(self):
        save_to = QFileDialog.getExistingDirectory(
            self, 'Open Directory', '',  QFileDialog.ShowDirsOnly)

        self.save_to.setText(save_to)
