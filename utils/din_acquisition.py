import time
from PySide6.QtCore import QObject, Signal, QThreadPool
from .thread_related import Worker
import shiboken6


class DynamicTest(QObject):
    data_ready = Signal(float)  # emite cada ponto para plot contínuo
    session_finished = Signal(list)  # emite toda a curva no final

    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self.threadpool = QThreadPool()
        self._running = False
        self.total_time = 0
        self.dt = 0.01
        self.collected_data = []

    def start(self, total_time, dt=0.01):
        self.total_time = float(total_time)
        self.dt = float(dt)
        self.collected_data = []
        self._running = True
        self.thread(self.acquisition)

    def stop(self):
        self._running = False

    def acquisition(self):
        # loop princiapl
        # tenta limpar buffer/porta antes
        try:
            self.serial.reset_input_buffer()
        except Exception:
            pass

        start_time = time.monotonic()
        while self._running:
            if not shiboken6.isValid(self):
                print("Objeto deletado")
                break

            now = time.monotonic()
            elapsed = now - start_time
            if elapsed >= self.total_time:
                break

            loop_start = time.monotonic()

            # leitura do sensor
            try:
                raw = self.serial.read(14)
                parts = raw.split()
                if len(parts) >= 2:
                    try:
                        value = int(parts[-2].decode("UTF-8")) * 0.00488
                        self.collected_data.append(value)
                        self.data_ready.emit(value)  # envia para plot contínuo
                    except Exception:
                        pass
            except Exception as e:
                print("Erro na leitura serial:", e)

            # controle preciso do intervalo
            loop_elapsed = time.monotonic() - loop_start
            delay = max(0, self.dt - loop_elapsed)
            if delay > 0:
                time.sleep(delay)

        # fim do ensaio
        self._running = False
        self.session_finished.emit(list(self.collected_data))
        print("DynamicTest: aquisição encerrada.")

    def thread(self, func_to_pass, *args, **kwargs):
        """Inicia função em thread separada usando Worker."""
        worker = Worker(func_to_pass, *args, **kwargs)
        self.threadpool.start(worker)
