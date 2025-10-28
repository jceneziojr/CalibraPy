# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configszVveyG.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_Configs(object):
    def setupUi(self, Configs):
        if not Configs.objectName():
            Configs.setObjectName(u"Configs")
        Configs.resize(364, 329)
        self.gridLayout = QGridLayout(Configs)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(Configs)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pontos = QWidget(self.widget)
        self.pontos.setObjectName(u"pontos")
        self.gridLayout_4 = QGridLayout(self.pontos)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.widget_2 = QWidget(self.pontos)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.point_input = QLineEdit(self.widget_2)
        self.point_input.setObjectName(u"point_input")
        self.point_input.setMinimumSize(QSize(70, 0))
        self.point_input.setMaximumSize(QSize(70, 16777215))
        self.point_input.setLayoutDirection(Qt.LeftToRight)
        self.point_input.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.point_input, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.widget_2, 0, 0, 1, 1)

        self.widget_3 = QWidget(self.pontos)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_5 = QGridLayout(self.widget_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.points_list = QListWidget(self.widget_3)
        self.points_list.setObjectName(u"points_list")

        self.gridLayout_5.addWidget(self.points_list, 0, 0, 1, 1)

        self.remove_point_b = QPushButton(self.widget_3)
        self.remove_point_b.setObjectName(u"remove_point_b")
        self.remove_point_b.setMaximumSize(QSize(100, 16777215))
        self.remove_point_b.setAutoRepeatInterval(97)
        self.remove_point_b.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.remove_point_b, 1, 0, 1, 1, Qt.AlignHCenter)


        self.gridLayout_4.addWidget(self.widget_3, 0, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_2.addWidget(self.pontos, 1, 0, 1, 1)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_6 = QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.acq_points = QLineEdit(self.widget_4)
        self.acq_points.setObjectName(u"acq_points")
        self.acq_points.setMinimumSize(QSize(70, 0))
        self.acq_points.setMaximumSize(QSize(70, 16777215))
        self.acq_points.setLayoutDirection(Qt.LeftToRight)
        self.acq_points.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.acq_points, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_4, 2, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.finish_b = QPushButton(self.widget)
        self.finish_b.setObjectName(u"finish_b")
        self.finish_b.setMinimumSize(QSize(100, 0))
        self.finish_b.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.finish_b.setFont(font)
        self.finish_b.setCheckable(False)
        self.finish_b.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.finish_b, 3, 0, 1, 1, Qt.AlignHCenter)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Configs)

        QMetaObject.connectSlotsByName(Configs)
    # setupUi

    def retranslateUi(self, Configs):
        Configs.setWindowTitle(QCoreApplication.translate("Configs", u"Configura\u00e7\u00f5es da calibra\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.widget_2.setToolTip(QCoreApplication.translate("Configs", u"<html><head/><body><p align=\"justify\">Insira no campo de texto os pontos de calibra\u00e7\u00e3o em ordem crescente. Durante o processo de calibra\u00e7\u00e3o, ajuste o sensor nos valores correspondentes a cada ponto definido, conforme solicitado pelo programa.</p><p align=\"justify\">Ex: para calibrar um LVDT, imagine que voc\u00ea defina os pontos 0, 5 e 10, todos em cent\u00edmetros. Quando o programa solicitar, posicione o sensor nos respectivos comprimentos.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Inserir Ponto</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.remove_point_b.setToolTip(QCoreApplication.translate("Configs", u"<html><head/><body><p align=\"justify\"><div style=\\\"width: 300px;\\\">Selecione um ponto na lista e pressione o bot\u00e3o para remov\u00ea-lo.</div></p></body></html>\n"
"\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.remove_point_b.setText(QCoreApplication.translate("Configs", u"Remover Ponto", None))
#if QT_CONFIG(tooltip)
        self.widget_4.setToolTip(QCoreApplication.translate("Configs", u"<html><head/><body><p>Defina quantas aquisi\u00e7\u00f5es ser\u00e3o feitas por ponto. Com esta fun\u00e7\u00e3o, podemos rastrear informa\u00e7\u00f5es como repetibilidade. O n\u00famero de aquisi\u00e7\u00f5es por ponto pode estar entre 1 e 10.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Aquisi\u00e7\u00f5es por ponto</span></p></body></html>", None))
        self.acq_points.setText(QCoreApplication.translate("Configs", u"5", None))
        self.label.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Configura\u00e7\u00e3o da calibra\u00e7\u00e3o</span></p></body></html>", None))
        self.finish_b.setText(QCoreApplication.translate("Configs", u"Finalizar", None))
    # retranslateUi

