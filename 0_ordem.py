import numpy as np
import matplotlib.pyplot as plt


class OrdemZero:
    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = t
        self.y = y
        self.amplitude_degrau = amplitude_degrau
        self.dt = dt if dt else t[1] - t[0]

        # parâmetros identificados
        self.K = None
        self.y_zerom = None
        self.y_inf = None
        self.modelo = None

    # ------------------------------------------------------------------------------------
    def ajustar(self):
        tam_amostra = len(self.y)

        self.y_inf = np.mean(self.y[-int(tam_amostra * 0.05):])
        # self.y_zerom = np.mean(self.y[int(tam_amostra * 0.01):])

        self.K = self.y_inf / self.amplitude_degrau

        self.modelo = np.ones_like(self.t) * (self.K * self.amplitude_degrau)

        print("=== Resultados do Ajuste (0ª Ordem) ===")
        print(f"Ganho (K): {self.K:.4f}")
        print("Função de Transferência aproximada:")
        print(f"G(s) = {self.K:.3f}")
        print("=======================================")

    # ------------------------------------------------------------------------------------
    def plot_comparacao(self):
        if self.modelo is None:
            raise RuntimeError("Modelo ainda não ajustado. Execute ajustar() primeiro.")

        plt.figure(figsize=(8, 4))
        plt.plot(self.t, self.y, 'r', label='Dados medidos')
        plt.plot(self.t, self.modelo, 'b', label='Modelo ajustado')
        plt.xlabel("Tempo [s]")
        plt.ylabel("Amplitude")
        plt.title("Comparação entre dados e modelo (0ª Ordem)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


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
modelo_0ordem.ajustar()
modelo_0ordem.plot_comparacao()
