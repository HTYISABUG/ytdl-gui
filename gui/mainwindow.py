import os
import requests
import shutil
import json

from zipfile import ZipFile

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QAbstractButton, QButtonGroup, QGroupBox
from PyQt5.QtCore import QProcess, Qt

from helper.helper_ytdl import YTDLHelper
from helper.helper_ffprobe import FFProbeHelper
from helper.helper_ffmpeg import FFMPEGHelper

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

        # Setup subprocess for getting stdout
        self.text_process = QProcess(self)
        self.text_process.setProcessChannelMode(QProcess.MergedChannels)

        # Setup program helper
        self.ytdl_helper = YTDLHelper(
            self.config['ytdl_path'], self.config['ffmpeg_path'], self.process, self.text_process)
        self.ffprobe_helper = FFProbeHelper(
            self.config['ffprobe_path'], self.text_process)
        self.ffmpeg_helper = FFMPEGHelper(
            self.config['ffmpeg_path'], self.process)

    def on_process_started(self):
        [btn.setEnabled(False)
         for btn in self.groupBox.findChildren(QAbstractButton)]
        self.abort.setEnabled(True)

        [btn.setEnabled(False)
         for btn in self.groupBox_2.findChildren((QAbstractButton, QGroupBox)) if btn.isCheckable()]

    def on_process_readyReadStandardOutput(self):
        outputBytes = self.process.readAll().data()
        outputUnicode = outputBytes.decode('big5', errors='replace')
        self.log.appendPlainText(outputUnicode)

    def on_process_finished(self, exitCode, exitStatus):
        [btn.setEnabled(True)
         for btn in self.groupBox.findChildren(QAbstractButton)]
        self.abort.setEnabled(False)

        [btn.setEnabled(True)
         for btn in self.groupBox_2.findChildren((QAbstractButton, QGroupBox)) if btn.isCheckable()]
        self.encoding.setEnabled(self.normal.isChecked())

        if exitStatus == 0:
            self.log.appendPlainText('[info] Done.')

    def on_download_released(self):
        url = self.url.text()

        folder = self.save_to.text()
        file_temp = self.filename_template.text()
        file_temp = self.template_process(file_temp)
        file_path = os.path.join(folder, file_temp)

        if not self.clip.isChecked():
            # Check Video Seperation option
            if self.split.isChecked():
                self.ytdl_helper.split()
            elif self.audio_only.isChecked():
                self.ytdl_helper.audio_only()

            # Check Video Encoding options
            if self.encoding.isChecked():
                fmt = self.encoding_format.currentText()
                self.ytdl_helper.encoding(fmt)

            # Check Thumbnail option
            if self.thumbnail.isChecked():
                self.ytdl_helper.thumbnail()

            self.ytdl_helper.output(file_path).exec(url)
        else:
            filename = self.ytdl_helper.get_filename(url)
            url = self.ytdl_helper.get_real_url(url)

            start = self.clip_from.text()
            end = self.clip_end.text()

            if start != '':
                self.ffmpeg_helper.start_time(start)

            if end != '':
                if self.clip_end_options.currentIndex() == 0:
                    self.ffmpeg_helper.stop_time(end)
                elif self.clip_end_options.currentIndex() == 1:
                    self.ffmpeg_helper.duration(end)

            self.ffmpeg_helper.download(url, filename)

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

    def on_normal_stateChanged(self, state):
        self.encoding.setEnabled(state == Qt.Checked)

    def on_analysis_released(self):
        url = self.ytdl_helper.get_real_url(self.url.text())
        duration = self.ffprobe_helper.get_duration(url)

        if duration == '':
            duration = 'N/A'
        else:
            duration = int(float(duration))

        self.video_length.setText(f'Total length: {duration}s')

    def on_clip_toggled(self, on):
        if on:
            self.filename_template.clear()
            self.normal.setChecked(True)
            self.encoding.setChecked(False)
            self.thumbnail.setChecked(False)

        self.filename_template.setEnabled(not on)
        [btn.setEnabled(not on)
         for btn in self.groupBox_3.findChildren(QAbstractButton)]
        self.encoding.setEnabled(not on)
        self.thumbnail.setEnabled(not on)

    def showEvent(self, event):
        super().showEvent(event)

        self.log.appendPlainText(
            '[info] Updating youtube-dl to latest version.')
        self.ytdl_helper.update()

    def closeEvent(self, event):
        super().closeEvent(event)

        with open(USER_CFG, 'w') as fp:
            json.dump(self.config, fp)
