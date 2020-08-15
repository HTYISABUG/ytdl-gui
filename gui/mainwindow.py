import os
import requests
import shutil
import json

from zipfile import ZipFile

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QProcess

from .ui_mainwindow import Ui_MainWindow

YTDL_EXE = "youtube-dl.exe"
FFMPEG_BUILD = 'ffmpeg-4.3.1-win64-static'
FFMPEG_EXE = 'ffmpeg.exe'
USER_CFG = 'config.json'


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, config):
        self.config = config

        super().__init__(None)
        self.setupUi(self)

        self.abort.setEnabled(False)
        self.save_to.setText(self.config['download_path'])
        self.setWindowTitle('ytdl-gui')

        # Setup subprocess
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        def on_process_finished(exitCode: int, exitStatus):
            self.download.setEnabled(True)
            self.abort.setEnabled(False)
            self.browse.setEnabled(True)

        self.process.finished.connect(on_process_finished)

        def on_process_readyReadStandardOutput():
            outputBytes = self.process.readAll().data()
            outputUnicode = outputBytes.decode('big5', errors='replace')
            self.log.appendPlainText(outputUnicode)

        self.process.readyReadStandardOutput.connect(
            on_process_readyReadStandardOutput)

    def on_download_released(self):
        url = self.url.text()
        self.download.setEnabled(False)
        self.browse.setEnabled(False)

        self.config['ytdl_path'] = self.get_ytdl_path()
        self.config['ffmpeg_path'] = self.get_ffmpeg_path()
        self.abort.setEnabled(True)

        folder = self.save_to.text()
        file_temp = "%(title)s.%(id)s.%(ext)s"
        file_path = os.path.join(folder, file_temp)

        self.process.start(self.config['ytdl_path'], [
            '--ffmpeg-location', self.config['ffmpeg_path'],
            '-o', file_path,
            url
        ])

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
            self.log.appendPlainText(
                '[info] The window will be freezed for a while.')
            QApplication.processEvents()

            # Download youtube-dl
            url = 'https://youtube-dl.org/downloads/latest/youtube-dl.exe'
            r = requests.get(url, allow_redirects=True)

            with open(YTDL_EXE, 'wb') as fp:
                fp.write(r.content)

            return YTDL_EXE

    def get_ffmpeg_path(self):
        if os.path.exists(self.config['ffmpeg_path']):
            # Check for path in config
            return self.config['ffmpeg_path']
        elif os.path.exists(FFMPEG_EXE):
            # Check for path in current directory
            return FFMPEG_EXE
        else:
            self.log.appendPlainText(
                '[info] ffmpeg not found, starting download automatically.')
            self.log.appendPlainText(
                '[info] The window will be freezed for a while.')
            QApplication.processEvents()

            # Download ffmpeg
            url = f'https://ffmpeg.zeranoe.com/builds/win64/static/{FFMPEG_BUILD}.zip'
            r = requests.get(url, allow_redirects=True)

            with open(f'{FFMPEG_BUILD}.zip', 'wb') as fp:
                fp.write(r.content)

            with ZipFile(f'{FFMPEG_BUILD}.zip') as zip:
                zip.extractall('')

            shutil.move(
                os.path.join(FFMPEG_BUILD, 'bin', FFMPEG_EXE), FFMPEG_EXE)
            shutil.rmtree(FFMPEG_BUILD)
            os.remove(f'{FFMPEG_BUILD}.zip')

            return FFMPEG_EXE

    def on_abort_released(self):
        self.process.kill()
        self.log.appendPlainText('[info]' 'The download has been aborted.')

    def on_browse_released(self):
        self.config['download_path'] = QFileDialog.getExistingDirectory(
            self, 'Open Directory', self.config['download_path'],  QFileDialog.ShowDirsOnly)

        self.save_to.setText(self.config['download_path'])

    def closeEvent(self, event):
        with open(USER_CFG, 'w') as fp:
            json.dump(self.config, fp)

        super().closeEvent(event)
