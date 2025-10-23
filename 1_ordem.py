import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema de primeira ordem
K = 2.0  # ganho estático
tau = 1.5  # constante de tempo (s)
t_final = 10  # duração da simulação
dt = 0.01  # passo de tempo

# Geração do vetor de tempo
t = np.arange(0, t_final, dt)

# Entrada: degrau unitário
u = np.ones_like(t)

# Resposta exata (sem ruído)
y_clean = K * (1 - np.exp(-t / tau))

# Adição de ruído gaussiano
noise_amplitude = 0.005 * K  # 5% do ganho
noise = np.random.normal(0, noise_amplitude, size=t.shape)
y_noisy = y_clean + noise

# Exibição dos resultados
plt.figure(figsize=(8, 4))
plt.plot(t, u, 'k--', label='Entrada (degrau unitário)')
plt.plot(t, y_clean, 'b', label='Saída sem ruído')
plt.plot(t, y_noisy, 'r', label='Saída com ruído')
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau Unitário – Sistema de 1ª Ordem')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Se quiser a lista de dados
data = np.column_stack((t, u, y_noisy))
# print(data)  # mostra os 10 primeiros pontos

# ====================================================================
tam_amostra = y_noisy.shape[0]  # tamanho do conjunto, usado pra calculos
amplitude_degrau = 1  # amplitude degrau de entrada
y_inf = np.mean(y_noisy[-int(tam_amostra * 0.05):])  # valor da saida no t->inf
y_zerom = y_noisy[0]  # valor da saida no t-> 0-

K = (y_inf - y_zerom) / amplitude_degrau  # ganho
y_tau = 0.632 * (y_inf - y_zerom) + y_zerom  # valor da saida onde tem o tau
index_tau = np.abs(
    y_noisy - y_tau).argmin()  # valor mais proximo de tau (subtrai o y_tau de todos, e ve o que da mais proximo)

tau = index_tau * dt
print(f"{K:.3f}/({tau}s+1)")
