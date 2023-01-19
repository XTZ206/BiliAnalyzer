# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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

class Ui_AboutWiindow(object):
    def setupUi(self, AboutWiindow):
        if not AboutWiindow.objectName():
            AboutWiindow.setObjectName(u"AboutWiindow")
        AboutWiindow.resize(480, 200)
        AboutWiindow.setMinimumSize(QSize(480, 200))
        AboutWiindow.setMaximumSize(QSize(480, 200))
        AboutWiindow.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"./icon/info.png", QSize(), QIcon.Normal, QIcon.Off)
        AboutWiindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AboutWiindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.aboutLabel = QLabel(AboutWiindow)
        self.aboutLabel.setObjectName(u"aboutLabel")
        font = QFont()
        font.setPointSize(14)
        self.aboutLabel.setFont(font)
        self.aboutLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.aboutLabel)

        self.textBrowser = QTextBrowser(AboutWiindow)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(AboutWiindow)

        QMetaObject.connectSlotsByName(AboutWiindow)
    # setupUi

    def retranslateUi(self, AboutWiindow):
        AboutWiindow.setWindowTitle(QCoreApplication.translate("AboutWiindow", u"\u5173\u4e8e", None))
        self.aboutLabel.setText(QCoreApplication.translate("AboutWiindow", u"\u5173\u4e8e", None))
        self.textBrowser.setMarkdown("")
        self.textBrowser.setHtml(QCoreApplication.translate("AboutWiindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

