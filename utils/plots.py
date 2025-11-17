import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Courier New'

# ===============================
# Dados de calibração (exemplo)
# ===============================
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0.1, 1.2, 2.1, 3.0, 4.1, 5.0])

# Ajuste linear (reta de calibração)
coef = np.polyfit(x, y, 1)
y_fit = np.polyval(coef, x)

# ===============================
# Gráfico
# ===============================
fig, ax = plt.subplots(figsize=(10, 5))

# Pontos experimentais
ax.plot(x, y, 'rx', label="Pontos adquiridos")

# Reta de calibração
ax.plot(x, y_fit, 'b-', label=f"Ajuste de primeiro grau", linewidth=2)

# ===============================
# Ajustes visuais
# ===============================
ax.set_xlabel("Entrada", fontsize=14)
ax.set_ylabel("Saída", fontsize=14)
ax.set_title("Curva de calibração estática", fontsize=14)
ax.grid(True)
ax.legend(fontsize=12)
ax.set_xlim(min(x) - 0.5, max(x) + 0.5)
ax.set_ylim(min(y) - 0.5, max(y) + 0.5)

fig.tight_layout()
fig.show()
