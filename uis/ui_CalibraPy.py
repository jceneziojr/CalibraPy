# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalibraPylGlcHB.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
                               QMainWindow, QMenuBar, QPushButton, QSizePolicy,
                               QSpacerItem, QStatusBar, QWidget)

from pyqtgraph import PlotWidget
from . import resources_rc


class Ui_CalibraPy(object):
    def setupUi(self, CalibraPy):
        if not CalibraPy.objectName():
            CalibraPy.setObjectName(u"CalibraPy")
        CalibraPy.resize(800, 600)
        CalibraPy.setStyleSheet(u"QPushButton#reload_devices{\n"
                                "	image: url(:/imgs/imgs/reload.png);\n"
                                "}\n"
                                "\n"
                                "QPushButton#reload_devices:hover{\n"
                                "	background-color: rgb(0, 50, 0);\n"
                                "}\n"
                                "\n"
                                "QPushButton#reload_devices:pressed{\n"
                                "	border: 2px solid rgb(255, 255, 255);\n"
                                "}")
        self.centralwidget = QWidget(CalibraPy)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.signal_plot = PlotWidget(self.centralwidget)
        self.signal_plot.setObjectName(u"signal_plot")

        self.gridLayout.addWidget(self.signal_plot, 2, 0, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.device_combo = QComboBox(self.widget)
        self.device_combo.setObjectName(u"device_combo")
        self.device_combo.setMinimumSize(QSize(300, 23))
        self.device_combo.setMaximumSize(QSize(300, 23))

        self.gridLayout_2.addWidget(self.device_combo, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.device_label = QLabel(self.widget)
        self.device_label.setObjectName(u"device_label")
        self.device_label.setMinimumSize(QSize(0, 30))
        self.device_label.setMaximumSize(QSize(120, 30))

        self.gridLayout_2.addWidget(self.device_label, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.reload_devices = QPushButton(self.widget)
        self.reload_devices.setObjectName(u"reload_devices")
        self.reload_devices.setMinimumSize(QSize(23, 23))
        self.reload_devices.setMaximumSize(QSize(23, 23))

        self.gridLayout_2.addWidget(self.reload_devices, 0, 3, 1, 1)

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.start_acq = QPushButton(self.centralwidget)
        self.start_acq.setObjectName(u"start_acq")
        self.start_acq.setMinimumSize(QSize(0, 23))
        self.start_acq.setMaximumSize(QSize(16777215, 23))

        self.gridLayout.addWidget(self.start_acq, 1, 0, 1, 1)

        self.stop_acq = QPushButton(self.centralwidget)
        self.stop_acq.setObjectName(u"stop_acq")

        self.gridLayout.addWidget(self.stop_acq, 3, 0, 1, 1)

        CalibraPy.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CalibraPy)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        CalibraPy.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CalibraPy)
        self.statusbar.setObjectName(u"statusbar")
        CalibraPy.setStatusBar(self.statusbar)

        self.retranslateUi(CalibraPy)

        QMetaObject.connectSlotsByName(CalibraPy)

    # setupUi

    def retranslateUi(self, CalibraPy):
        CalibraPy.setWindowTitle(QCoreApplication.translate("CalibraPy", u"MainWindow", None))
        self.device_label.setText(QCoreApplication.translate("CalibraPy", u"Selecione o Arduino", None))
        self.reload_devices.setText("")
        self.start_acq.setText(QCoreApplication.translate("CalibraPy", u"Come\u00e7ar aquisi\u00e7\u00e3o", None))
        self.stop_acq.setText(QCoreApplication.translate("CalibraPy", u"Parar aquisi\u00e7\u00e3o", None))
    # retranslateUi
