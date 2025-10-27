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
        texto = self.point_input.text().strip().replace(',', '.')

        if not texto:
            return  # sai se estiver vazio

        try:
            valor = float(texto)  # só procede se for numero
        except ValueError:
            return

        self.points_list.addItem(str(valor))  # QListWidget só aceita texto
        self.point_input.clear()

    def remove_ponto(self):
        listItems = self.points_list.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.points_list.takeItem(self.points_list.row(item))

    def finalizar(self):
        texto = self.acq_points.text().strip()

        if not texto:  # checa se o número de aquisição por pts está
            return

        try:
            valor = int(texto)  # checando se é um int
        except ValueError:
            return

        # verifica se está entre 1 e 10
        if valor < 1 or valor > 10:
            return

        # lista de pontos
        self.pontos = [float(self.points_list.item(x).text()) for x in range(self.points_list.count())]

        # checa se há pelo menos dois pontos válidos
        if not self.pontos or len(self.pontos) < 2:
            return

        self.pontos_acq = valor
        self.close()
