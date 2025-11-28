import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from scipy.signal import lti, step
from sklearn.metrics import mean_squared_error
import pynumdiff


class SundaresanSubamortecido:
    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = t
        self.y = y
        self.amplitude_degrau = amplitude_degrau
        self.dt = dt if dt is not None else t[1] - t[0]

        # Resultados finais
        self.K = None
        self.xi = None
        self.wn = None
        self.tau_d = None
        self.modelo = None
        self.indice_inflexao = None

    # ----------------------------------------------------------------------------------------
    # Função auxiliar: resolver ξ a partir de λ
    @staticmethod
    def xi_from_lambda(lmbd_target):
        def f(xi):
            chi = np.arccos(xi) / np.sqrt(1 - xi ** 2)
            return chi * np.exp(-xi * chi) - lmbd_target

        xi_vals = np.linspace(-0.9999, 0.9999, 2000)
        f_vals = [f(x) for x in xi_vals]
        sign_changes = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
        if len(sign_changes) == 0:
            raise ValueError("Nenhuma troca de sinal encontrada — λ fora do domínio possível.")

        a, b = xi_vals[sign_changes[0]], xi_vals[sign_changes[0] + 1]
        sol = root_scalar(f, bracket=(a, b), method='brentq')
        return sol.root

    # ----------------------------------------------------------------------------------------
    def _calcular_ganho_normalizar(self):
        tam_amostra = len(self.y)
        y_inf = np.mean(self.y[-int(tam_amostra * 0.05):])
        y_zerom = self.y[0]
        self.K = (y_inf - y_zerom) / self.amplitude_degrau

        y_adj = self.y - y_zerom
        valor_y_ss = np.mean(y_adj[int(tam_amostra * 0.9):])
        y_normalizado = y_adj / valor_y_ss
        return y_normalizado, y_zerom

    # ----------------------------------------------------------------------------------------
    def _calcular_area_m1(self, y_normalizado, dt):
        diff = y_normalizado - 1
        area_acima = np.sum(diff[diff > 0]) * dt
        area_abaixo = np.sum(-diff[diff < 0]) * dt
        m1 = area_abaixo - area_acima
        return m1

    # ----------------------------------------------------------------------------------------
    def _calcular_y_modelo(self, indice, t, x_hat, dxdt_hat, d2xdt_hat, m1, dt):
        x0, y0 = t[indice], x_hat[indice]
        Mi = dxdt_hat[indice]

        tm = x0 + (1 - y0) / Mi
        valor_lambda = (tm - m1) * Mi

        try:
            xi_valor = self.xi_from_lambda(valor_lambda)
        except ValueError:
            return np.inf, None, None, None, None

        wn_n = (np.arccos(xi_valor) / np.sqrt(1 - xi_valor ** 2)) * (1 / (tm - m1))
        tau_d = m1 - (2 * xi_valor) / wn_n

        num = [wn_n ** 2]
        den = [1, 2 * xi_valor * wn_n, wn_n ** 2]
        sistema = lti(num, den)
        _, _y = step(sistema, T=t)

        y_novo = np.zeros_like(_y)
        mask = t >= tau_d
        y_novo[mask] = np.interp(t[mask] - tau_d, t, _y)

        mse = mean_squared_error(x_hat, y_novo)
        return mse, y_novo, xi_valor, wn_n, tau_d

    # ----------------------------------------------------------------------------------------
    def ajustar(self, window_size=10, num_iter=3, max_passos=25, delta_idx=5, tolerancia=1e-4):

        y_normalizado, y_zerom = self._calcular_ganho_normalizar()  # normalizando e pegando o nivel DC

        m1 = self._calcular_area_m1(y_normalizado, self.dt)

        x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            y_normalizado, self.dt, kernel='mean', window_size=window_size, num_iterations=num_iter
        )
        _, d2xdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            dxdt_hat, self.dt, kernel='mean', window_size=window_size, num_iterations=num_iter
        )

        indice_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][0]

        melhor_mse, melhor_y, melhor_xi, melhor_wn, melhor_tau_d = self._calcular_y_modelo(
            indice_inflexao, self.t, x_hat, dxdt_hat, d2xdt_hat, m1, self.dt
        )
        melhor_indice = indice_inflexao

        for offset in range(delta_idx, max_passos * delta_idx + 1, delta_idx):
            # Frente
            idx_forward = indice_inflexao + offset
            if idx_forward < len(self.t):
                mse_fwd, y_fwd, xi_fwd, wn_fwd, tau_d_fwd = self._calcular_y_modelo(
                    idx_forward, self.t, x_hat, dxdt_hat, d2xdt_hat, m1, self.dt
                )
                if mse_fwd < melhor_mse:
                    melhor_mse, melhor_y, melhor_xi, melhor_wn, melhor_tau_d = mse_fwd, y_fwd, xi_fwd, wn_fwd, tau_d_fwd
                    melhor_indice = idx_forward

            # Trás
            idx_backward = indice_inflexao - offset
            if idx_backward >= 0:
                mse_bwd, y_bwd, xi_bwd, wn_bwd, tau_d_bwd = self._calcular_y_modelo(
                    idx_backward, self.t, x_hat, dxdt_hat, d2xdt_hat, m1, self.dt
                )
                if mse_bwd < melhor_mse:
                    melhor_mse, melhor_y, melhor_xi, melhor_wn, melhor_tau_d = mse_bwd, y_bwd, xi_bwd, wn_bwd, tau_d_bwd
                    melhor_indice = idx_backward

            if melhor_mse < tolerancia:
                break

        # Guarda resultados
        self.modelo = melhor_y * self.K + y_zerom
        self.xi = melhor_xi
        self.wn = melhor_wn
        self.tau_d = melhor_tau_d
        self.indice_inflexao = melhor_indice

        print("=== Resultados do Ajuste (Método Subamortecido) ===")
        print(f"Ganho (K): {self.K:.4f}")
        print(f"Fator de amortecimento (ξ): {self.xi:.4f}")
        print(f"Frequência natural (ωn): {self.wn:.4f} rad/s")
        print(f"Atraso de tempo (τd): {self.tau_d:.4f} s")
        print("Função de Transferência aproximada:")
        print(
            f"G(s) = {self.K:.3f} * exp(-{self.tau_d:.3f}s) / (s² + {2 * self.xi * self.wn:.3f}s + {self.wn ** 2:.3f})")
        print("====================================================")

    # ----------------------------------------------------------------------------------------
    def plot_comparacao(self):
        if self.modelo is None:
            raise RuntimeError("Modelo ainda não ajustado. Execute ajustar() primeiro.")
        plt.figure(figsize=(8, 4))
        plt.plot(self.t, self.y, 'r', label='Dados medidos')
        plt.plot(self.t, self.modelo, 'b', label='Modelo ajustado (x K)')
        plt.xlabel("Tempo [s]")
        plt.ylabel("Amplitude da saída do sensor")
        plt.title("Comparação entre dados e modelo (Método Subamortecido)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ===========================================================
# Teste com dados simulados
# ===========================================================
K_real = 2.0
wn_real = 2.0
xi_real = 0.75  # subamortecido
t_final = 30
dt = 0.01
t = np.arange(0, t_final, dt)

num = [K_real * wn_real ** 2]
den = [1, 2 * xi_real * wn_real, wn_real ** 2]
sistema = lti(num, den)
_, y_clean = step(sistema, T=t)

np.random.seed(42)
noise = np.random.normal(0, 0.005 * K_real, size=t.shape)
y_noisy = y_clean + noise
y_noisy = y_clean + noise + 3 * np.ones_like(y_clean)

# Aplicação da classe
modelo_sub = SundaresanSubamortecido(t, y_noisy, amplitude_degrau=1, dt=dt)
modelo_sub.ajustar()
modelo_sub.plot_comparacao()
