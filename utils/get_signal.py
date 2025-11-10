import time
from collections import deque
import shiboken6
from PySide6.QtCore import QObject, Signal, QThreadPool
from .thread_related import Worker


class GetSignal(QObject):
    data_ready = Signal(object)  # para atualizar o plot (buffer contínuo)
    samples_ready = Signal(list)  # para quando uma aquisição pontual terminar

    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self.buffer = deque(maxlen=100)
        self.threadpool = QThreadPool()
        self._running = True

        # fila de pedidos de aquisição pontual: cada item = dict {'n': int, 'interval': float}
        self.request_queue = deque()
        self._current_request = None  # estrutura: {'n', 'interval', 'collected', 'next_t', 'results'}

        # iniciar a thread de aquisição contínua
        self.thread(self.acquisition)

    def stop(self):
        """Para a aquisição contínua e solicita o fim da thread."""
        self._running = False

    def request_samples(self, n_points, interval=0.5):
        """
        Solicita uma aquisição pontual usando a MESMA thread.
        A thread irá coletar n_points amortizados por 'interval' segundos
        e emitir samples_ready(list_of_values) ao terminar.
        """
        if n_points <= 0:
            return
        self.request_queue.append({'n': int(n_points), 'interval': float(interval)})

    def acquisition(self):
        """
        Loop principal: mantém o buffer para plot e processa pedidos pontuais.
        """
        # tenta limpar o buffer/porta antes
        try:
            self.serial.reset_input_buffer()
        except Exception:
            pass

        while self._running:
            if not shiboken6.isValid(self):
                print("objeto deletado")
                break

            st = time.time()

            # leitura normal (para o plot)
            try:
                raw = self.serial.read(14)
                parts = raw.split()
                if len(parts) >= 2:
                    try:
                        temp = int(parts[-2].decode("UTF-8")) * 0.00488
                        print(temp)
                        self.buffer.append(temp)
                        # emite para atualizar plot
                        self.data_ready.emit(list(self.buffer))
                    except Exception:
                        # se parsing falhar, ignora
                        pass
            except Exception as e:
                # erro de leitura (porta fechada, timeout, etc.)
                print("Erro na leitura serial (loop contínuo):", e)
                # opcional: break  -> aqui apenas espera e continua
                # break

            # --- processa request atual ou pega nova ---
            now = time.monotonic()
            if self._current_request is None and self.request_queue:
                # inicia próximo pedido
                rq = self.request_queue.popleft()
                self._current_request = {
                    'n': rq['n'],
                    'interval': rq['interval'],
                    'collected': 0,
                    'next_t': now,  # coletar imediatamente
                    'results': []
                }

            if self._current_request is not None:
                cr = self._current_request
                if now >= cr['next_t']:
                    # faz a leitura (mesma forma de parsing)
                    try:
                        raw = self.serial.read(14)
                        parts = raw.split()
                        if len(parts) >= 2:
                            try:
                                temp = int(parts[-2].decode("UTF-8")) * 0.00488
                                cr['results'].append(temp)
                                cr['collected'] += 1
                            except Exception:
                                # falha de parse: ainda conta a tentativa? aqui NÂO conta e não avança next_t
                                pass
                        else:
                            # caso não haja dados suficientes, opcional: append None ou ignorar
                            pass
                    except Exception as e:
                        print("Erro na leitura serial (acq pontual):", e)

                    # agenda próxima amostra
                    cr['next_t'] = now + cr['interval']

                    # se completou, emite e limpa current_request
                    if cr['collected'] >= cr['n']:
                        try:
                            self.samples_ready.emit(list(cr['results']))
                        except Exception as e:
                            print("Erro emitindo samples_ready:", e)
                        self._current_request = None

            # controle de taxa do loop principal: mantém responsividade
            et = time.time()
            # o delay aqui evita loop 100% CPU; ajustável
            delay = 0.001 + (st - et)
            if delay > 0:
                time.sleep(delay)

        # fim while
        print("GetSignal: thread encerrada.")

    def thread(self, func_to_pass, *args, **kwargs):
        worker = Worker(func_to_pass, *args, **kwargs)
        self.threadpool.start(worker)
