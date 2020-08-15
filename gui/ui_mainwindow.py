# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.url = QtWidgets.QLineEdit(self.groupBox)
        self.url.setText("")
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.download = QtWidgets.QPushButton(self.groupBox)
        self.download.setObjectName("download")
        self.horizontalLayout_2.addWidget(self.download)
        self.abort = QtWidgets.QPushButton(self.groupBox)
        self.abort.setObjectName("abort")
        self.horizontalLayout_2.addWidget(self.abort)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.save_to = QtWidgets.QLineEdit(self.groupBox)
        self.save_to.setText("")
        self.save_to.setReadOnly(True)
        self.save_to.setObjectName("save_to")
        self.horizontalLayout_4.addWidget(self.save_to)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.browse = QtWidgets.QPushButton(self.groupBox)
        self.browse.setObjectName("browse")
        self.horizontalLayout_3.addWidget(self.browse)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.log = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(9)
        self.log.setFont(font)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.verticalLayout_2.addWidget(self.log)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Downlaod Setting"))
        self.label.setText(_translate("MainWindow", "Url:"))
        self.url.setPlaceholderText(_translate("MainWindow", "https://www.youtube.com/watch?v="))
        self.download.setText(_translate("MainWindow", "Download"))
        self.abort.setText(_translate("MainWindow", "Abort"))
        self.label_2.setText(_translate("MainWindow", "Save to:"))
        self.browse.setText(_translate("MainWindow", "Browse"))
