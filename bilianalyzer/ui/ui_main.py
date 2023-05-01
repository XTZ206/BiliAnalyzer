# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

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
        self.convertInfoLayout = QGridLayout()
        self.convertInfoLayout.setObjectName(u"convertInfoLayout")
        self.convertInputLabel = QLabel(self.convertTab)
        self.convertInputLabel.setObjectName(u"convertInputLabel")

        self.convertInfoLayout.addWidget(self.convertInputLabel, 0, 0, 1, 1)

        self.convertInput = QLineEdit(self.convertTab)
        self.convertInput.setObjectName(u"convertInput")

        self.convertInfoLayout.addWidget(self.convertInput, 0, 1, 1, 1)

        self.convertOutputLabel = QLabel(self.convertTab)
        self.convertOutputLabel.setObjectName(u"convertOutputLabel")

        self.convertInfoLayout.addWidget(self.convertOutputLabel, 1, 0, 1, 1)

        self.convertOutput = QLineEdit(self.convertTab)
        self.convertOutput.setObjectName(u"convertOutput")
        self.convertOutput.setReadOnly(True)

        self.convertInfoLayout.addWidget(self.convertOutput, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.convertInfoLayout)

        self.convertLine = QFrame(self.convertTab)
        self.convertLine.setObjectName(u"convertLine")
        self.convertLine.setFrameShape(QFrame.HLine)
        self.convertLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.convertLine)

        self.convertControlLayout = QHBoxLayout()
        self.convertControlLayout.setObjectName(u"convertControlLayout")
        self.convertControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.convertControlLayout.addItem(self.convertControlSpacer_left)

        self.convertRunButton = QPushButton(self.convertTab)
        self.convertRunButton.setObjectName(u"convertRunButton")

        self.convertControlLayout.addWidget(self.convertRunButton)

        self.convertCopyButton = QPushButton(self.convertTab)
        self.convertCopyButton.setObjectName(u"convertCopyButton")

        self.convertControlLayout.addWidget(self.convertCopyButton)

        self.convertControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.convertControlLayout.addItem(self.convertControlSpacer_right)


        self.verticalLayout_3.addLayout(self.convertControlLayout)

        self.convertSpacer = QSpacerItem(20, 328, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.convertSpacer)

        self.tabWidget.addTab(self.convertTab, "")
        self.downloadTab = QWidget()
        self.downloadTab.setObjectName(u"downloadTab")
        self.downloadTab.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.downloadTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.downloadInfoLayout = QGridLayout()
        self.downloadInfoLayout.setObjectName(u"downloadInfoLayout")
        self.downloadEndInput = QSpinBox(self.downloadTab)
        self.downloadEndInput.setObjectName(u"downloadEndInput")
        self.downloadEndInput.setFont(font1)
        self.downloadEndInput.setMinimum(1)
        self.downloadEndInput.setMaximum(10000000)

        self.downloadInfoLayout.addWidget(self.downloadEndInput, 3, 1, 1, 1)

        self.downloadOidInput = QLineEdit(self.downloadTab)
        self.downloadOidInput.setObjectName(u"downloadOidInput")
        self.downloadOidInput.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadOidInput, 0, 1, 1, 1)

        self.downloadOtypeInput = QComboBox(self.downloadTab)
        self.downloadOtypeInput.addItem("")
        self.downloadOtypeInput.addItem("")
        self.downloadOtypeInput.addItem("")
        self.downloadOtypeInput.setObjectName(u"downloadOtypeInput")
        self.downloadOtypeInput.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadOtypeInput, 1, 1, 1, 1)

        self.downloadStartLabel = QLabel(self.downloadTab)
        self.downloadStartLabel.setObjectName(u"downloadStartLabel")
        self.downloadStartLabel.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadStartLabel, 2, 0, 1, 1)

        self.downloadStepLabel = QLabel(self.downloadTab)
        self.downloadStepLabel.setObjectName(u"downloadStepLabel")
        self.downloadStepLabel.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadStepLabel, 4, 0, 1, 1)

        self.downloadStepInput = QSpinBox(self.downloadTab)
        self.downloadStepInput.setObjectName(u"downloadStepInput")
        self.downloadStepInput.setFont(font1)
        self.downloadStepInput.setMinimum(1)
        self.downloadStepInput.setMaximum(100000)
        self.downloadStepInput.setStepType(QAbstractSpinBox.DefaultStepType)
        self.downloadStepInput.setValue(20)

        self.downloadInfoLayout.addWidget(self.downloadStepInput, 4, 1, 1, 1)

        self.downloadEndLabel = QLabel(self.downloadTab)
        self.downloadEndLabel.setObjectName(u"downloadEndLabel")
        self.downloadEndLabel.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadEndLabel, 3, 0, 1, 1)

        self.downloadOidLabel = QLabel(self.downloadTab)
        self.downloadOidLabel.setObjectName(u"downloadOidLabel")
        self.downloadOidLabel.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadOidLabel, 0, 0, 1, 1)

        self.downloadStartInput = QSpinBox(self.downloadTab)
        self.downloadStartInput.setObjectName(u"downloadStartInput")
        self.downloadStartInput.setFont(font1)
        self.downloadStartInput.setMinimum(1)
        self.downloadStartInput.setMaximum(10000000)

        self.downloadInfoLayout.addWidget(self.downloadStartInput, 2, 1, 1, 1)

        self.downloadOtypeLabel = QLabel(self.downloadTab)
        self.downloadOtypeLabel.setObjectName(u"downloadOtypeLabel")
        self.downloadOtypeLabel.setFont(font1)

        self.downloadInfoLayout.addWidget(self.downloadOtypeLabel, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.downloadInfoLayout)

        self.downloadLine = QFrame(self.downloadTab)
        self.downloadLine.setObjectName(u"downloadLine")
        self.downloadLine.setFrameShape(QFrame.HLine)
        self.downloadLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.downloadLine)

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

        self.verticalLayout.addWidget(self.downloadProgress)

        self.downloadControlLayout = QHBoxLayout()
        self.downloadControlLayout.setObjectName(u"downloadControlLayout")
        self.downloadControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.downloadControlLayout.addItem(self.downloadControlSpacer_left)

        self.downloadRunButton = QPushButton(self.downloadTab)
        self.downloadRunButton.setObjectName(u"downloadRunButton")
        self.downloadRunButton.setFont(font1)

        self.downloadControlLayout.addWidget(self.downloadRunButton)

        self.downloadControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.downloadControlLayout.addItem(self.downloadControlSpacer_right)


        self.verticalLayout.addLayout(self.downloadControlLayout)

        self.downloadSpacer = QSpacerItem(20, 138, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.downloadSpacer)

        self.tabWidget.addTab(self.downloadTab, "")
        self.analyzeTab = QWidget()
        self.analyzeTab.setObjectName(u"analyzeTab")
        self.analyzeTab.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.verticalLayout_5 = QVBoxLayout(self.analyzeTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.analyzeInfoLayout = QGridLayout()
        self.analyzeInfoLayout.setObjectName(u"analyzeInfoLayout")
        self.analyzeCmtfileInput = QLineEdit(self.analyzeTab)
        self.analyzeCmtfileInput.setObjectName(u"analyzeCmtfileInput")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileInput, 0, 1, 1, 1)

        self.analyzeCmtfileButton = QToolButton(self.analyzeTab)
        self.analyzeCmtfileButton.setObjectName(u"analyzeCmtfileButton")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileButton, 0, 2, 1, 1)

        self.analyzePercentageUnit = QLabel(self.analyzeTab)
        self.analyzePercentageUnit.setObjectName(u"analyzePercentageUnit")

        self.analyzeInfoLayout.addWidget(self.analyzePercentageUnit, 2, 2, 1, 1)

        self.analyzeUsrfileLabel = QLabel(self.analyzeTab)
        self.analyzeUsrfileLabel.setObjectName(u"analyzeUsrfileLabel")

        self.analyzeInfoLayout.addWidget(self.analyzeUsrfileLabel, 1, 0, 1, 1)

        self.analyzeUsrfileButton = QToolButton(self.analyzeTab)
        self.analyzeUsrfileButton.setObjectName(u"analyzeUsrfileButton")

        self.analyzeInfoLayout.addWidget(self.analyzeUsrfileButton, 1, 2, 1, 1)

        self.analyzeCmtfileLabel = QLabel(self.analyzeTab)
        self.analyzeCmtfileLabel.setObjectName(u"analyzeCmtfileLabel")

        self.analyzeInfoLayout.addWidget(self.analyzeCmtfileLabel, 0, 0, 1, 1)

        self.analyzePercentageLabel = QLabel(self.analyzeTab)
        self.analyzePercentageLabel.setObjectName(u"analyzePercentageLabel")

        self.analyzeInfoLayout.addWidget(self.analyzePercentageLabel, 2, 0, 1, 1)

        self.analyzeUsrfileInput = QLineEdit(self.analyzeTab)
        self.analyzeUsrfileInput.setObjectName(u"analyzeUsrfileInput")

        self.analyzeInfoLayout.addWidget(self.analyzeUsrfileInput, 1, 1, 1, 1)

        self.analyzePercentageBox = QDoubleSpinBox(self.analyzeTab)
        self.analyzePercentageBox.setObjectName(u"analyzePercentageBox")
        self.analyzePercentageBox.setMinimum(0.010000000000000)
        self.analyzePercentageBox.setMaximum(100.000000000000000)
        self.analyzePercentageBox.setValue(100.000000000000000)

        self.analyzeInfoLayout.addWidget(self.analyzePercentageBox, 2, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.analyzeInfoLayout)

        self.analyzeLine = QFrame(self.analyzeTab)
        self.analyzeLine.setObjectName(u"analyzeLine")
        self.analyzeLine.setFrameShape(QFrame.HLine)
        self.analyzeLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.analyzeLine)

        self.analyzeProgress = QProgressBar(self.analyzeTab)
        self.analyzeProgress.setObjectName(u"analyzeProgress")
        self.analyzeProgress.setMaximum(100)
        self.analyzeProgress.setValue(0)
        self.analyzeProgress.setAlignment(Qt.AlignCenter)
        self.analyzeProgress.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_5.addWidget(self.analyzeProgress)

        self.analyzeControlLayout = QHBoxLayout()
        self.analyzeControlLayout.setObjectName(u"analyzeControlLayout")
        self.analyzeControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.analyzeControlLayout.addItem(self.analyzeControlSpacer_left)

        self.analyzeExportButton = QPushButton(self.analyzeTab)
        self.analyzeExportButton.setObjectName(u"analyzeExportButton")

        self.analyzeControlLayout.addWidget(self.analyzeExportButton)

        self.analyzeRunButton = QPushButton(self.analyzeTab)
        self.analyzeRunButton.setObjectName(u"analyzeRunButton")

        self.analyzeControlLayout.addWidget(self.analyzeRunButton)

        self.analyzeControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.analyzeControlLayout.addItem(self.analyzeControlSpacer_right)


        self.verticalLayout_5.addLayout(self.analyzeControlLayout)

        self.analyzeSpacer = QSpacerItem(20, 288, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.analyzeSpacer)

        self.tabWidget.addTab(self.analyzeTab, "")
        self.statisticsTab = QWidget()
        self.statisticsTab.setObjectName(u"statisticsTab")
        self.verticalLayout_4 = QVBoxLayout(self.statisticsTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.statisticsInfoLayout = QGridLayout()
        self.statisticsInfoLayout.setObjectName(u"statisticsInfoLayout")
        self.statisticsFileLabel = QLabel(self.statisticsTab)
        self.statisticsFileLabel.setObjectName(u"statisticsFileLabel")

        self.statisticsInfoLayout.addWidget(self.statisticsFileLabel, 0, 0, 1, 1)

        self.statisticsFileInput = QLineEdit(self.statisticsTab)
        self.statisticsFileInput.setObjectName(u"statisticsFileInput")

        self.statisticsInfoLayout.addWidget(self.statisticsFileInput, 0, 1, 1, 2)

        self.statisticsFileButton = QToolButton(self.statisticsTab)
        self.statisticsFileButton.setObjectName(u"statisticsFileButton")

        self.statisticsInfoLayout.addWidget(self.statisticsFileButton, 0, 3, 1, 1)

        self.statisticsModeLabel = QLabel(self.statisticsTab)
        self.statisticsModeLabel.setObjectName(u"statisticsModeLabel")

        self.statisticsInfoLayout.addWidget(self.statisticsModeLabel, 1, 0, 1, 1)

        self.statisticsTypeBox = QComboBox(self.statisticsTab)
        self.statisticsTypeBox.addItem("")
        self.statisticsTypeBox.addItem("")
        self.statisticsTypeBox.setObjectName(u"statisticsTypeBox")

        self.statisticsInfoLayout.addWidget(self.statisticsTypeBox, 1, 1, 1, 1)

        self.statisticsPropertyBox = QComboBox(self.statisticsTab)
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.addItem("")
        self.statisticsPropertyBox.setObjectName(u"statisticsPropertyBox")

        self.statisticsInfoLayout.addWidget(self.statisticsPropertyBox, 1, 2, 1, 2)

        self.statisticsShowBox = QCheckBox(self.statisticsTab)
        self.statisticsShowBox.setObjectName(u"statisticsShowBox")

        self.statisticsInfoLayout.addWidget(self.statisticsShowBox, 2, 0, 1, 4)


        self.verticalLayout_4.addLayout(self.statisticsInfoLayout)

        self.statisticsTable = QTableWidget(self.statisticsTab)
        self.statisticsTable.setObjectName(u"statisticsTable")
        self.statisticsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.statisticsTable.setShowGrid(True)
        self.statisticsTable.setColumnCount(0)

        self.verticalLayout_4.addWidget(self.statisticsTable)

        self.statisticsLine = QFrame(self.statisticsTab)
        self.statisticsLine.setObjectName(u"statisticsLine")
        self.statisticsLine.setFrameShape(QFrame.HLine)
        self.statisticsLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.statisticsLine)

        self.statisticsProgress = QProgressBar(self.statisticsTab)
        self.statisticsProgress.setObjectName(u"statisticsProgress")
        self.statisticsProgress.setFont(font1)
        self.statisticsProgress.setMinimum(0)
        self.statisticsProgress.setMaximum(1)
        self.statisticsProgress.setValue(0)
        self.statisticsProgress.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.statisticsProgress.setTextVisible(True)
        self.statisticsProgress.setInvertedAppearance(False)
        self.statisticsProgress.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_4.addWidget(self.statisticsProgress)

        self.statisticsControlLayout = QHBoxLayout()
        self.statisticsControlLayout.setObjectName(u"statisticsControlLayout")
        self.statisticsControlSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.statisticsControlLayout.addItem(self.statisticsControlSpacer_left)

        self.statisticsRunButton = QPushButton(self.statisticsTab)
        self.statisticsRunButton.setObjectName(u"statisticsRunButton")

        self.statisticsControlLayout.addWidget(self.statisticsRunButton)

        self.statisticsExportButton = QPushButton(self.statisticsTab)
        self.statisticsExportButton.setObjectName(u"statisticsExportButton")

        self.statisticsControlLayout.addWidget(self.statisticsExportButton)

        self.statisticsControlSpacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.statisticsControlLayout.addItem(self.statisticsControlSpacer_right)


        self.verticalLayout_4.addLayout(self.statisticsControlLayout)

        self.tabWidget.addTab(self.statisticsTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 21))
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
        QWidget.setTabOrder(self.tabWidget, self.convertInput)
        QWidget.setTabOrder(self.convertInput, self.convertOutput)
        QWidget.setTabOrder(self.convertOutput, self.convertRunButton)
        QWidget.setTabOrder(self.convertRunButton, self.convertCopyButton)
        QWidget.setTabOrder(self.convertCopyButton, self.downloadOidInput)
        QWidget.setTabOrder(self.downloadOidInput, self.downloadOtypeInput)
        QWidget.setTabOrder(self.downloadOtypeInput, self.downloadStartInput)
        QWidget.setTabOrder(self.downloadStartInput, self.downloadEndInput)
        QWidget.setTabOrder(self.downloadEndInput, self.downloadStepInput)
        QWidget.setTabOrder(self.downloadStepInput, self.downloadRunButton)
        QWidget.setTabOrder(self.downloadRunButton, self.analyzeCmtfileInput)
        QWidget.setTabOrder(self.analyzeCmtfileInput, self.analyzeCmtfileButton)
        QWidget.setTabOrder(self.analyzeCmtfileButton, self.analyzeUsrfileInput)
        QWidget.setTabOrder(self.analyzeUsrfileInput, self.analyzeUsrfileButton)
        QWidget.setTabOrder(self.analyzeUsrfileButton, self.analyzeExportButton)
        QWidget.setTabOrder(self.analyzeExportButton, self.analyzeRunButton)
        QWidget.setTabOrder(self.analyzeRunButton, self.statisticsFileInput)
        QWidget.setTabOrder(self.statisticsFileInput, self.statisticsFileButton)
        QWidget.setTabOrder(self.statisticsFileButton, self.statisticsPropertyBox)
        QWidget.setTabOrder(self.statisticsPropertyBox, self.statisticsShowBox)
        QWidget.setTabOrder(self.statisticsShowBox, self.statisticsTable)
        QWidget.setTabOrder(self.statisticsTable, self.statisticsRunButton)
        QWidget.setTabOrder(self.statisticsRunButton, self.statisticsExportButton)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u54d4\u54e9\u54d4\u54e9\u6210\u5206\u67e5\u8be2\u673a", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.actionConfig.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actionTutorial.setText(QCoreApplication.translate("MainWindow", u"\u6559\u7a0b", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u54d4\u54e9\u54d4\u54e9\u6210\u5206\u67e5\u8be2\u673a", None))
        self.convertInputLabel.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165AV\u53f7/BV\u53f7", None))
        self.convertOutputLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362\u7ed3\u679c", None))
        self.convertRunButton.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362", None))
        self.convertCopyButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.convertTab), QCoreApplication.translate("MainWindow", u"\u8f6c\u6362", None))
        self.downloadOtypeInput.setItemText(0, QCoreApplication.translate("MainWindow", u"\u89c6\u9891", None))
        self.downloadOtypeInput.setItemText(1, QCoreApplication.translate("MainWindow", u"\u52a8\u6001", None))
        self.downloadOtypeInput.setItemText(2, QCoreApplication.translate("MainWindow", u"\u753b\u518c", None))

        self.downloadStartLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u7d22\u5f15", None))
        self.downloadStepLabel.setText(QCoreApplication.translate("MainWindow", u"\u7d22\u5f15\u95f4\u9694", None))
        self.downloadEndLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u7d22\u5f15", None))
        self.downloadOidLabel.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90ID", None))
        self.downloadOtypeLabel.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\u7c7b\u578b", None))
        self.downloadProgress.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.downloadRunButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.downloadTab), QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.analyzeCmtfileButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.analyzePercentageUnit.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.analyzeUsrfileLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u7528\u6237\u6587\u4ef6", None))
        self.analyzeUsrfileButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.analyzeCmtfileLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u8bc4\u8bba\u6587\u4ef6", None))
        self.analyzePercentageLabel.setText(QCoreApplication.translate("MainWindow", u"\u7b5b\u9009\u6bd4\u4f8b", None))
        self.analyzeUsrfileInput.setText("")
        self.analyzeExportButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51faUID", None))
        self.analyzeRunButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5206\u6790", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analyzeTab), QCoreApplication.translate("MainWindow", u"\u5206\u6790", None))
        self.statisticsFileLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u7edf\u8ba1\u6587\u4ef6", None))
        self.statisticsFileButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.statisticsModeLabel.setText(QCoreApplication.translate("MainWindow", u"\u7edf\u8ba1\u6a21\u5f0f", None))
        self.statisticsTypeBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u7528\u6237", None))
        self.statisticsTypeBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u8bc4\u8bba", None))

        self.statisticsPropertyBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u6027\u522b", None))
        self.statisticsPropertyBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u751f\u65e5", None))
        self.statisticsPropertyBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5b66\u6821", None))
        self.statisticsPropertyBox.setItemText(3, QCoreApplication.translate("MainWindow", u"\u4e13\u4e1a", None))
        self.statisticsPropertyBox.setItemText(4, QCoreApplication.translate("MainWindow", u"UID\u4f4d\u6570", None))
        self.statisticsPropertyBox.setItemText(5, QCoreApplication.translate("MainWindow", u"\u7b49\u7ea7", None))
        self.statisticsPropertyBox.setItemText(6, QCoreApplication.translate("MainWindow", u"\u5927\u4f1a\u5458", None))
        self.statisticsPropertyBox.setItemText(7, QCoreApplication.translate("MainWindow", u"\u6807\u7b7e", None))
        self.statisticsPropertyBox.setItemText(8, QCoreApplication.translate("MainWindow", u"\u88c5\u626e", None))
        self.statisticsPropertyBox.setItemText(9, QCoreApplication.translate("MainWindow", u"\u540d\u724c", None))
        self.statisticsPropertyBox.setItemText(10, QCoreApplication.translate("MainWindow", u"\u5173\u6ce8", None))
        self.statisticsPropertyBox.setItemText(11, QCoreApplication.translate("MainWindow", u"\u7c89\u4e1d\u724c", None))

        self.statisticsShowBox.setText(QCoreApplication.translate("MainWindow", u"\u4ee5\u6635\u79f0\u663e\u793a\u5173\u6ce8/\u7c89\u4e1d\u724c\u5bf9\u8c61\uff08\u6781\u5927\u589e\u52a0\u7edf\u8ba1\u6240\u9700\u65f6\u95f4\uff01\uff09", None))
        self.statisticsProgress.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.statisticsRunButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u7edf\u8ba1", None))
        self.statisticsExportButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u7ed3\u679c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.statisticsTab), QCoreApplication.translate("MainWindow", u"\u7edf\u8ba1", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.editMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.helpMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

