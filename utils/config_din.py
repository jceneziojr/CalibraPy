from PySide6 import QtWidgets

from uis.ui_configs_din import Ui_Configs


class DinConfigDialog(QtWidgets.QDialog, Ui_Configs):

    def __init__(self):
        super(DinConfigDialog, self).__init__()
        self.setupUi(self)
        self.finish_b.released.connect(self.finalizar)
        self.amplitude_degrau = None
        self.tempo_sessao = None

    def finalizar(self):
        amp_txt = self.amp_deg.text().strip()
        tempo_txt = self.tempo_sesh.text().strip()

        if not amp_txt or not tempo_txt:
            return

        try:
            self.amplitude_degrau = float(amp_txt)
            self.tempo_sessao = float(tempo_txt)
        except ValueError:
            return

        self.close()
