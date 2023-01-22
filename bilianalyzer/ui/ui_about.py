# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        if not AboutWindow.objectName():
            AboutWindow.setObjectName(u"AboutWindow")
        AboutWindow.resize(480, 240)
        AboutWindow.setMinimumSize(QSize(480, 240))
        AboutWindow.setMaximumSize(QSize(480, 240))
        AboutWindow.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"./icon/info.png", QSize(), QIcon.Normal, QIcon.Off)
        AboutWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AboutWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.aboutLabel = QLabel(AboutWindow)
        self.aboutLabel.setObjectName(u"aboutLabel")
        font = QFont()
        font.setPointSize(14)
        self.aboutLabel.setFont(font)
        self.aboutLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.aboutLabel)

        self.textBrowser = QTextBrowser(AboutWindow)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(AboutWindow)

        QMetaObject.connectSlotsByName(AboutWindow)
    # setupUi

    def retranslateUi(self, AboutWindow):
        AboutWindow.setWindowTitle(QCoreApplication.translate("AboutWindow", u"\u5173\u4e8e", None))
        self.aboutLabel.setText(QCoreApplication.translate("AboutWindow", u"\u5173\u4e8eBiliAnalyzer", None))
        self.textBrowser.setMarkdown("")
        self.textBrowser.setHtml(QCoreApplication.translate("AboutWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

