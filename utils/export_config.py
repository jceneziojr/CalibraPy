from PySide6 import QtWidgets

from uis.ui_configs_saida import Ui_ConfigsSaida


class ExportConfig(QtWidgets.QDialog, Ui_ConfigsSaida):
    def __init__(self):
        super(ExportConfig, self).__init__()
        self.finish_b.released.connect(self.finalizar)
        self.nome = None
        self.sensor = None
        self.unidade = None
        self.destino = None

    def finalizar(self):
        if not self.nome_input.text().strip() or self.sensor_input.text().strip() or self.unidade_input.text().strip():
            return
        else:
            self.destino = QtWidgets.QFileDialog.getExistingDirectory(
                self, caption="Local para salvar o relatório de calibração"
            )
            self.nome = self.nome_input.text()
            self.sensor = self.sensor_input.text()
            self.unidade = self.unidade_input.text()

        self.close()
