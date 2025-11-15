import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Courier New'


class OrdemZero:
    """Modelo dinâmico de 0ª ordem para resposta a degrau."""

    # identificador
    TIPO_AJUSTE = "0a_ordem"

    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = np.array(t)
        self.y = np.array(y)
        self.amplitude_degrau = amplitude_degrau
        self.dt = dt if dt else self.t[1] - self.t[0]

        # parâmetros identificados
        self.K = None
        self.y_inf = None
        self.modelo = None
        self.erro_mse = None

        self._ajustar_modelo()
        self._avaliar_erro()
        self._gerar_plot()

    # ============================================================
    def _ajustar_modelo(self):
        """Ajuste simples de modelo 0ª ordem."""
        tam = len(self.y)

        # valor final da resposta -- média dos últimos 5%
        self.y_inf = float(np.mean(self.y[-int(tam * 0.05):]))

        # ganho K
        self.K = float(self.y_inf / self.amplitude_degrau)

        # modelo 0ª ordem = constante no valor final
        self.modelo = np.ones_like(self.t) * (self.K * self.amplitude_degrau)

    # ============================================================
    def _avaliar_erro(self):
        """Cálculo do erro MSE entre modelo e dados reais."""
        self.erro_mse = float(np.mean((self.y - self.modelo) ** 2))

    # ============================================================
    def _gerar_plot(self):
        """Gera figura padrão para relatório (comparação dado vs modelo)."""
        self.fig_dyn, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.t, self.y, 'r', label="Dados")
        ax.plot(self.t, self.modelo, 'b', label="Modelo aproximado")
        ax.set_xlabel("Tempo [s]", fontsize=14)
        ax.set_ylabel("Amplitude", fontsize=14)
        ax.set_title("Comparação entre dados e modelo dinâmico", fontsize=14)
        ax.grid(True)
        ax.legend()
        self.fig_dyn.tight_layout()


K_real = 3.0
t_final = 5
dt = 0.01
t = np.arange(0, t_final, dt)
u = np.ones_like(t)
y_clean = K_real * u

np.random.seed(42)
noise = np.random.normal(0, 0.02 * K_real, size=t.shape)
y_noisy = y_clean + noise

modelo_0ordem = OrdemZero(t, y_noisy, amplitude_degrau=1, dt=dt)
