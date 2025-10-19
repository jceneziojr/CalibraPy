# comando resources pyside6-rcc resources.qrc -o resources_rc.py
#   precisa ir no arquivo Ui e mudar a linha de import para from . import resources_rc

import os
import sys
import time
import serial
import serial.tools.list_ports

from uis.ui_CalibraPy import Ui_CalibraPy

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QThreadPool, QSize
from utils.get_signal import GetSignal


class MainWindow(QtWidgets.QMainWindow, Ui_CalibraPy):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized()

        # Connecting Signals
        self.reload_devices.released.connect(self.update_com_ports)
        self.start_acq.released.connect(self._open_serial)

        # Setting the starting values for some widgets
        self.update_com_ports()

    def update_com_ports(self):
        self.com_ports = [i.description for i in serial.tools.list_ports.comports()]
        selected = self.device_combo.currentText()

        self.device_combo.clear()
        self.device_combo.addItems(self.com_ports)

        index_arduino = next(
            (i for i, desc in enumerate(self.com_ports) if "arduino" in desc.lower()),
            -1
        )

        if index_arduino != -1:
            self.device_combo.setCurrentIndex(index_arduino)
        else:
            index_current = self.device_combo.findText(selected)
            if index_current != -1:
                self.device_combo.setCurrentIndex(index_current)

    def _open_serial(self):
        """Opening ports for serial communication"""

        self.serial = serial.Serial()
        self.serial.dtr = True
        self.serial.baudrate = 115200
        self.serial.port = self.com_port = serial.tools.list_ports.comports()[
            self.com_ports.index(self.device_combo.currentText())
        ].name  # Defining port

        if not self.serial.isOpen():  # Open port if not openned
            self.serial.open()  # Opening port

        time.sleep(2)  # Wait for Arduino and Serial to start up
        self.start_acquisition()

    def start_acquisition(self):
        self.signal_plot.setXRange(0, 100, padding=0.02)
        self.signal_plot.setYRange(0, 5, padding=0.02)
        p1 = self.signal_plot.plot()
        self.get_signal = GetSignal(self.serial)
        self.get_signal.data_ready.connect(lambda data: p1.setData(data))
        self.start_acq.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
# with open("auxiliary_codes/style.qss", "r") as f:
#     _style = f.read()
#     app.setStyleSheet(_style)
app.exec()
