import numpy as np
from scipy.signal import lti, step

from .id_2_ordem_subam import SundaresanSubamortecido


class SundaresanCriticamenteAmortecido(SundaresanSubamortecido):
    TIPO_AJUSTE = "2a_ordem_critico"


K_real = 2.0
wn_real = 2.0
zeta_real = 1
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
modelo_crit = SundaresanCriticamenteAmortecido(t, y_noisy, amplitude_degrau=1, dt=dt)
