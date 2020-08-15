import json
import sys

from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow


def load_config():
    with open('config.json') as fp:
        config = json.load(fp)
    return config


if __name__ == '__main__':
    # Load config
    config = load_config()

    a = QApplication(sys.argv)
    w = MainWindow(config)
    w.show()

    a.exec()
