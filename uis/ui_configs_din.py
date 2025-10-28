# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configs_dinAgnxRN.ui'
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

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_6 = QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.amp_deg = QLineEdit(self.widget_4)
        self.amp_deg.setObjectName(u"amp_deg")
        self.amp_deg.setMinimumSize(QSize(70, 0))
        self.amp_deg.setMaximumSize(QSize(70, 16777215))
        self.amp_deg.setLayoutDirection(Qt.LeftToRight)
        self.amp_deg.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.amp_deg, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_4, 1, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.tempo_sesh = QLineEdit(self.widget_2)
        self.tempo_sesh.setObjectName(u"tempo_sesh")
        self.tempo_sesh.setMinimumSize(QSize(70, 0))
        self.tempo_sesh.setMaximumSize(QSize(70, 16777215))
        self.tempo_sesh.setLayoutDirection(Qt.LeftToRight)
        self.tempo_sesh.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.tempo_sesh, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(Configs)

        QMetaObject.connectSlotsByName(Configs)
    # setupUi

    def retranslateUi(self, Configs):
        Configs.setWindowTitle(QCoreApplication.translate("Configs", u"Configura\u00e7\u00f5es da calibra\u00e7\u00e3o", None))
        self.finish_b.setText(QCoreApplication.translate("Configs", u"Finalizar", None))
#if QT_CONFIG(tooltip)
        self.widget_4.setToolTip(QCoreApplication.translate("Configs", u"<html><head/><body><p>Defina a amplitude do degrau que ser\u00e1 aplicado na entrada. Ex: se o seu degrau no LVDT variar de 0 cm at\u00e9 10 cm, a amplitude ser\u00e1 10.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Amplitude do degrau</span></p></body></html>", None))
        self.amp_deg.setText("")
        self.label.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Configura\u00e7\u00e3o da calibra\u00e7\u00e3o</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.widget_2.setToolTip(QCoreApplication.translate("Configs", u"<html><head/><body><p>Defina o tempo total da aquisi\u00e7\u00e3o do ensaio din\u00e2mico. Tempos muito curtos podem impedir o funcionamento correto do <span style=\" font-style:italic;\">script</span>, dependendo da din\u00e2mica do seu sistema.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Configs", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Tempo da sess\u00e3o</span></p></body></html>", None))
        self.tempo_sesh.setText("")
    # retranslateUi

