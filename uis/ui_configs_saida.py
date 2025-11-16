# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configs_saidaXmZFFA.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_ConfigsSaida(object):
    def setupUi(self, ConfigsSaida):
        if not ConfigsSaida.objectName():
            ConfigsSaida.setObjectName(u"ConfigsSaida")
        ConfigsSaida.resize(500, 238)
        self.gridLayout = QGridLayout(ConfigsSaida)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(ConfigsSaida)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_6 = QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.nome_input = QLineEdit(self.widget_4)
        self.nome_input.setObjectName(u"nome_input")
        self.nome_input.setMinimumSize(QSize(200, 0))
        self.nome_input.setMaximumSize(QSize(200, 16777215))
        self.nome_input.setLayoutDirection(Qt.LeftToRight)
        self.nome_input.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.nome_input, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_4, 1, 0, 1, 1)

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

        self.gridLayout_2.addWidget(self.finish_b, 4, 0, 1, 1, Qt.AlignHCenter)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.sensor_input = QLineEdit(self.widget_2)
        self.sensor_input.setObjectName(u"sensor_input")
        self.sensor_input.setMinimumSize(QSize(200, 0))
        self.sensor_input.setMaximumSize(QSize(200, 16777215))
        self.sensor_input.setLayoutDirection(Qt.LeftToRight)
        self.sensor_input.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.sensor_input, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 2, 0, 1, 1)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_4 = QGridLayout(self.widget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)

        self.unidade_input = QLineEdit(self.widget_3)
        self.unidade_input.setObjectName(u"unidade_input")
        self.unidade_input.setMinimumSize(QSize(200, 0))
        self.unidade_input.setMaximumSize(QSize(200, 16777215))
        self.unidade_input.setLayoutDirection(Qt.LeftToRight)
        self.unidade_input.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.unidade_input, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_3, 3, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        QWidget.setTabOrder(self.nome_input, self.sensor_input)
        QWidget.setTabOrder(self.sensor_input, self.unidade_input)
        QWidget.setTabOrder(self.unidade_input, self.finish_b)

        self.retranslateUi(ConfigsSaida)

        QMetaObject.connectSlotsByName(ConfigsSaida)
    # setupUi

    def retranslateUi(self, ConfigsSaida):
        ConfigsSaida.setWindowTitle(QCoreApplication.translate("ConfigsSaida", u"Configura\u00e7\u00f5es", None))
#if QT_CONFIG(tooltip)
        self.widget_4.setToolTip(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p>Nome da pessoa respons\u00e1vel pela calibra\u00e7\u00e3o</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Nome do respons\u00e1vel</span></p></body></html>", None))
        self.nome_input.setText("")
        self.label.setText(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Configura\u00e7\u00e3o do relat\u00f3rio</span></p></body></html>", None))
        self.finish_b.setText(QCoreApplication.translate("ConfigsSaida", u"Finalizar", None))
#if QT_CONFIG(tooltip)
        self.widget_2.setToolTip(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p>Nome do sensor calibrado</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Nome do sensor</span></p></body></html>", None))
        self.sensor_input.setText("")
#if QT_CONFIG(tooltip)
        self.widget_3.setToolTip(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p>Unidade de medida do mensurando (ex: ohm, graus, cm)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("ConfigsSaida", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Unidade do mensurando</span></p></body></html>", None))
        self.unidade_input.setText("")
    # retranslateUi

