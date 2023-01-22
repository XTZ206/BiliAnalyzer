# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tutorial.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_TutorialWindow(object):
    def setupUi(self, TutorialWindow):
        if not TutorialWindow.objectName():
            TutorialWindow.setObjectName(u"TutorialWindow")
        TutorialWindow.resize(515, 320)
        icon = QIcon()
        icon.addFile(u"./icon/tutorial.png", QSize(), QIcon.Normal, QIcon.Off)
        TutorialWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(TutorialWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(TutorialWindow)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.textBrowser = QTextBrowser(TutorialWindow)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setFont(font)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(TutorialWindow)

        QMetaObject.connectSlotsByName(TutorialWindow)
    # setupUi

    def retranslateUi(self, TutorialWindow):
        TutorialWindow.setWindowTitle(QCoreApplication.translate("TutorialWindow", u"\u6559\u7a0b", None))
        self.label.setText(QCoreApplication.translate("TutorialWindow", u"\u4f7f\u7528\u6559\u7a0b", None))
    # retranslateUi

