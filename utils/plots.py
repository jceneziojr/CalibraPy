import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step

plt.rcParams['font.family'] = 'Courier New'

# ============================
#  SISTEMA DE PRIMEIRA ORDEM
# ============================

tau = 1.0
dt = 0.01
t_resp = np.arange(0, 10, dt)

# Função de transferência: 1 / (tau*s + 1)
num = [1]
den = [tau, 1]
sistema = lti(num, den)

t_out, y_out = step(sistema, T=t_resp)

# ============================
#  GRÁFICO
# ============================
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(t_out, y_out, color='red', linewidth=2)

ax.set_xlabel("Tempo [s]", fontsize=14)
ax.set_ylabel("Amplitude da saída do sensor", fontsize=14)
ax.set_title("Resposta ao degrau de sistema de primeira ordem", fontsize=14)

ax.grid(True)
fig.tight_layout()
fig.show()
