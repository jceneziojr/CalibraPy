import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step
from scipy.optimize import root_scalar
from sklearn.metrics import mean_squared_error
import pynumdiff

plt.rcParams['font.family'] = 'Courier New'


class SundaresanSubamortecido:
    """Identificação de modelo de 2ª ordem subamortecido (método de Sundaresan)."""

    # identificador
    TIPO_AJUSTE = "2a_ordem_subamortecido"

    def __init__(self, t, y, amplitude_degrau=1.0, dt=None,
                 window_size=10, num_iter=3, max_passos=25,
                 delta_idx=5, tolerancia=1e-4):

        self.t = np.array(t)
        self.y = np.array(y)
        self.amplitude_degrau = amplitude_degrau
        # self.dt = dt if dt else self.t[1] - self.t[0]

        # reconstruindo o vetor de tempo, pra ser espaçado igualmente
        dts = np.diff(self.t)
        dt_medio = np.mean(dts)
        self.dt = np.round(dt_medio, 3)

        t0 = self.t[0]
        N = len(self.t)

        self.t = t0 + np.arange(N) * self.dt

        # Resultados
        self.K = None
        self.xi = None
        self.wn = None
        self.tau_d = None
        self.indice_inflexao = None
        self.modelo = None
        self.erro_mse = None

        # Processamento automático
        self._ajustar_modelo(window_size, num_iter, max_passos, delta_idx, tolerancia)
        self._avaliar_erro()
        self._gerar_plot()

    # ----------------------------------------------------------------------------------------
    @staticmethod
    def xi_from_lambda(lmbd_target):
        """Resolve xi pelo método de Brent a partir de lambda."""

        def f(xi):
            chi = np.arccos(xi) / np.sqrt(1 - xi ** 2)
            return chi * np.exp(-xi * chi) - lmbd_target

        xi_vals = np.linspace(-0.9999, 0.9999, 2000)
        f_vals = [f(x) for x in xi_vals]
        sign_changes = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
        if len(sign_changes) == 0:
            raise ValueError("Nenhuma troca de sinal — λ fora do domínio.")

        a, b = xi_vals[sign_changes[0]], xi_vals[sign_changes[0] + 1]
        sol = root_scalar(f, bracket=(a, b), method='brentq')
        return sol.root

    # ----------------------------------------------------------------------------------------
    def _calcular_ganho_normalizar(self):
        tam = len(self.y)
        y_inf = np.mean(self.y[-int(tam * 0.05):])
        y_zerom = self.y[0]

        self.K = (y_inf - y_zerom) / self.amplitude_degrau

        y_adj = self.y - y_zerom
        valor_y_ss = np.mean(y_adj[int(tam * 0.9):])
        y_normalizado = y_adj / valor_y_ss
        return y_normalizado, y_zerom

    # ----------------------------------------------------------------------------------------
    def _calcular_area_m1(self, y_normalizado):
        diff = y_normalizado - 1
        area_acima = np.sum(diff[diff > 0]) * self.dt
        area_abaixo = np.sum(-diff[diff < 0]) * self.dt
        return area_abaixo - area_acima

    # ----------------------------------------------------------------------------------------
    def _calcular_y_modelo(self, indice, t, x_hat, dxdt_hat, d2xdt_hat, m1):
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

        sistema = lti([wn_n ** 2], [1, 2 * xi_valor * wn_n, wn_n ** 2])
        _, y_step = step(sistema, T=t)

        y_mod = np.zeros_like(y_step)
        mask = t >= tau_d
        y_mod[mask] = np.interp(t[mask] - tau_d, t, y_step)

        mse = mean_squared_error(x_hat, y_mod)
        return mse, y_mod, xi_valor, wn_n, tau_d

    # ----------------------------------------------------------------------------------------
    def _ajustar_modelo(self, window_size, num_iter, max_passos, delta_idx, tolerancia):

        y_norm, y_zerom = self._calcular_ganho_normalizar()
        m1 = self._calcular_area_m1(y_norm)

        x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            y_norm, self.dt, kernel='mean',
            window_size=window_size, num_iterations=num_iter
        )
        _, d2xdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            dxdt_hat, self.dt, kernel='mean',
            window_size=window_size, num_iterations=num_iter
        )

        indice_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][0]

        melhor_mse, melhor_y, melhor_xi, melhor_wn, melhor_tau_d = \
            self._calcular_y_modelo(indice_inflexao, self.t, x_hat,
                                    dxdt_hat, d2xdt_hat, m1)

        melhor_indice = indice_inflexao

        for offset in range(delta_idx, max_passos * delta_idx + 1, delta_idx):

            # Frente
            idx_f = indice_inflexao + offset
            if idx_f < len(self.t):
                mse, y_mod, xi0, wn0, td0 = \
                    self._calcular_y_modelo(idx_f, self.t, x_hat,
                                            dxdt_hat, d2xdt_hat, m1)
                if mse < melhor_mse:
                    melhor_mse, melhor_y = mse, y_mod
                    melhor_xi, melhor_wn, melhor_tau_d = xi0, wn0, td0
                    melhor_indice = idx_f

            # Trás
            idx_b = indice_inflexao - offset
            if idx_b >= 0:
                mse, y_mod, xi0, wn0, td0 = \
                    self._calcular_y_modelo(idx_b, self.t, x_hat,
                                            dxdt_hat, d2xdt_hat, m1)
                if mse < melhor_mse:
                    melhor_mse, melhor_y = mse, y_mod
                    melhor_xi, melhor_wn, melhor_tau_d = xi0, wn0, td0
                    melhor_indice = idx_b

            if melhor_mse < tolerancia:
                break

        # Resultados finais escalonados
        self.modelo = melhor_y * self.K + y_zerom
        self.xi = melhor_xi
        self.wn = melhor_wn
        self.tau_d = melhor_tau_d
        self.indice_inflexao = melhor_indice

    # ----------------------------------------------------------------------------------------
    def _avaliar_erro(self):
        self.erro_mse = float(np.mean((self.y - self.modelo) ** 2))

    # ----------------------------------------------------------------------------------------
    def _gerar_plot(self):
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
