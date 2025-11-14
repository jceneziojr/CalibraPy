# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_staZJKxbB.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_StaticHelp(object):
    def setupUi(self, StaticHelp):
        if not StaticHelp.objectName():
            StaticHelp.setObjectName(u"StaticHelp")
        StaticHelp.resize(623, 206)
        self.gridLayout = QGridLayout(StaticHelp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(StaticHelp)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(StaticHelp)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignTop)

        self.line = QFrame(StaticHelp)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)


        self.retranslateUi(StaticHelp)

        QMetaObject.connectSlotsByName(StaticHelp)
    # setupUi

    def retranslateUi(self, StaticHelp):
        StaticHelp.setWindowTitle(QCoreApplication.translate("StaticHelp", u"Ajuda", None))
        self.label_2.setText(QCoreApplication.translate("StaticHelp", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:700;\">1\u00ba -</span><span style=\" font-size:10pt;\"> Selecione sua placa Arduino<br/></span><span style=\" font-size:10pt; font-weight:700;\">2\u00ba -</span><span style=\" font-size:10pt;\"> Pressione o bot\u00e3o </span><span style=\" font-size:10pt; font-weight:700;\">Configurar aquisi\u00e7\u00e3o</span><span style=\" font-size:10pt;\"> para determinar os pontos de calibra\u00e7\u00e3o<br/></span><span style=\" font-size:10pt; font-weight:700;\">3\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style=\" font-size:10pt; font-weight:700;\">Come\u00e7ar aquisi\u00e7\u00e3o</span><span style=\" font-size:10pt;\"><br/></span><span style=\" font-size:10pt; font-weight:700;\">4\u00ba - </span><span style=\" font-size:10pt;\">Ajuste o seu mensurando no ponto requisitado<br/></span><span style=\" font-size:10pt; font-weight:700;\">5\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style"
                        "=\" font-size:10pt; font-weight:700;\">Aquisitar ponto</span><span style=\" font-size:10pt;\"><br/></span><span style=\" font-size:10pt; font-weight:700;\">6\u00ba -</span><span style=\" font-size:10pt;\"> O ponto ir\u00e1 aparecer no gr\u00e1fico da parte inferior. Se necess\u00e1rio, pressione </span><span style=\" font-size:10pt; font-weight:700;\">Refazer ponto</span><span style=\" font-size:10pt;\"><br/></span><span style=\" font-size:10pt; font-weight:700;\">7\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style=\" font-size:10pt; font-weight:700;\">Pr\u00f3ximo ponto</span><span style=\" font-size:10pt;\"> para avan\u00e7ar<br/></span><span style=\" font-size:10pt; font-weight:700;\">8\u00ba -</span><span style=\" font-size:10pt;\"> Quando finalizar a aquisi\u00e7\u00e3o dos pontos, selecione o tipo de ajuste a partir dos pontos adquiridos<br/></span><span style=\" font-size:10pt; font-weight:700;\">9\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style=\""
                        " font-size:10pt; font-weight:700;\">Finalizar</span><span style=\" font-size:10pt;\"> para encerrar o ensaio est\u00e1tico </span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("StaticHelp", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:700;\">Instru\u00e7\u00f5es para o ensaio de calibra\u00e7\u00e3o est\u00e1tico</span></p></body></html>", None))
    # retranslateUi

