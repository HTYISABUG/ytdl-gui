from PyQt5.QtCore import QProcess


class FFProbeHelper(object):

    def __init__(self, ffprobe_path, text_process):
        self.ffprobe_path = ffprobe_path
        self.text_process = text_process

    def get_duration(self, url):
        self.text_process.start(self.ffprobe_path, [
            '-i', url,
            '-show_entries', 'format=duration',
            '-v', 'quiet',
            '-of', 'csv=p=0',
        ])

        self.text_process.waitForReadyRead()
        self.text_process.waitForFinished()

        duration = self.text_process.readAll().data().decode().strip()

        return duration
