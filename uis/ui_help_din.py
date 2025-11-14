# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help_dinHbjjSE.ui'
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

class Ui_DynamicHelp(object):
    def setupUi(self, DynamicHelp):
        if not DynamicHelp.objectName():
            DynamicHelp.setObjectName(u"DynamicHelp")
        DynamicHelp.resize(743, 172)
        self.gridLayout = QGridLayout(DynamicHelp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(DynamicHelp)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label = QLabel(DynamicHelp)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignTop)

        self.line = QFrame(DynamicHelp)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)


        self.retranslateUi(DynamicHelp)

        QMetaObject.connectSlotsByName(DynamicHelp)
    # setupUi

    def retranslateUi(self, DynamicHelp):
        DynamicHelp.setWindowTitle(QCoreApplication.translate("DynamicHelp", u"Ajuda", None))
        self.label_2.setText(QCoreApplication.translate("DynamicHelp", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:700;\">1\u00ba -</span><span style=\" font-size:10pt;\"> Selecione sua placa Arduino<br/></span><span style=\" font-size:10pt; font-weight:700;\">2\u00ba -</span><span style=\" font-size:10pt;\"> Pressione o bot\u00e3o </span><span style=\" font-size:10pt; font-weight:700;\">Configurar aquisi\u00e7\u00e3o</span><span style=\" font-size:10pt;\"> para ajustar o tempo de sess\u00e3o e a amplitude do degrau que voc\u00ea ir\u00e1 aplicar<br/></span><span style=\" font-size:10pt; font-weight:700;\">3\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style=\" font-size:10pt; font-weight:700;\">Come\u00e7ar aquisi\u00e7\u00e3o</span><span style=\" font-size:10pt;\"><br/></span><span style=\" font-size:10pt; font-weight:700;\">4\u00ba - </span><span style=\" font-size:10pt;\">Aplique o degrau no seu sistema, com a amplitude que voc\u00ea determinou</span><span style=\" font-size:10pt;\"><br/></span><span style=\" fon"
                        "t-size:10pt; font-weight:700;\">5\u00ba -</span><span style=\" font-size:10pt;\"> Observe os dados coletados no gr\u00e1fico. Se n\u00e3o estiver satisfeito, pressione </span><span style=\" font-size:10pt; font-weight:700;\">Refazer ensaio</span><span style=\" font-size:10pt;\"><br/></span><span style=\" font-size:10pt; font-weight:700;\">6\u00ba -</span><span style=\" font-size:10pt;\"> De acordo com os dados coletados, selecione um tipo de din\u00e2mica para o algoritmo de identifica\u00e7\u00e3o<br/></span><span style=\" font-size:10pt; font-weight:700;\">7\u00ba -</span><span style=\" font-size:10pt;\"> Pressione </span><span style=\" font-size:10pt; font-weight:700;\">Finalizar</span><span style=\" font-size:10pt;\"> para encerrar o ensaio din\u00e2mico</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("DynamicHelp", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:700;\">Instru\u00e7\u00f5es para o ensaio de calibra\u00e7\u00e3o din\u00e2mico</span></p></body></html>", None))
    # retranslateUi

