import time
from PySide6.QtCore import QObject, Signal, QThreadPool
from .thread_related import Worker
import shiboken6


class DynamicTest(QObject):
    # Agora emite (tempo, valor)
    data_ready = Signal(float, float)  
    session_finished = Signal(list)  # emite toda a curva no final

    def __init__(self, serial, _reset_buffer=True):
        super().__init__()
        self.serial = serial
        self.threadpool = QThreadPool()
        self._running = False
        self.total_time = 0
        self.dt = 0.01
        self.collected_data = []  # apenas y
        self.collected_time = []  # guarda também o tempo

        self._reset_buffer = _reset_buffer

    def start(self, total_time, dt=0.01):
        self.total_time = float(total_time)
        self.dt = float(dt)
        self.collected_data = []
        self.collected_time = []
        self._running = True
        self.thread(self.acquisition)

    def stop(self):
        self._running = False

    def acquisition(self):
        if self._reset_buffer:
            try:
                self.serial.reset_input_buffer()
            except Exception:
                pass
        
        start_time = time.monotonic()
        while self._running:
            if not shiboken6.isValid(self):
                print("objeto do plot deletado")
                break

            now = time.monotonic()
            elapsed = now - start_time
            if elapsed >= self.total_time:
                break

            loop_start = time.monotonic()

            try:
                raw = self.serial.read(14)
                parts = raw.split()
                if len(parts) >= 2:
                    try:
                        value = int(parts[-2].decode("UTF-8")) * 0.00488
                        self.collected_data.append(value)
                        self.collected_time.append(elapsed)
                        # envia tempo e valor
                        self.data_ready.emit(elapsed, value)
                    except Exception:
                        pass
            except Exception as e:
                print("erro na leitura serial:", e)

            loop_elapsed = time.monotonic() - loop_start
            delay = max(0, self.dt - loop_elapsed)
            if delay > 0:
                time.sleep(delay)

        self.session_finished.emit(list(self.collected_data))

    def thread(self, func_to_pass, *args, **kwargs):
        worker = Worker(func_to_pass, *args, **kwargs)
        self.threadpool.start(worker)
