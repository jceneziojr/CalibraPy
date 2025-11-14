from PySide6 import QtWidgets

from uis.ui_help_din import Ui_DynamicHelp
from uis.ui_help_sta import Ui_StaticHelp


class StaticHelp(QtWidgets.QDialog, Ui_StaticHelp):

    def __init__(self):
        super(StaticHelp, self).__init__()
        self.setupUi(self)


class DynamicHelp(QtWidgets.QDialog, Ui_DynamicHelp):

    def __init__(self):
        super(DynamicHelp, self).__init__()
        self.setupUi(self)
