# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFrame,
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
        self.resultPathLayout = QHBoxLayout()
        self.resultPathLayout.setObjectName(u"resultPathLayout")
        self.resultPathLabel = QLabel(ConfigWindow)
        self.resultPathLabel.setObjectName(u"resultPathLabel")
        font = QFont()
        font.setPointSize(14)
        self.resultPathLabel.setFont(font)

        self.resultPathLayout.addWidget(self.resultPathLabel)

        self.resultPathInput = QLineEdit(ConfigWindow)
        self.resultPathInput.setObjectName(u"resultPathInput")
        self.resultPathInput.setFont(font)

        self.resultPathLayout.addWidget(self.resultPathInput)

        self.resultPathButton = QToolButton(ConfigWindow)
        self.resultPathButton.setObjectName(u"resultPathButton")
        self.resultPathButton.setFont(font)

        self.resultPathLayout.addWidget(self.resultPathButton)


        self.verticalLayout.addLayout(self.resultPathLayout)

        self.configLine_1 = QFrame(ConfigWindow)
        self.configLine_1.setObjectName(u"configLine_1")
        self.configLine_1.setFrameShape(QFrame.HLine)
        self.configLine_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.configLine_1)

        self.credentialLayout = QGridLayout()
        self.credentialLayout.setObjectName(u"credentialLayout")
        self.credentialLabel = QLabel(ConfigWindow)
        self.credentialLabel.setObjectName(u"credentialLabel")
        self.credentialLabel.setFont(font)

        self.credentialLayout.addWidget(self.credentialLabel, 0, 0, 1, 1)

        self.credentialControlLayout = QHBoxLayout()
        self.credentialControlLayout.setObjectName(u"credentialControlLayout")
        self.credentialScanButton = QPushButton(ConfigWindow)
        self.credentialScanButton.setObjectName(u"credentialScanButton")
        self.credentialScanButton.setFont(font)

        self.credentialControlLayout.addWidget(self.credentialScanButton)

        self.credentialImportButton = QPushButton(ConfigWindow)
        self.credentialImportButton.setObjectName(u"credentialImportButton")
        self.credentialImportButton.setFont(font)

        self.credentialControlLayout.addWidget(self.credentialImportButton)

        self.credentialExportButton = QPushButton(ConfigWindow)
        self.credentialExportButton.setObjectName(u"credentialExportButton")
        self.credentialExportButton.setFont(font)

        self.credentialControlLayout.addWidget(self.credentialExportButton)

        self.credentialRevealButton = QPushButton(ConfigWindow)
        self.credentialRevealButton.setObjectName(u"credentialRevealButton")
        self.credentialRevealButton.setFont(font)

        self.credentialControlLayout.addWidget(self.credentialRevealButton)


        self.credentialLayout.addLayout(self.credentialControlLayout, 0, 1, 1, 1)

        self.credentialSessdataLabel = QLabel(ConfigWindow)
        self.credentialSessdataLabel.setObjectName(u"credentialSessdataLabel")
        self.credentialSessdataLabel.setFont(font)

        self.credentialLayout.addWidget(self.credentialSessdataLabel, 1, 0, 1, 1)

        self.credentialSessdataInput = QLineEdit(ConfigWindow)
        self.credentialSessdataInput.setObjectName(u"credentialSessdataInput")
        self.credentialSessdataInput.setFont(font)
        self.credentialSessdataInput.setEchoMode(QLineEdit.Password)

        self.credentialLayout.addWidget(self.credentialSessdataInput, 1, 1, 1, 1)

        self.credentialBilijctLabel = QLabel(ConfigWindow)
        self.credentialBilijctLabel.setObjectName(u"credentialBilijctLabel")
        self.credentialBilijctLabel.setFont(font)

        self.credentialLayout.addWidget(self.credentialBilijctLabel, 2, 0, 1, 1)

        self.credentialBilijctInput = QLineEdit(ConfigWindow)
        self.credentialBilijctInput.setObjectName(u"credentialBilijctInput")
        self.credentialBilijctInput.setFont(font)
        self.credentialBilijctInput.setEchoMode(QLineEdit.Password)

        self.credentialLayout.addWidget(self.credentialBilijctInput, 2, 1, 1, 1)

        self.credentialBuvid3Label = QLabel(ConfigWindow)
        self.credentialBuvid3Label.setObjectName(u"credentialBuvid3Label")
        self.credentialBuvid3Label.setFont(font)

        self.credentialLayout.addWidget(self.credentialBuvid3Label, 3, 0, 1, 1)

        self.credentialBuvid3Input = QLineEdit(ConfigWindow)
        self.credentialBuvid3Input.setObjectName(u"credentialBuvid3Input")
        self.credentialBuvid3Input.setFont(font)
        self.credentialBuvid3Input.setEchoMode(QLineEdit.Password)

        self.credentialLayout.addWidget(self.credentialBuvid3Input, 3, 1, 1, 1)

        self.credentialDedeuseridLabel = QLabel(ConfigWindow)
        self.credentialDedeuseridLabel.setObjectName(u"credentialDedeuseridLabel")
        self.credentialDedeuseridLabel.setFont(font)

        self.credentialLayout.addWidget(self.credentialDedeuseridLabel, 4, 0, 1, 1)

        self.credentialDedeuseridInput = QLineEdit(ConfigWindow)
        self.credentialDedeuseridInput.setObjectName(u"credentialDedeuseridInput")
        self.credentialDedeuseridInput.setFont(font)
        self.credentialDedeuseridInput.setEchoMode(QLineEdit.Password)

        self.credentialLayout.addWidget(self.credentialDedeuseridInput, 4, 1, 1, 1)


        self.verticalLayout.addLayout(self.credentialLayout)

        self.configSpacer = QSpacerItem(20, 62, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.configSpacer)

        self.confirmLayout = QHBoxLayout()
        self.confirmLayout.setObjectName(u"confirmLayout")
        self.confirmSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.confirmLayout.addItem(self.confirmSpacer)

        self.confirmButton = QDialogButtonBox(ConfigWindow)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setFont(font)
        self.confirmButton.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.confirmLayout.addWidget(self.confirmButton)


        self.verticalLayout.addLayout(self.confirmLayout)


        self.retranslateUi(ConfigWindow)

        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"\u8bbe\u7f6e", None))
        self.resultPathLabel.setText(QCoreApplication.translate("ConfigWindow", u"\u8f93\u51fa\u8def\u5f84", None))
        self.resultPathButton.setText(QCoreApplication.translate("ConfigWindow", u"...", None))
        self.credentialLabel.setText(QCoreApplication.translate("ConfigWindow", u"\u51ed\u8bc1", None))
        self.credentialScanButton.setText(QCoreApplication.translate("ConfigWindow", u"\u626b\u7801\u5bfc\u5165", None))
        self.credentialImportButton.setText(QCoreApplication.translate("ConfigWindow", u"\u5bfc\u5165\u51ed\u8bc1", None))
        self.credentialExportButton.setText(QCoreApplication.translate("ConfigWindow", u"\u5bfc\u51fa\u51ed\u8bc1", None))
        self.credentialRevealButton.setText(QCoreApplication.translate("ConfigWindow", u"\u663e\u793a\u51ed\u8bc1", None))
        self.credentialSessdataLabel.setText(QCoreApplication.translate("ConfigWindow", u"sessdata", None))
        self.credentialBilijctLabel.setText(QCoreApplication.translate("ConfigWindow", u"bili_jct", None))
        self.credentialBilijctInput.setText("")
        self.credentialBuvid3Label.setText(QCoreApplication.translate("ConfigWindow", u"buvid3", None))
        self.credentialDedeuseridLabel.setText(QCoreApplication.translate("ConfigWindow", u"dedeuserid", None))
        self.credentialDedeuseridInput.setText("")
    # retranslateUi

