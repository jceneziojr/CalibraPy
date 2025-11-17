# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalibraPyDVQuch.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QWidget)

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
"\n"
"QPushButton#help_b{\n"
"	image: url(:/imgs/imgs/help.png);\n"
"}\n"
"\n"
"\n"
"QPushButton#help_b_2{\n"
"	image: url(:/imgs/imgs/help.png);\n"
"}\n"
"")
        self.centralwidget = QWidget(CalibraPy)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.estatico = QWidget(self.tab)
        self.estatico.setObjectName(u"estatico")
        self.estatico.setEnabled(True)
        self.gridLayout_3 = QGridLayout(self.estatico)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget_3 = QWidget(self.estatico)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_5 = QGridLayout(self.widget_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.acq_b = QPushButton(self.widget_3)
        self.acq_b.setObjectName(u"acq_b")
        self.acq_b.setEnabled(False)
        self.acq_b.setMinimumSize(QSize(0, 23))
        self.acq_b.setMaximumSize(QSize(100, 23))

        self.gridLayout_5.addWidget(self.acq_b, 0, 0, 1, 1, Qt.AlignHCenter)

        self.status_l = QLabel(self.widget_3)
        self.status_l.setObjectName(u"status_l")
        self.status_l.setMinimumSize(QSize(0, 23))
        self.status_l.setMaximumSize(QSize(16777215, 23))

        self.gridLayout_5.addWidget(self.status_l, 1, 0, 1, 1, Qt.AlignHCenter)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 50))
        self.widget_4.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_6 = QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.redo_point_b = QPushButton(self.widget_4)
        self.redo_point_b.setObjectName(u"redo_point_b")
        self.redo_point_b.setEnabled(False)

        self.gridLayout_6.addWidget(self.redo_point_b, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.next_point_b = QPushButton(self.widget_4)
        self.next_point_b.setObjectName(u"next_point_b")
        self.next_point_b.setEnabled(False)

        self.gridLayout_6.addWidget(self.next_point_b, 0, 2, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalSpacer_3 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.widget_4, 2, 0, 1, 1, Qt.AlignHCenter)


        self.gridLayout_3.addWidget(self.widget_3, 2, 0, 1, 1)

        self.widget_5 = QWidget(self.estatico)
        self.widget_5.setObjectName(u"widget_5")
        self.gridLayout_7 = QGridLayout(self.widget_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.signal_plot = PlotWidget(self.widget_5)
        self.signal_plot.setObjectName(u"signal_plot")
        self.signal_plot.setMinimumSize(QSize(300, 0))
        self.signal_plot.setMaximumSize(QSize(300, 16777215))

        self.gridLayout_7.addWidget(self.signal_plot, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.widget_5, 1, 0, 1, 1)

        self.widget_2 = QWidget(self.estatico)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 50))
        self.widget_2.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_4 = QGridLayout(self.widget_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.config_acq_b = QPushButton(self.widget_2)
        self.config_acq_b.setObjectName(u"config_acq_b")
        self.config_acq_b.setMinimumSize(QSize(200, 23))
        self.config_acq_b.setMaximumSize(QSize(200, 23))

        self.gridLayout_4.addWidget(self.config_acq_b, 0, 0, 1, 1, Qt.AlignLeft)

        self.help_b = QPushButton(self.widget_2)
        self.help_b.setObjectName(u"help_b")
        self.help_b.setMinimumSize(QSize(23, 23))
        self.help_b.setMaximumSize(QSize(23, 23))

        self.gridLayout_4.addWidget(self.help_b, 0, 2, 1, 1)

        self.start_acq = QPushButton(self.widget_2)
        self.start_acq.setObjectName(u"start_acq")
        self.start_acq.setEnabled(False)
        self.start_acq.setMinimumSize(QSize(200, 23))
        self.start_acq.setMaximumSize(QSize(200, 23))

        self.gridLayout_4.addWidget(self.start_acq, 0, 1, 1, 1, Qt.AlignRight)


        self.gridLayout_3.addWidget(self.widget_2, 0, 0, 1, 1, Qt.AlignHCenter)

        self.points_plot = PlotWidget(self.estatico)
        self.points_plot.setObjectName(u"points_plot")

        self.gridLayout_3.addWidget(self.points_plot, 3, 0, 1, 1)


        self.gridLayout_9.addWidget(self.estatico, 0, 0, 1, 1)

        self.widget_6 = QWidget(self.tab)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMinimumSize(QSize(0, 50))
        self.widget_6.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_8 = QGridLayout(self.widget_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.finish_stat_b = QPushButton(self.widget_6)
        self.finish_stat_b.setObjectName(u"finish_stat_b")
        self.finish_stat_b.setEnabled(False)
        self.finish_stat_b.setMinimumSize(QSize(0, 23))
        self.finish_stat_b.setMaximumSize(QSize(16777215, 23))

        self.gridLayout_8.addWidget(self.finish_stat_b, 0, 3, 3, 2)

        self.ajuste_combo = QComboBox(self.widget_6)
        self.ajuste_combo.addItem("")
        self.ajuste_combo.addItem("")
        self.ajuste_combo.addItem("")
        self.ajuste_combo.setObjectName(u"ajuste_combo")
        self.ajuste_combo.setEnabled(True)

        self.gridLayout_8.addWidget(self.ajuste_combo, 0, 1, 3, 2)

        self.label_2 = QLabel(self.widget_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 23))
        self.label_2.setMaximumSize(QSize(100, 23))

        self.gridLayout_8.addWidget(self.label_2, 0, 0, 3, 1)


        self.gridLayout_9.addWidget(self.widget_6, 1, 0, 1, 1, Qt.AlignHCenter)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_16 = QGridLayout(self.tab_2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.dinamico = QWidget(self.tab_2)
        self.dinamico.setObjectName(u"dinamico")
        self.dinamico.setEnabled(True)
        self.gridLayout_10 = QGridLayout(self.dinamico)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.widget_11 = QWidget(self.dinamico)
        self.widget_11.setObjectName(u"widget_11")
        self.gridLayout_12 = QGridLayout(self.widget_11)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.widget_12 = QWidget(self.widget_11)
        self.widget_12.setObjectName(u"widget_12")
        self.gridLayout_17 = QGridLayout(self.widget_12)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label = QLabel(self.widget_12)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 23))
        self.label.setMaximumSize(QSize(120, 23))

        self.gridLayout_17.addWidget(self.label, 0, 0, 1, 1)

        self.delay_ajuste = QDoubleSpinBox(self.widget_12)
        self.delay_ajuste.setObjectName(u"delay_ajuste")
        self.delay_ajuste.setMinimumSize(QSize(0, 23))
        self.delay_ajuste.setMaximumSize(QSize(16777215, 23))
        self.delay_ajuste.setMaximum(10.000000000000000)
        self.delay_ajuste.setSingleStep(0.500000000000000)
        self.delay_ajuste.setValue(4.000000000000000)

        self.gridLayout_17.addWidget(self.delay_ajuste, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.widget_12, 0, 1, 1, 1)

        self.widget_8 = QWidget(self.widget_11)
        self.widget_8.setObjectName(u"widget_8")
        self.gridLayout_15 = QGridLayout(self.widget_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_3 = QLabel(self.widget_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 23))
        self.label_3.setMaximumSize(QSize(120, 23))

        self.gridLayout_15.addWidget(self.label_3, 0, 0, 1, 1)

        self.dinamica_combo = QComboBox(self.widget_8)
        self.dinamica_combo.addItem("")
        self.dinamica_combo.addItem("")
        self.dinamica_combo.addItem("")
        self.dinamica_combo.addItem("")
        self.dinamica_combo.addItem("")
        self.dinamica_combo.setObjectName(u"dinamica_combo")
        self.dinamica_combo.setEnabled(True)
        self.dinamica_combo.setMinimumSize(QSize(0, 23))
        self.dinamica_combo.setMaximumSize(QSize(16777215, 23))

        self.gridLayout_15.addWidget(self.dinamica_combo, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.widget_8, 0, 0, 1, 1)

        self.finish_din_b = QPushButton(self.widget_11)
        self.finish_din_b.setObjectName(u"finish_din_b")
        self.finish_din_b.setEnabled(False)
        self.finish_din_b.setMinimumSize(QSize(0, 23))
        self.finish_din_b.setMaximumSize(QSize(16777215, 23))

        self.gridLayout_12.addWidget(self.finish_din_b, 0, 5, 1, 1)


        self.gridLayout_10.addWidget(self.widget_11, 3, 0, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        self.widget_7 = QWidget(self.dinamico)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(0, 50))
        self.widget_7.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_11 = QGridLayout(self.widget_7)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.config_acq_b_2 = QPushButton(self.widget_7)
        self.config_acq_b_2.setObjectName(u"config_acq_b_2")
        self.config_acq_b_2.setMinimumSize(QSize(200, 23))
        self.config_acq_b_2.setMaximumSize(QSize(200, 23))

        self.gridLayout_11.addWidget(self.config_acq_b_2, 0, 0, 1, 1, Qt.AlignLeft)

        self.help_b_2 = QPushButton(self.widget_7)
        self.help_b_2.setObjectName(u"help_b_2")
        self.help_b_2.setMinimumSize(QSize(23, 23))
        self.help_b_2.setMaximumSize(QSize(23, 23))

        self.gridLayout_11.addWidget(self.help_b_2, 0, 2, 1, 1)

        self.start_acq_2 = QPushButton(self.widget_7)
        self.start_acq_2.setObjectName(u"start_acq_2")
        self.start_acq_2.setEnabled(False)
        self.start_acq_2.setMinimumSize(QSize(200, 23))
        self.start_acq_2.setMaximumSize(QSize(200, 23))

        self.gridLayout_11.addWidget(self.start_acq_2, 0, 1, 1, 1, Qt.AlignRight)


        self.gridLayout_10.addWidget(self.widget_7, 0, 0, 1, 1, Qt.AlignHCenter)

        self.widget_9 = QWidget(self.dinamico)
        self.widget_9.setObjectName(u"widget_9")
        self.gridLayout_13 = QGridLayout(self.widget_9)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.widget_10 = QWidget(self.widget_9)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setMinimumSize(QSize(0, 50))
        self.widget_10.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_14 = QGridLayout(self.widget_10)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.redo_test_b = QPushButton(self.widget_10)
        self.redo_test_b.setObjectName(u"redo_test_b")
        self.redo_test_b.setEnabled(False)

        self.gridLayout_14.addWidget(self.redo_test_b, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)


        self.gridLayout_13.addWidget(self.widget_10, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignTop)


        self.gridLayout_10.addWidget(self.widget_9, 1, 0, 1, 1)

        self.test_plot = PlotWidget(self.dinamico)
        self.test_plot.setObjectName(u"test_plot")

        self.gridLayout_10.addWidget(self.test_plot, 2, 0, 1, 1)


        self.gridLayout_16.addWidget(self.dinamico, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 50))
        self.widget.setMaximumSize(QSize(16777215, 50))
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
        self.device_label.setMaximumSize(QSize(150, 30))

        self.gridLayout_2.addWidget(self.device_label, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.reload_devices = QPushButton(self.widget)
        self.reload_devices.setObjectName(u"reload_devices")
        self.reload_devices.setMinimumSize(QSize(23, 23))
        self.reload_devices.setMaximumSize(QSize(23, 23))

        self.gridLayout_2.addWidget(self.reload_devices, 0, 3, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.export_report_b = QPushButton(self.centralwidget)
        self.export_report_b.setObjectName(u"export_report_b")
        self.export_report_b.setEnabled(False)
        self.export_report_b.setMinimumSize(QSize(0, 30))
        self.export_report_b.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.export_report_b, 2, 0, 1, 1, Qt.AlignHCenter|Qt.AlignBottom)

        CalibraPy.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CalibraPy)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        CalibraPy.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CalibraPy)
        self.statusbar.setObjectName(u"statusbar")
        CalibraPy.setStatusBar(self.statusbar)

        self.retranslateUi(CalibraPy)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CalibraPy)
    # setupUi

    def retranslateUi(self, CalibraPy):
        CalibraPy.setWindowTitle(QCoreApplication.translate("CalibraPy", u"CalibraPy", None))
        self.acq_b.setText(QCoreApplication.translate("CalibraPy", u"Adquirir ponto", None))
        self.status_l.setText(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Ponto atual: X   (Y de Z)</span></p></body></html>", None))
        self.redo_point_b.setText(QCoreApplication.translate("CalibraPy", u"Refazer ponto", None))
        self.next_point_b.setText(QCoreApplication.translate("CalibraPy", u"Pr\u00f3ximo ponto", None))
        self.config_acq_b.setText(QCoreApplication.translate("CalibraPy", u"Configurar aquisi\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.help_b.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Ajuda sobre a calibra\u00e7\u00e3o est\u00e1tica.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.help_b.setText("")
        self.start_acq.setText(QCoreApplication.translate("CalibraPy", u"Come\u00e7ar aquisi\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.widget_6.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.finish_stat_b.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Finaliza a aquisi\u00e7\u00e3o e calcula as caracter\u00edsticas est\u00e1ticas do seu sensor.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.finish_stat_b.setText(QCoreApplication.translate("CalibraPy", u"Finalizar", None))
        self.ajuste_combo.setItemText(0, QCoreApplication.translate("CalibraPy", u"Primeiro grau (reta)", None))
        self.ajuste_combo.setItemText(1, QCoreApplication.translate("CalibraPy", u"Segundo grau (curva)", None))
        self.ajuste_combo.setItemText(2, QCoreApplication.translate("CalibraPy", u"Terceiro grau (curva)", None))

#if QT_CONFIG(tooltip)
        self.ajuste_combo.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Escolha o tipo de ajuste para a curva de calibra\u00e7\u00e3o est\u00e1tica (a partir dos pontos no gr\u00e1fico acima).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Escolha o tipo de ajuste para a curva de calibra\u00e7\u00e3o est\u00e1tica (a partir dos pontos no gr\u00e1fico acima).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Tipo de ajuste</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("CalibraPy", u"Est\u00e1tico", None))
#if QT_CONFIG(tooltip)
        self.widget_11.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.widget_12.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Existe um delay da comunica\u00e7\u00e3o serial arduino de cerca de 4 segundos. Ajuste esse tempo a partir dos dados obtidos.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Tempo de atraso</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.delay_ajuste.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Escolha o tipo de ajuste para a curva de calibra\u00e7\u00e3o est\u00e1tica (a partir dos pontos no gr\u00e1fico acima).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Tipo de din\u00e2mica</span></p></body></html>", None))
        self.dinamica_combo.setItemText(0, QCoreApplication.translate("CalibraPy", u"Ordem zero", None))
        self.dinamica_combo.setItemText(1, QCoreApplication.translate("CalibraPy", u"Primeira ordem", None))
        self.dinamica_combo.setItemText(2, QCoreApplication.translate("CalibraPy", u"Segunda ordem subamortecido", None))
        self.dinamica_combo.setItemText(3, QCoreApplication.translate("CalibraPy", u"Segunda ordem criticamente amortecido", None))
        self.dinamica_combo.setItemText(4, QCoreApplication.translate("CalibraPy", u"Segunda ordem sobreamortecido", None))

#if QT_CONFIG(tooltip)
        self.dinamica_combo.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Escolha o tipo de ajuste para a curva de calibra\u00e7\u00e3o est\u00e1tica (a partir dos pontos no gr\u00e1fico acima).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.finish_din_b.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Finaliza a aquisi\u00e7\u00e3o e calcula as caracter\u00edsticas est\u00e1ticas do seu sensor.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.finish_din_b.setText(QCoreApplication.translate("CalibraPy", u"Finalizar", None))
        self.config_acq_b_2.setText(QCoreApplication.translate("CalibraPy", u"Configurar aquisi\u00e7\u00e3o", None))
#if QT_CONFIG(tooltip)
        self.help_b_2.setToolTip(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p>Ajuda sobre a calibra\u00e7\u00e3o est\u00e1tica.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.help_b_2.setText("")
        self.start_acq_2.setText(QCoreApplication.translate("CalibraPy", u"Come\u00e7ar aquisi\u00e7\u00e3o", None))
        self.redo_test_b.setText(QCoreApplication.translate("CalibraPy", u"Refazer ensaio", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("CalibraPy", u"Din\u00e2mico", None))
        self.device_label.setText(QCoreApplication.translate("CalibraPy", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Selecione o Arduino</span></p></body></html>", None))
        self.reload_devices.setText("")
        self.export_report_b.setText(QCoreApplication.translate("CalibraPy", u"Exportar Relat\u00f3rio", None))
    # retranslateUi

