# comando resources pyside6-rcc resources.qrc -o resources_rc.py
#   precisa ir no arquivo Ui e mudar a linha de import para from . import resources_rc

import os
import sys
import time
import serial
import serial.tools.list_ports
import numpy as np

from uis.ui_CalibraPy import Ui_CalibraPy

from PySide6 import QtWidgets
from PySide6.QtGui import QFont

from utils.get_signal import GetSignal
from utils.config_stat import StatConfigDialog


class MainWindow(QtWidgets.QMainWindow, Ui_CalibraPy):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized()

        # conectando sinais
        self.reload_devices.released.connect(self.update_com_ports)
        self.start_acq.released.connect(self._open_serial)
        self.config_acq_b.released.connect(self.open_config_dialog)
        self.next_point_b.released.connect(self.next_point_handle)
        self.redo_point_b.released.connect(self.redo_point_handle)

        # configurações iniciais
        self.acquisition_points = 5  # numero de aquisições em cada ponto
        self.pontos = None  # Lista com os pontos da calibração estática
        self.update_com_ports()

        # arrumando texto
        font = QFont()
        font.setPointSize(12)  # tamanho da fonte
        font.setBold(True)  # deixa em negrito
        self.status_l.setFont(font)
        self.status_l.setText("-----------------")

        # ajustes do plot
        self.signal_plot.setXRange(0, 100, padding=0.02)
        self.signal_plot.setYRange(0, 5, padding=0.02)
        self.signal_plot.setMouseEnabled(x=False, y=False)
        self.signal_plot.hideButtons()
        self.signal_plot.getPlotItem().hideAxis('bottom')

        self.points_plot.setYRange(0, 5, padding=0.02)
        self.points_plot.setMouseEnabled(x=False, y=False)
        self.points_plot.hideButtons()

        # configuração processo de aquisição estatico
        self.acq_index = None
        self.sequence_points = None
        self.forward_dict = None
        self.backward_dict = None
        self.fwd_avg = None
        self.bwd_avg = None
        self.done_last_point = False

        # plot dos pontos estaticos
        self.fwd_curve = self.points_plot.plot([], [], pen=None, symbol='o', symbolBrush='r', name='Fwd')
        self.bwd_curve = self.points_plot.plot([], [], pen=None, symbol='x', symbolBrush='b', name='Bwd')
        self.fwd_x = []
        self.bwd_x = []

    def open_config_dialog(self):
        config_dialog = StatConfigDialog()
        config_dialog.exec()

        self.acquisition_points = config_dialog.pontos_acq
        self.pontos = config_dialog.pontos

        # print(f"num pontos: {self.acquisition_points}")
        # print(f"pontos: {self.pontos}")
        self.start_acq.setEnabled(True)
        self.points_plot.setXRange(self.pontos[0], self.pontos[-1], padding=0.02)

    def startup_acquisition_process(self):
        self.acq_index = 0
        self.sequence_points = self.pontos + self.pontos[::-1]
        self.forward_dict = dict()
        self.backward_dict = dict()
        self.fwd_avg = list()
        self.bwd_avg = list()

        self.status_l.setText(
            f"Ponto atual: {self.sequence_points[self.acq_index]} ({self.acq_index + 1} de {len(self.sequence_points)})")

    def update_com_ports(self):
        self.com_ports = [i.description for i in serial.tools.list_ports.comports()]
        selected = self.device_combo.currentText()

        self.device_combo.clear()
        self.device_combo.addItems(self.com_ports)

        index_arduino = next(
            (i for i, desc in enumerate(self.com_ports)
             if "arduino" in desc.lower() or "com10" in desc.lower()),  # TIRAR COM10 NO FINAL
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
        p1 = self.signal_plot.plot()

        self.get_signal = GetSignal(self.serial)
        self.get_signal.data_ready.connect(lambda data: p1.setData(data))
        self.get_signal.samples_ready.connect(self.handle_samples_ready)  # conecta o retorno pontual
        self.start_acq.setEnabled(False)

        # conecta o botão de aquisição pontual (acq_b)
        self.acq_b.released.connect(self.on_acq_button_pressed)

        self.acq_b.setEnabled(True)
        self.startup_acquisition_process()

    def on_acq_button_pressed(self):
        # desabilita o botão enquanto a aquisição pontual está em curso (opcional)
        self.acq_b.setEnabled(False)
        # solicita N pontos com intervalo de 0.5s (substitua self.acquisition_points conforme necessário)
        self.get_signal.request_samples(self.acquisition_points, interval=0.5)

    def handle_static_acq_process(self, samples):
        mean = float(np.mean(samples))
        if self.acq_index < len(self.sequence_points) // 2:
            # indo
            self.forward_dict[self.sequence_points[self.acq_index]] = samples
            self.fwd_avg.append(mean)
            self.fwd_x.append(self.sequence_points[self.acq_index])

        else:
            # voltando
            self.backward_dict[self.sequence_points[self.acq_index]] = samples
            self.bwd_avg.append(mean)
            self.bwd_x.append(self.sequence_points[self.acq_index])

    def handle_samples_ready(self, samples: list):
        # método pra cuidar dos dados coletados
        # print(f"amostras recebidas pela thread: {samples}")
        self.handle_static_acq_process(samples)
        self.redo_point_b.setEnabled(True)
        if not self.acq_index == len(self.sequence_points) - 1:
            self.next_point_b.setEnabled(True)
        else:
            self.finish_stat_b.setEnabled(True)

        self.plot_static_points()

    def plot_static_points(self):
        print("=====================")
        print("========PLOT=========")
        print("=====================")
        if self.acq_index < len(self.sequence_points) // 2:
            print(self.fwd_x)
            print(self.fwd_avg)
            self.fwd_curve.setData(self.fwd_x, self.fwd_avg)
        else:
            self.bwd_curve.setData(self.bwd_x, self.bwd_avg)

    def redo_point_handle(self):
        print("=====================")
        print("========REDO=========")
        print("=====================")
        if self.acq_index < len(self.sequence_points) // 2:
            # indo
            del self.forward_dict[self.sequence_points[self.acq_index]]
            self.fwd_avg.pop()
            self.fwd_x.pop()
            print("passei aqui")

        else:
            # voltando
            del self.backward_dict[self.sequence_points[self.acq_index]]
            self.bwd_avg.pop()
            self.bwd_x.pop()

        self.plot_static_points()

        self.acq_b.setEnabled(True)
        self.redo_point_b.setEnabled(False)
        self.next_point_b.setEnabled(False)

    def next_point_handle(self):
        print("=====================")
        print("========NEXT=========")
        print("=====================")
        self.acq_b.setEnabled(True)
        self.redo_point_b.setEnabled(False)
        self.next_point_b.setEnabled(False)

        self.acq_index += 1
        self.status_l.setText(
            f"Ponto atual: {self.sequence_points[self.acq_index]} ({self.acq_index + 1} de {len(self.sequence_points)})")

    def exit_handle(self):
        # para a thread do GetSignal e espera terminar
        if hasattr(self, "get_signal"):
            self.get_signal.stop()
            # aguarda a threadpool processar(não sei se realmente precisa)
            self.get_signal.threadpool.waitForDone(2000)  # timeout em ms

        if hasattr(self, "serial") and self.serial.is_open:
            try:
                self.serial.close()
            except Exception:
                pass


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.aboutToQuit.connect(window.exit_handle)
sys.exit(app.exec())
