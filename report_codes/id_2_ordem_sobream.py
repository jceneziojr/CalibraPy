import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step
from sklearn.metrics import mean_squared_error
from scipy.optimize import root_scalar
import pynumdiff

plt.rcParams['font.family'] = 'Courier New'


class SundaresanSobreamortecido:
    """
    Identificação de sistemas de 2ª ordem sobreamortecidos usando o método de Sundaresan.
    """

    # identificador
    TIPO_AJUSTE = "2a_ordem_sobreamortecido"

    def __init__(self, t, y, amplitude_degrau=1.0, dt=None):
        self.t = np.array(t)
        self.y = np.array(y)
        self.amplitude_degrau = float(amplitude_degrau)
        self.dt = dt if dt is not None else float(t[1] - t[0])

        # parâmetros de saída
        self.K = None
        self.xi = None
        self.wn = None
        self.tau_d = None
        self.modelo = None
        self.erro_mse = None
        self.indice_inflexao = None

        # processamento
        self._ajustar_modelo()
        self._avaliar_erro()
        self._gerar_plot()

    # =====================================================================
    # utilitário interno
    # =====================================================================
    @staticmethod
    def eta_from_lambda(lmbd_target):
        """Resolve η dado λ usando root_scalar."""

        def f(eta):
            _x = np.log(eta) / (eta - 1)
            return _x * np.exp(-_x) - lmbd_target

        eta_vals = np.linspace(0.0001, 0.9999, 1000)
        f_vals = [f(e) for e in eta_vals]

        sign_changes = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
        if len(sign_changes) == 0:
            raise ValueError("λ fora do domínio.")

        a = eta_vals[sign_changes[0]]
        b = eta_vals[sign_changes[0] + 1]

        return root_scalar(f, bracket=(a, b), method="brentq").root

    # =====================================================================
    def _normalizar(self):
        tam = len(self.y)

        y_inf = float(np.mean(self.y[-int(tam * 0.05):]))
        y_zerom = float(self.y[0])

        self.K = (y_inf - y_zerom) / self.amplitude_degrau

        y_adj = self.y - y_zerom
        valor_y_ss = float(np.mean(y_adj[int(tam * 0.9):]))

        y_norm = y_adj / valor_y_ss
        return y_norm, y_zerom

    # =====================================================================
    def _calcular_area_m1(self, y_norm):
        dif = np.maximum(1 - y_norm, 0)
        return float(np.sum(dif) * self.dt)

    # =====================================================================
    def _avaliar_modelo_indice(self, idx, t, x_hat, dxdt_hat, d2xdt_hat, m1):
        """Calcula MSE para um candidato a ponto de inflexão."""

        x0, y0 = t[idx], x_hat[idx]
        Mi = dxdt_hat[idx]

        tm = x0 + (1 - y0) / Mi
        lamb = (tm - m1) * Mi

        try:
            eta = self.eta_from_lambda(lamb)
        except ValueError:
            return np.inf, None, None, None, None

        tau1 = (eta ** (eta / (1 - eta))) / Mi
        tau2 = (eta ** (1 / (1 - eta))) / Mi
        tau_d = m1 - tau1 - tau2

        wn2 = 1 / (tau1 * tau2)
        wn = np.sqrt(wn2)
        xi = (tau1 + tau2) / (2 * np.sqrt(tau1 * tau2))

        num = [wn ** 2]
        den = [1, 2 * xi * wn, wn ** 2]
        sys = lti(num, den)

        _, y_step = step(sys, T=t)

        y_new = np.zeros_like(y_step)
        mask = t >= tau_d
        y_new[mask] = np.interp(t[mask] - tau_d, t, y_step)

        mse = mean_squared_error(x_hat, y_new)

        return mse, y_new, xi, wn, tau_d

    # =====================================================================
    def _ajustar_modelo(self, window_size=10, num_iter=3, max_passos=30, delta_idx=5, tolerancia=1e-4):
        """Algoritmo principal do método de Sundaresan."""

        y_norm, y0 = self._normalizar()
        m1 = self._calcular_area_m1(y_norm)

        # derivadas suavizadas
        x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            y_norm, self.dt, kernel="mean", window_size=window_size, num_iterations=num_iter
        )
        _, d2xdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(
            dxdt_hat, self.dt, kernel="mean", window_size=window_size, num_iterations=num_iter
        )

        # ponto inicial de inflexão
        idx_inf = int(np.where(np.diff(np.sign(d2xdt_hat)))[0][0])

        # primeira tentativa
        best_mse, best_y, best_xi, best_wn, best_tau_d = \
            self._avaliar_modelo_indice(idx_inf, self.t, x_hat, dxdt_hat, d2xdt_hat, m1)

        best_idx = idx_inf

        # busca refinada
        for off in range(delta_idx, max_passos * delta_idx + 1, delta_idx):

            # frente
            i_fwd = idx_inf + off
            if i_fwd < len(self.t):
                mse, y_mod, xi, wn, tau_d = \
                    self._avaliar_modelo_indice(i_fwd, self.t, x_hat, dxdt_hat, d2xdt_hat, m1)

                if mse < best_mse:
                    best_mse, best_y, best_xi, best_wn, best_tau_d = mse, y_mod, xi, wn, tau_d
                    best_idx = i_fwd

            # trás
            i_bwd = idx_inf - off
            if i_bwd >= 0:
                mse, y_mod, xi, wn, tau_d = \
                    self._avaliar_modelo_indice(i_bwd, self.t, x_hat, dxdt_hat, d2xdt_hat, m1)

                if mse < best_mse:
                    best_mse, best_y, best_xi, best_wn, best_tau_d = mse, y_mod, xi, wn, tau_d
                    best_idx = i_bwd

            if best_mse < tolerancia:
                break

        # guarda resultados finais
        self.modelo = best_y * self.K + y0
        self.xi = best_xi
        self.wn = best_wn
        self.tau_d = best_tau_d
        self.indice_inflexao = best_idx

    # =====================================================================
    def _avaliar_erro(self):
        self.erro_mse = float(np.mean((self.y - self.modelo) ** 2))

    # =====================================================================
    def _gerar_plot(self):
        self.fig_dyn, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.t, self.y, "r", label="Dados")
        ax.plot(self.t, self.modelo, "b", label="Modelo aproximado")
        ax.set_xlabel("Tempo [s]", fontsize=14)
        ax.set_ylabel("Amplitude", fontsize=14)
        ax.set_title("Comparação entre dados e modelo dinâmico", fontsize=14)
        ax.grid(True)
        ax.legend()
        self.fig_dyn.tight_layout()


K_real = 2.0
wn_real = 2.0
zeta_real = 1.001
t_final = 30
dt = 0.01
t = np.arange(0, t_final, dt)

num = [K_real * wn_real ** 2]
den = [1, 2 * zeta_real * wn_real, wn_real ** 2]

sistema = lti(num, den)
_, y_clean = step(sistema, T=t)

np.random.seed(42)
noise = np.random.normal(0, 0.005 * K_real, size=t.shape)
y_noisy = y_clean + noise

# Aplicando a classe
modelo_sob = SundaresanSobreamortecido(t, y_noisy, amplitude_degrau=1, dt=dt)
