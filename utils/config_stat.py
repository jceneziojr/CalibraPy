from PySide6 import QtWidgets

from uis.ui_configs import Ui_Configs


class StatConfigDialog(QtWidgets.QDialog, Ui_Configs):
    def __init__(self):
        super(StatConfigDialog, self).__init__()
        self.setupUi(self)
        self.finish_b.released.connect(self.finalizar)
        self.pontos = None
        self.pontos_acq = None

        self.point_input.editingFinished.connect(self.get_ponto)
        self.remove_point_b.released.connect(self.remove_ponto)

    def get_ponto(self):
        self.points_list.addItem(self.point_input.text())
        self.point_input.clear()

    def remove_ponto(self):
        listItems = self.points_list.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.points_list.takeItem(self.points_list.row(item))

    def finalizar(self):
        texto = self.acq_points.text().strip()
        self.pontos = [self.points_list.item(x).text() for x in range(self.points_list.count())]
        if not texto or not self.pontos or len(self.pontos) < 2:
            pass
        else:
            self.pontos_acq = int(texto)
            self.close()
