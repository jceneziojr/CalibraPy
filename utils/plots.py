import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step

plt.rcParams['font.family'] = 'Courier New'

# ===============================
# Parâmetros do sistema
# ===============================
wn = 8.0
zeta = 0.25     # subamortecido
dt = 0.0005
t_resp = np.arange(0, 4, dt)

num = [wn**2]
den = [1, 2*zeta*wn, wn**2]

sistema = lti(num, den)
t, y = step(sistema, T=t_resp)

# ===============================
# Valor final (1)
# ===============================
y_final = 1.0

# ===============================
# Primeira vez que a curva encosta em 1
# ===============================
idx_touch = np.where(y >= 1)[0][0]
t_touch = t[idx_touch]

# ===============================
# Gráfico
# ===============================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, y, 'r', label="Subamortecido (ζ = 0.25)")

# ---------------------------------------
# Linha vertical onde toca em 1
# ---------------------------------------
ax.plot([t_touch, t_touch], [0, 1], 'k--', linewidth=1.2)

ax.text(t_touch, -0.05, "tm", ha='center', va='top',
        fontsize=14, fontweight='bold')

# ===========================================================
# ÁREA HACHURADA — alternando acima/abaixo de 1
# ===========================================================

# Identificar mudanças de sinal em (y - 1)
sign_changes = np.where(np.diff(np.sign(y - 1)) != 0)[0]
interval_edges = [0] + list(sign_changes) + [len(t) - 1]

# Para cada intervalo entre cruzamentos:
for i in range(len(interval_edges) - 1):

    i1 = interval_edges[i]
    i2 = interval_edges[i + 1]

    t_seg = t[i1:i2+1]
    y_seg = y[i1:i2+1]

    # Se estiver ANTES do toque:
    if i2 < idx_touch:
        # hachurar entre y(t) e 1
        ax.fill_between(t_seg, y_seg, 1,
                        hatch='..', edgecolor='gray',
                        facecolor='none')
        continue

    # Depois do toque:
    # Se curva está abaixo de 1 → hachurar entre y e 1
    if np.mean(y_seg) < 1:
        ax.fill_between(t_seg, y_seg, 1,
                        hatch='..', edgecolor='gray',
                        facecolor='none')
    else:
        # Curva acima de 1 → hachurar entre 1 e y
        ax.fill_between(t_seg, 1, y_seg,
                        hatch='..', edgecolor='gray',
                        facecolor='none')


ax.text(0.075, 0.9, "m1", fontsize=16, fontweight='bold')
# ===============================
# Ajuste dos eixos
# ===============================
ax.set_xlim(0, t_resp[-1])
ax.set_ylim(0, max(y) * 1.1)

# ===============================
# Ajustes visuais
# ===============================
ax.set_xlabel("Tempo [s]", fontsize=14)
ax.set_ylabel("Amplitude", fontsize=14)
ax.set_title("Resposta ao degrau subamortecido", fontsize=14)
ax.grid(True)
# ax.legend(fontsize=12)
fig.tight_layout()
fig.show()
