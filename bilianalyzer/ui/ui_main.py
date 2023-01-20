# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 611)
        icon = QIcon()
        icon.addFile(u"./icon/main.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionConfig = QAction(MainWindow)
        self.actionConfig.setObjectName(u"actionConfig")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionTutorial = QAction(MainWindow)
        self.actionTutorial.setObjectName(u"actionTutorial")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.title)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font1 = QFont()
        font1.setPointSize(14)
        self.tabWidget.setFont(font1)
        self.convertTab = QWidget()
        self.convertTab.setObjectName(u"convertTab")
        self.verticalLayout_3 = QVBoxLayout(self.convertTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.convertGrid = QGridLayout()
        self.convertGrid.setObjectName(u"convertGrid")
        self.convertInputLabel = QLabel(self.convertTab)
        self.convertInputLabel.setObjectName(u"convertInputLabel")

        self.convertGrid.addWidget(self.convertInputLabel, 0, 0, 1, 1)

        self.convertInput = QLineEdit(self.convertTab)
        self.convertInput.setObjectName(u"convertInput")

        self.convertGrid.addWidget(self.convertInput, 0, 1, 1, 1)

        self.convertOutputLabel = QLabel(self.convertTab)
        self.convertOutputLabel.setObjectName(u"convertOutputLabel")

        self.convertGrid.addWidget(self.convertOutputLabel, 1, 0, 1, 1)

        self.convertOutput = QLineEdit(self.convertTab)
        self.convertOutput.setObjectName(u"convertOutput")
        self.convertOutput.setReadOnly(True)

        self.convertGrid.addWidget(self.convertOutput, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.convertGrid)

        self.convertLine = QFrame(self.convertTab)
        self.convertLine.setObjectName(u"convertLine")
        self.convertLine.setFrameShape(QFrame.HLine)
        self.convertLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.convertLine)

        self.convertControl = QHBoxLayout()
        self.convertControl.setObjectName(u"convertControl")
        self.convertControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.convertControl.addItem(self.convertControlSpacer_left)

        self.convertButton = QPushButton(self.convertTab)
        self.convertButton.setObjectName(u"convertButton")

        self.convertControl.addWidget(self.convertButton)

        self.copyButton = QPushButton(self.convertTab)
        self.copyButton.setObjectName(u"copyButton")

        self.convertControl.addWidget(self.copyButton)

        self.convertControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.convertControl.addItem(self.convertControlSpacer_right)


        self.verticalLayout_3.addLayout(self.convertControl)

        self.convertSpacer = QSpacerItem(20, 328, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.convertSpacer)

        self.tabWidget.addTab(self.convertTab, "")
        self.downloadTab = QWidget()
        self.downloadTab.setObjectName(u"downloadTab")
        self.downloadTab.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.downloadTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoLayout = QHBoxLayout()
        self.infoLayout.setObjectName(u"infoLayout")
        self.infoSpacer_left = QSpacerItem(149, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.infoLayout.addItem(self.infoSpacer_left)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.typeBox = QComboBox(self.downloadTab)
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.setObjectName(u"typeBox")
        self.typeBox.setFont(font1)

        self.gridLayout.addWidget(self.typeBox, 1, 1, 1, 1)

        self.startBox = QSpinBox(self.downloadTab)
        self.startBox.setObjectName(u"startBox")
        self.startBox.setFont(font1)
        self.startBox.setMinimum(1)
        self.startBox.setMaximum(10000000)

        self.gridLayout.addWidget(self.startBox, 2, 1, 1, 1)

        self.endLabel = QLabel(self.downloadTab)
        self.endLabel.setObjectName(u"endLabel")
        self.endLabel.setFont(font1)

        self.gridLayout.addWidget(self.endLabel, 3, 0, 1, 1)

        self.typeLabel = QLabel(self.downloadTab)
        self.typeLabel.setObjectName(u"typeLabel")
        self.typeLabel.setFont(font1)

        self.gridLayout.addWidget(self.typeLabel, 1, 0, 1, 1)

        self.startLabel = QLabel(self.downloadTab)
        self.startLabel.setObjectName(u"startLabel")
        self.startLabel.setFont(font1)

        self.gridLayout.addWidget(self.startLabel, 2, 0, 1, 1)

        self.idLabel = QLabel(self.downloadTab)
        self.idLabel.setObjectName(u"idLabel")
        self.idLabel.setFont(font1)

        self.gridLayout.addWidget(self.idLabel, 0, 0, 1, 1)

        self.stepLabel = QLabel(self.downloadTab)
        self.stepLabel.setObjectName(u"stepLabel")
        self.stepLabel.setFont(font1)

        self.gridLayout.addWidget(self.stepLabel, 4, 0, 1, 1)

        self.endBox = QSpinBox(self.downloadTab)
        self.endBox.setObjectName(u"endBox")
        self.endBox.setFont(font1)
        self.endBox.setMinimum(1)
        self.endBox.setMaximum(10000000)

        self.gridLayout.addWidget(self.endBox, 3, 1, 1, 1)

        self.idEntry = QLineEdit(self.downloadTab)
        self.idEntry.setObjectName(u"idEntry")
        self.idEntry.setFont(font1)

        self.gridLayout.addWidget(self.idEntry, 0, 1, 1, 1)

        self.stepBox = QSpinBox(self.downloadTab)
        self.stepBox.setObjectName(u"stepBox")
        self.stepBox.setFont(font1)
        self.stepBox.setMinimum(1)
        self.stepBox.setMaximum(100000)

        self.gridLayout.addWidget(self.stepBox, 4, 1, 1, 1)


        self.infoLayout.addLayout(self.gridLayout)

        self.infoSpacer_right = QSpacerItem(149, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.infoLayout.addItem(self.infoSpacer_right)


        self.verticalLayout.addLayout(self.infoLayout)

        self.line = QFrame(self.downloadTab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.setObjectName(u"controlLayout")
        self.controlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.controlLayout.addItem(self.controlSpacer_left)

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.downloadProgress = QProgressBar(self.downloadTab)
        self.downloadProgress.setObjectName(u"downloadProgress")
        self.downloadProgress.setFont(font1)
        self.downloadProgress.setMinimum(0)
        self.downloadProgress.setMaximum(1)
        self.downloadProgress.setValue(0)
        self.downloadProgress.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.downloadProgress.setTextVisible(True)
        self.downloadProgress.setInvertedAppearance(False)
        self.downloadProgress.setTextDirection(QProgressBar.TopToBottom)

        self.buttonLayout.addWidget(self.downloadProgress)

        self.downloadButton = QPushButton(self.downloadTab)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setFont(font1)

        self.buttonLayout.addWidget(self.downloadButton)


        self.controlLayout.addLayout(self.buttonLayout)

        self.controlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.controlLayout.addItem(self.controlSpacer_right)


        self.verticalLayout.addLayout(self.controlLayout)

        self.downloadSpacer = QSpacerItem(20, 138, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.downloadSpacer)

        self.tabWidget.addTab(self.downloadTab, "")
        self.analyzeTab = QWidget()
        self.analyzeTab.setObjectName(u"analyzeTab")
        self.verticalLayout_4 = QVBoxLayout(self.analyzeTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.analyzeInfoLayout = QGridLayout()
        self.analyzeInfoLayout.setObjectName(u"analyzeInfoLayout")
        self.analyzeCmtfileLabel = QLabel(self.analyzeTab)
        self.analyzeCmtfileLabel.setObjectName(u"analyzeCmtfileLabel")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileLabel, 0, 0, 1, 1)

        self.analyzeCmtfileInput = QLineEdit(self.analyzeTab)
        self.analyzeCmtfileInput.setObjectName(u"analyzeCmtfileInput")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileInput, 0, 1, 1, 1)

        self.analyzeCmtfileButton = QToolButton(self.analyzeTab)
        self.analyzeCmtfileButton.setObjectName(u"analyzeCmtfileButton")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileButton, 0, 2, 1, 1)

        self.analyzeModeLabel = QLabel(self.analyzeTab)
        self.analyzeModeLabel.setObjectName(u"analyzeModeLabel")

        self.analyzeInfoLayout.addWidget(self.analyzeModeLabel, 1, 0, 1, 1)

        self.analyzeModeBox = QComboBox(self.analyzeTab)
        self.analyzeModeBox.addItem("")
        self.analyzeModeBox.addItem("")
        self.analyzeModeBox.setObjectName(u"analyzeModeBox")

        self.analyzeInfoLayout.addWidget(self.analyzeModeBox, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.analyzeInfoLayout)

        self.analyzeTable = QTableWidget(self.analyzeTab)
        self.analyzeTable.setObjectName(u"analyzeTable")
        self.analyzeTable.setShowGrid(True)
        self.analyzeTable.setColumnCount(0)

        self.verticalLayout_4.addWidget(self.analyzeTable)

        self.analyzeLine = QFrame(self.analyzeTab)
        self.analyzeLine.setObjectName(u"analyzeLine")
        self.analyzeLine.setFrameShape(QFrame.HLine)
        self.analyzeLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.analyzeLine)

        self.analyzeProgress = QProgressBar(self.analyzeTab)
        self.analyzeProgress.setObjectName(u"analyzeProgress")
        self.analyzeProgress.setFont(font1)
        self.analyzeProgress.setMinimum(0)
        self.analyzeProgress.setMaximum(1)
        self.analyzeProgress.setValue(0)
        self.analyzeProgress.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.analyzeProgress.setTextVisible(True)
        self.analyzeProgress.setInvertedAppearance(False)
        self.analyzeProgress.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_4.addWidget(self.analyzeProgress)

        self.analyzeControlLayout = QHBoxLayout()
        self.analyzeControlLayout.setObjectName(u"analyzeControlLayout")
        self.analyzeControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.analyzeControlLayout.addItem(self.analyzeControlSpacer_left)

        self.analyzeRunButton = QPushButton(self.analyzeTab)
        self.analyzeRunButton.setObjectName(u"analyzeRunButton")

        self.analyzeControlLayout.addWidget(self.analyzeRunButton)

        self.analyzeExportButton = QPushButton(self.analyzeTab)
        self.analyzeExportButton.setObjectName(u"analyzeExportButton")

        self.analyzeControlLayout.addWidget(self.analyzeExportButton)

        self.analyzeControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.analyzeControlLayout.addItem(self.analyzeControlSpacer_right)


        self.verticalLayout_4.addLayout(self.analyzeControlLayout)

        self.tabWidget.addTab(self.analyzeTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 22))
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.editMenu = QMenu(self.menubar)
        self.editMenu.setObjectName(u"editMenu")
        self.helpMenu = QMenu(self.menubar)
        self.helpMenu.setObjectName(u"helpMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.fileMenu.addAction(self.actionQuit)
        self.editMenu.addAction(self.actionConfig)
        self.helpMenu.addAction(self.actionAbout)
        self.helpMenu.addAction(self.actionTutorial)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u54d4\u54e9\u54d4\u54e9\u8bc4\u8bba\u4e0b\u8f7d\u5668", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.actionConfig.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actionTutorial.setText(QCoreApplication.translate("MainWindow", u"\u6559\u7a0b", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u54d4\u54e9\u54d4\u54e9\u6210\u5206\u67e5\u8be2\u673a", None))
        self.convertInputLabel.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165AV\u53f7/BV\u53f7", None))
        self.convertOutputLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362\u7ed3\u679c", None))
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362", None))
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.convertTab), QCoreApplication.translate("MainWindow", u"\u8f6c\u6362", None))
        self.typeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u89c6\u9891", None))
        self.typeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u52a8\u6001", None))
        self.typeBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u753b\u518c", None))

        self.endLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u7d22\u5f15", None))
        self.typeLabel.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\u7c7b\u578b", None))
        self.startLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u7d22\u5f15", None))
        self.idLabel.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90ID", None))
        self.stepLabel.setText(QCoreApplication.translate("MainWindow", u"\u7d22\u5f15\u95f4\u9694", None))
        self.downloadProgress.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.downloadButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.downloadTab), QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.analyzeCmtfileLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u8bc4\u8bba\u6587\u4ef6", None))
        self.analyzeCmtfileButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.analyzeModeLabel.setText(QCoreApplication.translate("MainWindow", u"\u5206\u6790\u6a21\u5f0f", None))
        self.analyzeModeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u8bc4\u8bba\u8005\u5173\u6ce8", None))
        self.analyzeModeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u8bc4\u8bba\u8005\u7c89\u4e1d\u724c", None))

        self.analyzeProgress.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.analyzeRunButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5206\u6790", None))
        self.analyzeExportButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u7ed3\u679c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analyzeTab), QCoreApplication.translate("MainWindow", u"\u5206\u6790", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.editMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.helpMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

