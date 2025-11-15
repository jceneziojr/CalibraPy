import numpy as np
import matplotlib.pyplot as plt


class PrimeiraOrdem:
    """
    Classe para identificação de sistemas de 1ª ordem (sem atraso),
    a partir da resposta ao degrau.

    Modelo identificado:
        G(s) = K / (τs + 1)
    """

    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = t
        self.y = y
        self.amplitude_degrau = amplitude_degrau
        self.dt = dt if dt else t[1] - t[0]

        # parâmetros identificados
        self.K = None
        self.tau = None
        self.y_zerom = None
        self.y_inf = None
        self.modelo = None

    # ------------------------------------------------------------------------------------
    def ajustar(self):
        """Identifica o ganho K e a constante de tempo τ."""

        tam_amostra = len(self.y)

        # valores inicial e final
        self.y_inf = np.mean(self.y[-int(tam_amostra * 0.05):])
        self.y_zerom = self.y[0]

        # ganho estático
        self.K = (self.y_inf - self.y_zerom) / self.amplitude_degrau

        # valor correspondente a 63,2% do ganho total
        y_tau = 0.632 * (self.y_inf - self.y_zerom) + self.y_zerom

        # índice mais próximo do ponto onde y ≈ y_tau
        index_tau = np.abs(self.y - y_tau).argmin()

        # constante de tempo (em segundos)
        self.tau = index_tau * self.dt

        # gera o modelo ajustado
        self.modelo = self.y_zerom + self.K * (1 - np.exp(-self.t / self.tau))

        print("=== Resultados do Ajuste (1ª Ordem) ===")
        print(f"Ganho (K): {self.K:.4f}")
        print(f"Constante de tempo (τ): {self.tau:.4f} s")
        print("Função de Transferência aproximada:")
        print(f"G(s) = {self.K:.3f} / ({self.tau:.3f}s + 1)")
        print("======================================")

    # ------------------------------------------------------------------------------------
    def plot_comparacao(self):
        """Plota comparação entre dados e modelo ajustado."""
        if self.modelo is None:
            raise RuntimeError("Modelo ainda não ajustado. Execute ajustar() primeiro.")

        plt.figure(figsize=(8, 4))
        plt.plot(self.t, self.y, 'r', label='Dados medidos')
        plt.plot(self.t, self.modelo, 'b', label='Modelo ajustado')
        plt.xlabel("Tempo [s]")
        plt.ylabel("Amplitude")
        plt.title("Comparação entre dados e modelo (1ª Ordem)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


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
modelo_1ordem.ajustar()
modelo_1ordem.plot_comparacao()
