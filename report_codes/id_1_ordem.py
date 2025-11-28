import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Courier New'


class PrimeiraOrdem:
    """
    Identificação de sistemas de 1ª ordem a partir da resposta ao degrau.
    Modelo identificado:
        G(s) = K / (τs + 1)
    """

    # identificador
    TIPO_AJUSTE = "1a_ordem"

    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = np.array(t)
        self.y = np.array(y)
        self.amplitude_degrau = amplitude_degrau
        self.dt = dt if dt else self.t[1] - self.t[0]

        # parâmetros identificados
        self.K = None
        self.tau = None
        self.y_zerom = None
        self.y_inf = None
        self.modelo = None
        self.erro_mse = None

        # processamento automático
        self._ajustar_modelo()
        self._avaliar_erro()
        self._gerar_plot()

    # ============================================================
    def _ajustar_modelo(self):
        """Identifica o ganho K e a constante de tempo τ."""
        tam = len(self.y)

        # condição inicial
        self.y_zerom = float(self.y[0])

        # remove condição inicial
        y_adj = self.y - self.y_zerom

        # valor final (normalizado)
        self.y_inf = float(np.mean(y_adj[-int(tam * 0.05):]))

        # ganho DC
        self.K = float(self.y_inf / self.amplitude_degrau)

        # nível correspondente a 63,2% da variação
        y_tau = 0.632 * self.y_inf

        # índice mais próximo em y_adj
        idx_tau = int(np.abs(y_adj - y_tau).argmin())

        # constante de tempo τ
        self.tau = float(idx_tau * self.dt)

        # modelo ajustado partindo de zero
        modelo_zero = self.K * (1 - np.exp(-self.t / self.tau))

        # modelo final com condição inicial recolocada
        self.modelo = self.y_zerom + modelo_zero

    # ============================================================
    def _avaliar_erro(self):
        """Erro MSE entre modelo e valores medidos."""
        self.erro_mse = float(np.mean((self.y - self.modelo) ** 2))

    # ============================================================
    def _gerar_plot(self):
        """Gera figura para relatório (comparação dado vs modelo)."""
        self.fig_dyn, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.t, self.y, 'r', label="Dados")
        ax.plot(self.t, self.modelo, 'b', label="Modelo aproximado")
        ax.set_xlabel("Tempo [s]", fontsize=14)
        ax.set_ylabel("Amplitude da saída do sensor", fontsize=14)
        ax.set_title("Comparação entre dados e modelo dinâmico", fontsize=14)
        ax.set_ylim(-1, 6)
        ax.grid(True)
        ax.legend()
        self.fig_dyn.tight_layout()


# --- gera dados simulados ---
K_real = 2.0
tau_real = 4
t_final = 30
dt = 0.01
t = np.arange(0, t_final, dt)
y_clean = K_real * (1 - np.exp(-t / tau_real))

np.random.seed(42)
noise = np.random.normal(0, 0.005 * K_real, size=t.shape)
y_noisy = y_clean + noise

# --- aplica identificação ---
modelo_1ordem = PrimeiraOrdem(t, y_noisy, amplitude_degrau=1, dt=dt)
