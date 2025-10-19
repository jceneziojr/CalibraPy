from PySide6.QtCore import QObject, QRunnable, Slot, Signal


class WorkerSignals(QObject):
    finished = Signal()
    started = Signal()
    progress = Signal(str)
    returned = Signal(object)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        self.signals.started.emit()
        saida = self.fn(*self.args, **self.kwargs)
        self.signals.returned.emit(saida)
        self.signals.finished.emit()
