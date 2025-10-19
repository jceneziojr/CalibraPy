import os
import time
import shiboken6
from collections import deque
from .thread_related import Worker
from PySide6.QtCore import QThreadPool, QThread, QObject, QMutex, Signal, QWaitCondition


class GetSignal(QObject):
    data_ready = Signal(object)  # signal para enviar os dados para a GUI

    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self.buffer = deque(maxlen=100)
        self.threadpool = QThreadPool()
        self.thread(self.acquisition)

    def acquisition(self):
        self.serial.reset_input_buffer()
        while True:
            if not shiboken6.isValid(self):
                print("objeto deletado")
                break

            st = time.time()
            temp = int(self.serial.read(14).split()[-2].decode("UTF-8")) * 0.00488  # ex: ard_vpb
            self.buffer.append(temp)
            print(temp)
            # envia os dados para a GUI
            self.data_ready.emit(list(self.buffer))

            et = time.time()
            if 0.001 + (st - et) > 0:
                time.sleep(0.001 + (st - et))

    def thread(self, func_to_pass, *args, **kwargs):
        worker = Worker(func_to_pass, *args, **kwargs)
        self.threadpool.start(worker)
