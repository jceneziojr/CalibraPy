# comando resources pyside6-rcc resources.qrc -o resources_rc.py
#   precisa ir no arquivo Ui e mudar a linha de import para from . import resources_rc
# tem algum bug, que na segunda execução o ponto é aquisitado todas as vezes. tem que checar oq acontece
#   mas por enquanto, fechar e abrir pra cada

import os
import sys
import time
import serial
import unicodedata
import serial.tools.list_ports
import numpy as np
from report_codes.static import CaracteristicasEstaticas

from report_codes.id_0_ordem import OrdemZero
from report_codes.id_1_ordem import PrimeiraOrdem
from report_codes.id_2_ordem_subam import SundaresanSubamortecido
from report_codes.id_2_ordem_sobream import SundaresanSobreamortecido
from report_codes.id_2_ordem_critico import SundaresanCriticamenteAmortecido
from report_codes.report_generator import RelatorioCalibracao
from uis.ui_CalibraPy import Ui_CalibraPy

from PySide6 import QtWidgets
from PySide6.QtGui import QFont

from utils.get_signal import GetSignal
from utils.config_stat import StatConfigDialog
from utils.config_din import DinConfigDialog
from utils.din_acquisition import DynamicTest
from utils.help_dialogs import DynamicHelp, StaticHelp
from utils.export_config import ExportConfig


def ajustar_str(texto):
    # remover acentos
    texto_sem_acento = unicodedata.normalize("NFKD", texto)
    texto_sem_acento = "".join(c for c in texto_sem_acento if not unicodedata.combining(c))
    return texto_sem_acento.replace(" ", "_")  # substitui espaço por _


class MainWindow(QtWidgets.QMainWindow, Ui_CalibraPy):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized()

        self.serial = None

        # conectando sinais estatico
        self.reload_devices.released.connect(self.update_com_ports)
        self.start_acq.released.connect(self.stat_open_serial)
        self.config_acq_b.released.connect(self.open_config_dialog)
        self.next_point_b.released.connect(self.next_point_handle)
        self.redo_point_b.released.connect(self.redo_point_handle)
        self.finish_stat_b.released.connect(self.finish_stat_handle)
        self.help_b.released.connect(self.open_help_s)

        # conectando sinais dinamico
        self.config_acq_b_2.released.connect(self.open_config_dialog_2)
        self.start_acq_2.released.connect(self.start_din_test)
        self.redo_test_b.released.connect(self.redo_teste_handle)
        self.finish_din_b.released.connect(self.finish_din_test_handle)
        self.help_b_2.released.connect(self.open_help_d)

        # variaveis do report
        self._nome = None
        self._sensor = None
        self._unidade = None
        self._destino = None
        self.export_report_b.released.connect(self.generate_report)

        # configurações iniciais estatico
        self.acquisition_points = 5  # numero de aquisições em cada ponto
        self.pontos = None  # Lista com os pontos da calibração estática
        self.static_report_done = False

        # configurações iniciais dinamico
        self.amplitude_degrau = None
        self.tempo_sessao = None
        self.dados_plot_din = list()
        self.first_point_done = False
        self.din_x = list()
        self.din_teste = None
        self.dynamic_report_done = False

        # arrumando texto
        font = QFont()
        font.setPointSize(12)  # tamanho da fonte
        font.setBold(True)  # deixa em negrito
        self.status_l.setFont(font)
        self.status_l.setText("-----------------")

        # ajustes do plot estatico
        self.signal_plot.setXRange(0, 100, padding=0.02)
        self.signal_plot.setYRange(0, 5, padding=0.02)
        self.signal_plot.setMouseEnabled(x=False, y=False)
        self.signal_plot.hideButtons()
        self.signal_plot.getPlotItem().hideAxis('bottom')

        self.points_plot.setYRange(0, 5, padding=0.02)
        self.points_plot.setMouseEnabled(x=False, y=False)
        self.points_plot.hideButtons()

        # ajustes do plot estatico
        self.test_plot.setYRange(0, 5, padding=0.02)
        self.test_plot.setMouseEnabled(x=False, y=False)
        self.test_plot.hideButtons()

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

        self.update_com_ports()

    def open_config_dialog(self):
        config_dialog = StatConfigDialog()
        if self.pontos and self.acquisition_points:
            for p in self.pontos:
                config_dialog.points_list.addItem(str(p))
            config_dialog.acq_points.setText(str(self.acquisition_points))
        config_dialog.exec()

        self.acquisition_points = config_dialog.pontos_acq
        self.pontos = config_dialog.pontos

        # print(f"num pontos: {self.acquisition_points}")
        # print(f"pontos: {self.pontos}")
        if len(self.pontos) > 1:
            self.start_acq.setEnabled(True)
        self.finish_stat_b.setEnabled(False)
        self.points_plot.clear()
        self.points_plot.setXRange(self.pontos[0], self.pontos[-1], padding=0.02)

    def open_config_dialog_2(self):
        config_dialog = DinConfigDialog()
        if self.amplitude_degrau and self.tempo_sessao:
            config_dialog.amp_deg.setText(str(self.amplitude_degrau))
            config_dialog.tempo_sesh.setText(str(self.tempo_sessao))
        config_dialog.exec()

        self.amplitude_degrau = config_dialog.amplitude_degrau
        self.tempo_sessao = config_dialog.tempo_sessao

        self.start_acq_2.setEnabled(True)
        self.finish_din_b.setEnabled(False)
        self.test_plot.clear()
        self.test_plot.setXRange(0, self.tempo_sessao, padding=0.02)
        self.din_open_serial()

    def din_open_serial(self):
        """Opening ports for serial communication"""
        if not self.serial:
            print("ABRINDO SERIAL ...")
            self.serial = serial.Serial()
            self.serial.dtr = True
            self.serial.baudrate = 115200
            self.serial.port = self.com_port = serial.tools.list_ports.comports()[
                self.com_ports.index(self.device_combo.currentText())
            ].name  # Defining port

            if not self.serial.isOpen():  # Open port if not openned
                self.serial.open()  # Opening port

            time.sleep(2)  # Wait for Arduino and Serial to start up

    def finish_din_test_handle(self):
        self.redo_test_b.setEnabled(False)
        self.config_acq_b_2.setEnabled(False)
        self.tab.setEnabled(True)

        self.dynamic_info()
        if hasattr(self, "din_teste"):
            self.din_teste.stop()
            # aguarda a threadpool processar(não sei se realmente precisa)
            self.din_teste.threadpool.waitForDone(2000)  # timeout em ms
        # if self.dados_plot_din and self.din_x:
        #     print(len(self.din_x))
        #     print("DADOS DE TESTE DINÂMICO PRONTOS PARA TRATAMENTO")
        #     dinamica = self.dinamica_combo.currentText()
        #     print(f"ROTINA: {dinamica}")
        #     diffs = np.diff(self.din_x)
        #
        #     step = np.mean(diffs)
        #     max_error = np.max(np.abs(diffs - step))
        #
        #     print(f"Passo médio: {step}")
        #     print(f"Erro máximo: {max_error}")
        #
        #     if max_error < 1e-9:
        #         print("➡️ O vetor é uniformemente espaçado.")
        #     else:
        #         print("⚠️ O espaçamento NÃO é uniforme.")

        if self.dynamic_report_done and self.static_report_done:
            self.export_report_b.setEnabled(True)

    def generate_report(self):
        export_dialog = ExportConfig()

        if self._nome and self._sensor and self._unidade and self._destino:
            export_dialog.nome_input.setText(str(self._nome))
            export_dialog.sensor_input.setText(str(self._sensor))
            export_dialog.unidade_input.setText(str(self._unidade))
            export_dialog.destino = self._destino

        export_dialog.exec()
        self._nome = export_dialog.nome
        self._sensor = export_dialog.sensor
        self._unidade = export_dialog.unidade
        self._destino = export_dialog.destino


        nome_arquivo = f"relatorio_calibração-{ajustar_str(self._sensor)}.pdf"

        rel = RelatorioCalibracao(pdf_file=os.path.join(self._destino, nome_arquivo),
                                  sensor=self._sensor,
                                  responsavel=self._nome,
                                  sta=self.car_est,
                                  dyn=self.car_din,
                                  unidade=self._unidade)

        rel.build()

    def dynamic_info(self):
        ajustes = {
            0: OrdemZero,
            1: PrimeiraOrdem,
            2: SundaresanSubamortecido,
            3: SundaresanCriticamenteAmortecido,
            4: SundaresanSobreamortecido
        }

        classe_escolhida = ajustes.get(self.dinamica_combo.currentIndex())

        if classe_escolhida is not None:
            self.car_din = classe_escolhida(self.din_x, self.dados_plot_din, self.amplitude_degrau)

        self.car_din.fig_dyn.show()
        self.dynamic_report_done = True

    def open_help_s(self):
        dialog = StaticHelp()
        dialog.exec()

    def open_help_d(self):
        dialog = DynamicHelp()
        dialog.exec()

    def start_din_test(self):
        self.din_plot = self.test_plot.plot()
        self.dados_plot_din = list()

        if self.din_teste:
            self.din_teste = DynamicTest(self.serial, _reset_buffer=False)
        else:
            self.din_teste = DynamicTest(self.serial)
        self.din_teste.data_ready.connect(self.din_plot_handle)
        self.din_teste.session_finished.connect(self.din_session_finish_handle)
        self.dt = 0.01
        self.din_teste.start(self.tempo_sessao, dt=self.dt)
        self.start_acq_2.setEnabled(False)
        self.tab.setEnabled(False)

    def din_plot_handle(self, t, y):
        self.dados_plot_din.append(y)
        self.din_x.append(t)

        self.din_plot.setData(self.din_x, self.dados_plot_din)

    def din_session_finish_handle(self):
        self.redo_test_b.setEnabled(True)
        self.finish_din_b.setEnabled(True)

    def redo_teste_handle(self):
        self.redo_test_b.setEnabled(False)
        self.config_acq_b_2.setEnabled(True)
        self.din_x = list()

    def startup_acquisition_process(self):
        self.acq_index = 0
        self.sequence_points = self.pontos + self.pontos[::-1]
        self.forward_dict = dict()
        self.backward_dict = dict()
        self.fwd_avg = list()
        self.bwd_avg = list()
        self.fwd_x = []
        self.bwd_x = []

        self.fwd_curve = self.points_plot.plot([], [], pen=None, symbol='o', symbolBrush='r', name='Fwd')
        self.bwd_curve = self.points_plot.plot([], [], pen=None, symbol='x', symbolBrush='b', name='Bwd')

        self.status_l.setText(
            f"Ponto atual: {self.sequence_points[self.acq_index]} ({self.acq_index + 1} de {len(self.sequence_points)})")

    def update_com_ports(self):
        self.com_ports = [i.description for i in serial.tools.list_ports.comports()]
        selected = self.device_combo.currentText()

        self.device_combo.clear()
        self.device_combo.addItems(self.com_ports)

        index_arduino = next(
            (i for i, desc in enumerate(self.com_ports)
             if "arduino" in desc.lower()),  # TIRAR COM10 NO FINAL
            -1
        )

        # index_arduino = next(
        #     (i for i, desc in enumerate(self.com_ports)
        #      if "arduino" in desc.lower() or "com10" in desc.lower()),  # TIRAR COM10 NO FINAL
        #     -1
        # )

        if index_arduino != -1:
            self.device_combo.setCurrentIndex(index_arduino)
        else:
            index_current = self.device_combo.findText(selected)
            if index_current != -1:
                self.device_combo.setCurrentIndex(index_current)

    def stat_open_serial(self):
        """Opening ports for serial communication"""

        if not self.serial:
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
        self.config_acq_b.setEnabled(False)
        self.tab_2.setEnabled(False)
        self.startup_acquisition_process()

    def on_acq_button_pressed(self):
        self.acq_b.setEnabled(False)
        # solicita os pontos com intervalo de 0.5s
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
        self.handle_static_acq_process(samples)
        self.redo_point_b.setEnabled(True)
        if not self.acq_index == len(self.sequence_points) - 1:
            self.next_point_b.setEnabled(True)
        else:
            self.finish_stat_b.setEnabled(True)

        self.plot_static_points()

    def plot_static_points(self):
        if self.acq_index < len(self.sequence_points) // 2:
            self.fwd_curve.setData(self.fwd_x, self.fwd_avg)
        else:
            self.bwd_curve.setData(self.bwd_x, self.bwd_avg)

    def redo_point_handle(self):
        if self.acq_index < len(self.sequence_points) // 2:
            # indo
            del self.forward_dict[self.sequence_points[self.acq_index]]
            self.fwd_avg.pop()
            self.fwd_x.pop()

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
        self.acq_b.setEnabled(True)
        self.redo_point_b.setEnabled(False)
        self.next_point_b.setEnabled(False)

        self.acq_index += 1
        self.status_l.setText(
            f"Ponto atual: {self.sequence_points[self.acq_index]} ({self.acq_index + 1} de {len(self.sequence_points)})")

    def finish_stat_handle(self):
        self.static_info()
        if hasattr(self, "get_signal"):
            self.get_signal.stop()
            # aguarda a threadpool processar(não sei se realmente precisa)
            self.get_signal.threadpool.waitForDone(2000)  # timeout em ms

        self.config_acq_b.setEnabled(False)
        self.redo_point_b.setEnabled(False)
        self.tab_2.setEnabled(True)
        self.signal_plot.clear()

        if self.dynamic_report_done and self.static_report_done:
            self.export_report_b.setEnabled(True)

    def static_info(self):

        self.car_est = CaracteristicasEstaticas(self.pontos, self.forward_dict, self.backward_dict,
                                                self.ajuste_combo.currentIndex() + 1)
        self.car_est.fig_ccs.show()
        self.car_est.fig_csens.show()
        self.car_est.fig_hist.show()

        self.static_report_done = True

    def exit_handle(self):
        # para a thread do GetSignal e espera terminar
        if self.din_teste._running:
            self.din_teste.stop()

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
