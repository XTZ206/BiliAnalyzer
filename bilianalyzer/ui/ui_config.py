# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_ConfigWindow(object):
    def setupUi(self, ConfigWindow):
        if not ConfigWindow.objectName():
            ConfigWindow.setObjectName(u"ConfigWindow")
        ConfigWindow.resize(561, 454)
        icon = QIcon()
        icon.addFile(u"./icon/config.png", QSize(), QIcon.Normal, QIcon.Off)
        ConfigWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ConfigWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.downloadLayout = QHBoxLayout()
        self.downloadLayout.setObjectName(u"downloadLayout")
        self.downloadLabel = QLabel(ConfigWindow)
        self.downloadLabel.setObjectName(u"downloadLabel")
        font = QFont()
        font.setPointSize(14)
        self.downloadLabel.setFont(font)

        self.downloadLayout.addWidget(self.downloadLabel)

        self.downloadEntry = QLineEdit(ConfigWindow)
        self.downloadEntry.setObjectName(u"downloadEntry")
        self.downloadEntry.setFont(font)

        self.downloadLayout.addWidget(self.downloadEntry)

        self.downloadTool = QToolButton(ConfigWindow)
        self.downloadTool.setObjectName(u"downloadTool")
        self.downloadTool.setFont(font)

        self.downloadLayout.addWidget(self.downloadTool)


        self.verticalLayout.addLayout(self.downloadLayout)

        self.logLayout = QHBoxLayout()
        self.logLayout.setObjectName(u"logLayout")
        self.logCheckBox = QCheckBox(ConfigWindow)
        self.logCheckBox.setObjectName(u"logCheckBox")
        self.logCheckBox.setFont(font)

        self.logLayout.addWidget(self.logCheckBox)

        self.logSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.logLayout.addItem(self.logSpacer)


        self.verticalLayout.addLayout(self.logLayout)

        self.logpathLayout = QHBoxLayout()
        self.logpathLayout.setObjectName(u"logpathLayout")
        self.logpathLabel = QLabel(ConfigWindow)
        self.logpathLabel.setObjectName(u"logpathLabel")
        self.logpathLabel.setFont(font)

        self.logpathLayout.addWidget(self.logpathLabel)

        self.logpathEntry = QLineEdit(ConfigWindow)
        self.logpathEntry.setObjectName(u"logpathEntry")
        self.logpathEntry.setEnabled(False)
        self.logpathEntry.setFont(font)

        self.logpathLayout.addWidget(self.logpathEntry)

        self.logpathTool = QToolButton(ConfigWindow)
        self.logpathTool.setObjectName(u"logpathTool")
        self.logpathTool.setEnabled(False)
        self.logpathTool.setFont(font)

        self.logpathLayout.addWidget(self.logpathTool)


        self.verticalLayout.addLayout(self.logpathLayout)

        self.credentialGrid = QGridLayout()
        self.credentialGrid.setObjectName(u"credentialGrid")
        self.buvid3Entry = QLineEdit(ConfigWindow)
        self.buvid3Entry.setObjectName(u"buvid3Entry")
        self.buvid3Entry.setFont(font)

        self.credentialGrid.addWidget(self.buvid3Entry, 3, 1, 1, 1)

        self.sessdataLabel = QLabel(ConfigWindow)
        self.sessdataLabel.setObjectName(u"sessdataLabel")
        self.sessdataLabel.setFont(font)

        self.credentialGrid.addWidget(self.sessdataLabel, 1, 0, 1, 1)

        self.bilijctEntry = QLineEdit(ConfigWindow)
        self.bilijctEntry.setObjectName(u"bilijctEntry")
        self.bilijctEntry.setFont(font)

        self.credentialGrid.addWidget(self.bilijctEntry, 2, 1, 1, 1)

        self.credentialLayout = QHBoxLayout()
        self.credentialLayout.setObjectName(u"credentialLayout")
        self.credentialLabel = QLabel(ConfigWindow)
        self.credentialLabel.setObjectName(u"credentialLabel")
        self.credentialLabel.setFont(font)

        self.credentialLayout.addWidget(self.credentialLabel)

        self.scanButton = QPushButton(ConfigWindow)
        self.scanButton.setObjectName(u"scanButton")
        self.scanButton.setFont(font)

        self.credentialLayout.addWidget(self.scanButton)

        self.importButton = QPushButton(ConfigWindow)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setFont(font)

        self.credentialLayout.addWidget(self.importButton)

        self.exportButton = QPushButton(ConfigWindow)
        self.exportButton.setObjectName(u"exportButton")
        self.exportButton.setFont(font)

        self.credentialLayout.addWidget(self.exportButton)


        self.credentialGrid.addLayout(self.credentialLayout, 0, 0, 1, 2)

        self.bilijctLabel = QLabel(ConfigWindow)
        self.bilijctLabel.setObjectName(u"bilijctLabel")
        self.bilijctLabel.setFont(font)

        self.credentialGrid.addWidget(self.bilijctLabel, 2, 0, 1, 1)

        self.sessdataEntry = QLineEdit(ConfigWindow)
        self.sessdataEntry.setObjectName(u"sessdataEntry")
        self.sessdataEntry.setFont(font)

        self.credentialGrid.addWidget(self.sessdataEntry, 1, 1, 1, 1)

        self.buvid3Label = QLabel(ConfigWindow)
        self.buvid3Label.setObjectName(u"buvid3Label")
        self.buvid3Label.setFont(font)

        self.credentialGrid.addWidget(self.buvid3Label, 3, 0, 1, 1)


        self.verticalLayout.addLayout(self.credentialGrid)

        self.verticalSpacer = QSpacerItem(20, 62, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.confirmLayout = QHBoxLayout()
        self.confirmLayout.setObjectName(u"confirmLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.confirmLayout.addItem(self.horizontalSpacer)

        self.confirmButton = QDialogButtonBox(ConfigWindow)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setFont(font)
        self.confirmButton.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.confirmLayout.addWidget(self.confirmButton)


        self.verticalLayout.addLayout(self.confirmLayout)


        self.retranslateUi(ConfigWindow)
        self.logCheckBox.clicked["bool"].connect(self.logpathEntry.setEnabled)
        self.logCheckBox.clicked["bool"].connect(self.logpathTool.setEnabled)

        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"\u8bbe\u7f6e", None))
        self.downloadLabel.setText(QCoreApplication.translate("ConfigWindow", u"\u4e0b\u8f7d\u8def\u5f84", None))
        self.downloadTool.setText(QCoreApplication.translate("ConfigWindow", u"...", None))
        self.logCheckBox.setText(QCoreApplication.translate("ConfigWindow", u"\u4fdd\u5b58\u65e5\u5fd7", None))
        self.logpathLabel.setText(QCoreApplication.translate("ConfigWindow", u"\u65e5\u5fd7\u8def\u5f84", None))
        self.logpathTool.setText(QCoreApplication.translate("ConfigWindow", u"...", None))
        self.sessdataLabel.setText(QCoreApplication.translate("ConfigWindow", u"sessdata", None))
        self.credentialLabel.setText(QCoreApplication.translate("ConfigWindow", u"\u51ed\u8bc1", None))
        self.scanButton.setText(QCoreApplication.translate("ConfigWindow", u"\u626b\u7801\u5bfc\u5165", None))
        self.importButton.setText(QCoreApplication.translate("ConfigWindow", u"\u5bfc\u5165\u51ed\u8bc1", None))
        self.exportButton.setText(QCoreApplication.translate("ConfigWindow", u"\u5bfc\u51fa\u51ed\u8bc1", None))
        self.bilijctLabel.setText(QCoreApplication.translate("ConfigWindow", u"bili_jct", None))
        self.buvid3Label.setText(QCoreApplication.translate("ConfigWindow", u"buvid3", None))
    # retranslateUi

