from PySide6 import QtWidgets

from uis.ui_configs_saida import Ui_ConfigsSaida


class ExportConfig(QtWidgets.QDialog, Ui_ConfigsSaida):
    def __init__(self):
        super(ExportConfig, self).__init__()
        pass
