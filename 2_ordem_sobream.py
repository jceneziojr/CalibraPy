import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import pynumdiff
from scipy.signal import lti, step


def eta_from_lambda(lmbd_target):
    # encontrando o valor de eta, pelo lambda
    def f(eta):
        _x = np.log(eta) / (eta - 1)
        return _x * np.exp(-_x) - lmbd_target

    sol = root_scalar(f, bracket=(0.0001, 0.9999), method='brentq')
    return sol.root


# Parâmetros do sistema de segunda ordem (sobreamortecido)
K = 2.0  # ganho estático
wn = 2.0  # frequência natural [rad/s]
zeta = 1.5  # fator de amortecimento (>1 para sobreamortecido)

t_final = 10  # duração da simulação [s]
dt = 0.01  # passo de tempo [s]

# Vetor de tempo
t = np.arange(0, t_final, dt)

# Entrada: degrau unitário
u = np.ones_like(t)

# Cálculo dos polos reais (sobreamortecido)
s1 = -wn * (zeta - np.sqrt(zeta ** 2 - 1))
s2 = -wn * (zeta + np.sqrt(zeta ** 2 - 1))

# Resposta exata ao degrau unitário
# Fórmula da resposta ao degrau para sistema sobreamortecido
y_clean = K * (1 - (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1))

# Adição de ruído gaussiano (5% do ganho)
noise_amplitude = 0.005 * K
noise = np.random.normal(0, noise_amplitude, size=t.shape)
y_noisy = y_clean + noise

# Exibição dos resultados
# plt.figure(figsize=(8, 4))
# plt.plot(t, u, 'k--', label='Entrada (degrau unitário)')
# plt.plot(t, y_clean, 'b', label='Saída sem ruído')
# plt.plot(t, y_noisy, 'r', label='Saída com ruído')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Amplitude')
# plt.title('Resposta ao Degrau Unitário – Sistema de 2ª Ordem Sobreamortecido')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# ========================================================================================================
# CURVA ETA X LAMBDA
eta = np.linspace(0.0001, 1, 10000)  # evita eta=1, pois causaria divisão por zero

# Calcula chi e lambda
chi = np.log(eta) / (eta - 1)

lmbd = chi * np.exp(-chi)

# Plota
# plt.figure(figsize=(8, 5))
# plt.plot(lmbd, eta, linewidth=2)
# plt.ylabel(r'$\eta$', fontsize=14)
# plt.xlabel(r'$\lambda$', fontsize=14)
# plt.title(r'Curva $\lambda(\eta) = \frac{\ln(\eta)}{\eta - 1} e^{-\frac{\ln(\eta)}{\eta - 1}}$', fontsize=14)
# plt.grid(True)
# plt.show()

# ========================================================================================================
tam_amostra = y_noisy.shape[0]
amplitude_degrau = 1  # amplitude degrau de entrada
y_inf = np.mean(y_noisy[-int(tam_amostra * 0.05):])
y_zerom = y_noisy[0]  # valor da saida no t-> 0-

K = (y_inf - y_zerom) / amplitude_degrau  # ganho

y_adj = y_noisy - y_noisy[0]  # tirando o valor da condição inicial

valor_y_ss = np.mean(y_noisy[int(tam_amostra * 0.9):])  # valor em regime permanente, pegando os ultimos 10% dos dados

y_normalizado = y_adj / valor_y_ss

plt.figure(figsize=(8, 4))
# plt.plot(t, u, 'k--', label='Entrada (degrau unitário)')
# plt.plot(t, y_clean, 'b', label='Saída sem ruído')
# plt.plot(t, y_noisy, 'r', label='Saída com ruído')
# plt.plot(t, y_normalizado, 'g', label='Saída ajustada')
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau Unitário – Sistema de 2ª Ordem Sobreamortecido')
plt.grid(True)
plt.tight_layout()
plt.ylim([0, 1])

dif_curva = 1 - y_normalizado  # pra pegar a area mi
dif_curva[dif_curva < 0] = 0  # zerando os valores que poderiam ficar acima de 1, pois deve estar tudo abaixo

area = m1 = np.sum(dif_curva) * dt  # valor de m1
print(f"m1 = {area}")

# ==================================================
# pegando derivada e segunda derivada, pra achar o ponto de inflexão
x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(y_normalizado, dt, kernel='mean', window_size=10,
                                                                num_iterations=3)
x2_hat, d2xdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(dxdt_hat, dt, kernel='mean', window_size=10,
                                                                  num_iterations=3)

plt.plot(t, x_hat, 'r', label='Saída filtrada')
# plt.plot(t, dxdt_hat, 'b', label='Derivada saída')
# plt.plot(t, d2xdt_hat, 'g', label='Derivada segunda saída')
# print(np.where(d2xdt_hat == 0))

indice_ponto_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][1]  # ponto de inflexão
ponto_inflexao = (x0, y0) = (t[indice_ponto_inflexao], x_hat[indice_ponto_inflexao])
Mi = dxdt_hat[indice_ponto_inflexao]

x_reta = np.linspace(x0 - 2, x0 + 2, 100)
y_reta = Mi * (x_reta - x0) + y0

plt.plot(x_reta, y_reta, 'r--', label='Tangente')
plt.plot(x0, y0, 'ko', label='Ponto')
print(f"Mi = {Mi}")

tm = x0 + (1 - y0) / Mi
print(f"tm = {tm}")
valor_lambda = (tm - m1) * Mi
print(f"lambda = {valor_lambda}")

eta_valor = eta_from_lambda(valor_lambda)
print(f"eta = {eta_valor}")
tau_1 = (eta_valor ** (eta_valor / (1 - eta_valor))) / Mi
tau_2 = (eta_valor ** (1 / (1 - eta_valor))) / Mi
tau_d = m1 - tau_1 - tau_2

wn_2 = 1 / (tau_1 * tau_2)
wn_n = wn_2 ** (1 / 2)

print(f"{wn} -> {wn_n}")
constante = (tau_2 + tau_1) / (tau_1 * tau_2)
xi = constante / (2 * wn_n)
print(f"{zeta} -> {xi}")

num = [wn_n ** 2]
den = [1, 2 * xi * wn_n, wn_n ** 2]
sistema = lti(num, den)

_, y_novo = step(sistema, T=t - tau_d)  # desloca o tempo
y_novo[t < tau_d] = 0  # mantém zero antes do atraso

plt.plot(t, y_novo, label=f'Resposta ao degrau')
plt.legend()
plt.show()
