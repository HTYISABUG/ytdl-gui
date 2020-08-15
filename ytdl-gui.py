import json
import sys
import os

from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

INITIAL_CFG = 'config.ini'
USER_CFG = 'config.json'


def load_config():
    config = INITIAL_CFG

    if os.path.exists(USER_CFG):
        config = USER_CFG

    with open(config) as fp:
        config = json.load(fp)

    return config


if __name__ == '__main__':
    # Load config
    config = load_config()

    a = QApplication(sys.argv)
    w = MainWindow(config)
    w.show()

    a.exec()
