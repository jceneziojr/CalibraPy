import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import pynumdiff
from scipy.signal import lti, step

# ============================================================================================
# DADOS SIMULAÇÃO
# ============================================================================================

# Parâmetros do sistema
K = 2.0
wn = 2.0
xi = 0.95  # subamortecido

# Cria sistema de segunda ordem
num = [K * wn ** 2]  # numerador
den = [1, 2 * xi * wn, wn ** 2]  # denominador
sistema = lti(num, den)

# Vetor de tempo
t_final = 30
dt = 0.01
t = np.arange(0, t_final, dt)

# Resposta ao degrau
t_out, y_clean = step(sistema, T=t)

# Adição de ruído
noise_amplitude = 0.005 * K
np.random.seed(42)
noise = np.random.normal(0, noise_amplitude, size=t.shape)
y_noisy = y_clean + noise
y_noisy = y_noisy + np.ones_like(y_noisy)
# Exibição dos resultados
plt.figure(figsize=(8, 4))
plt.plot(t, y_clean, 'b', label='Saída sem ruído')
plt.plot(t, y_noisy, 'r', label='Saída com ruído')
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau Unitário – Sistema de 2ª Ordem Subamortecido')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ========================================================================================================
# CURVA XI X LAMBDA
# ========================================================================================================
xi = np.linspace(0.0001, 1, 10000)  # evita xi=1, pois causaria divisão por zero


# Calcula lambda

# chi = np.acos(xi) / (np.sqrt(1 - (xi ** 2)))
#
# lmbd = chi * np.exp(-xi * chi)
#
# # Plota
# plt.figure(figsize=(8, 5))
# plt.plot(lmbd, xi, linewidth=2)
# plt.ylabel(r'$\xi$', fontsize=14)
# plt.xlabel(r'$\lambda$', fontsize=14)
# plt.axvline(np.exp(-1), color='r', linestyle='--', linewidth=1.5, label=r'$\lambda = e^{-1}$')
# plt.title(r'Curva $\lambda(\xi)$', fontsize=14)
# plt.grid(True)
# plt.show()

# ========================================================================================================
# CALCULO XI
# ========================================================================================================
def xi_from_lambda(lmbd_target):
    def f(xi):
        chi = np.arccos(xi) / np.sqrt(1 - xi ** 2)
        return chi * np.exp(-xi * chi) - lmbd_target

    # domínio válido: xi ∈ (-1, 1)
    xi_vals = np.linspace(-0.9999, 0.9999, 2000)
    f_vals = [f(x) for x in xi_vals]

    # identifica pares consecutivos onde há troca de sinal
    sign_changes = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
    if len(sign_changes) == 0:
        raise ValueError("Nenhuma troca de sinal encontrada — talvez λ esteja fora do domínio possível.")

    # usa o primeiro intervalo que muda de sinal
    a, b = xi_vals[sign_changes[0]], xi_vals[sign_changes[0] + 1]

    sol = root_scalar(f, bracket=(a, b), method='brentq')
    return sol.root


# ========================================================================================================
# CALCULO DO GANHO K
# ========================================================================================================

tam_amostra = y_noisy.shape[0]
amplitude_degrau = 1  # amplitude degrau de entrada
y_inf = np.mean(y_noisy[-int(tam_amostra * 0.05):])
y_zerom = y_noisy[0]  # valor da saida no t-> 0-

K = (y_inf - y_zerom) / amplitude_degrau  # ganho

print(f"{y_inf} / {y_zerom} / {K}")

# ========================================================================================================
# REMOÇÃO PATAMAR INICIAL
# ========================================================================================================

y_adj = y_noisy - y_noisy[0]  # tirando o valor da condição inicial
# print(f"{y_adj[0:10]} / {y_adj[-10:]}")
# ========================================================================================================
# NORMALIZAÇÃO
# ========================================================================================================

valor_y_ss = np.mean(y_adj[int(tam_amostra * 0.9):])  # valor em regime permanente, pegando os ultimos 10% dos dados

print(f"{valor_y_ss}")

y_normalizado = y_adj / valor_y_ss

plt.figure(figsize=(8, 4))
# plt.plot(t, u, 'k--', label='Entrada (degrau unitário)')
# plt.plot(t, y_clean, 'b', label='Saída sem ruído')
# plt.plot(t, y_noisy, 'r', label='Saída com ruído')
plt.plot(t, y_normalizado, 'g', label='Saída ajustada')
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude')
plt.title('Resposta ao Degrau Unitário – Sistema de 2ª Ordem Sobreamortecido')
plt.grid(True)
plt.tight_layout()
# plt.ylim([0, np.max(y_normalizado) * 1.1])
plt.show()

# ========================================================================================================
# CALCULO AREA m1
# ========================================================================================================
# Diferença em relação ao regime permanente, pra separar de forma simples
diff = y_normalizado - 1

# Áreas separadas
area_acima = np.sum(diff[diff > 0]) * dt  # acima da linha
area_abaixo = np.sum(-diff[diff < 0]) * dt  # abaixo da linha

m1 = area_abaixo - area_acima

print(f"m1 = {m1}")

# ========================================================================================================
# OUTROS PASSOS
# ========================================================================================================

# pegando derivada e segunda derivada, pra achar o ponto de inflexão
x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(y_normalizado, dt, kernel='mean', window_size=10,
                                                                num_iterations=3)
x2_hat, d2xdt_hat = pynumdiff.smooth_finite_difference.kerneldiff(dxdt_hat, dt, kernel='mean', window_size=10,
                                                                  num_iterations=3)
idx_primeiro_um = np.where(x_hat >= 1)[0][0]  # primeira vez que cruza 1 (o ponto de inflexão tá limitado até ali)
print(idx_primeiro_um)

plt.plot(t, x_hat, 'r', label='Saída filtrada')
# plt.plot(t, dxdt_hat, 'b', label='Derivada saída')
# plt.plot(t, d2xdt_hat, 'g', label='Derivada segunda saída')
plt.grid(True)
plt.tight_layout()

# indice_ponto_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][0]
# print(f"indice = {indice_ponto_inflexao}")
# ponto_inflexao = (x0, y0) = (t[indice_ponto_inflexao], x_hat[indice_ponto_inflexao])
# Mi = dxdt_hat[indice_ponto_inflexao]
#
# x_reta = np.linspace(x0 - 1, x0 + 1, 100)
# y_reta = Mi * (x_reta - x0) + y0
#
# plt.plot(x_reta, y_reta, 'r--', label='Tangente')
# plt.plot(x0, y0, 'ko', label='Ponto')
# plt.show()

from sklearn.metrics import mean_squared_error


def calcular_y_modelo(indice_ponto_inflexao):
    """Calcula o modelo (y_novo) a partir de um índice de ponto de inflexão."""
    x0, y0 = t[indice_ponto_inflexao], x_hat[indice_ponto_inflexao]
    Mi = dxdt_hat[indice_ponto_inflexao]

    tm = x0 + (1 - y0) / Mi
    valor_lambda = (tm - m1) * Mi

    try:
        xi_valor = xi_from_lambda(valor_lambda)
    except ValueError:
        return np.inf, None  # λ fora do domínio, penaliza erro alto

    # print(f"{xi_valor} / {tm} / {m1} / {Mi}")

    wn_n = (np.acos(xi_valor) / np.sqrt(1 - (xi_valor ** 2))) * (1 / (tm - m1))
    tau_d = m1 - (2 * xi_valor) / wn_n

    # print(f"{wn_n} / {tau_d}")

    num = [wn_n ** 2]
    den = [1, 2 * xi_valor * wn_n, wn_n ** 2]

    sistema = lti(num, den)

    _, _y = step(sistema, T=t)

    y_novo = np.zeros_like(_y)
    mask = t >= tau_d
    y_novo[mask] = np.interp(t[mask] - tau_d, t, _y)

    mse = mean_squared_error(x_hat, y_novo)
    return mse, y_novo


# índice inicial
indice_ponto_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][0]

# parâmetros de busca
max_passos = 25  # distância máxima (em índices) para procurar a partir do índice inicial
delta_idx = 5  # incremento de índice (evita conflito com scipy.signal.step)
tolerancia = 1e-4  # MSE alvo para parar a busca

melhor_mse, melhor_y = calcular_y_modelo(indice_ponto_inflexao)
melhor_indice = indice_ponto_inflexao

# busca em torno do índice inicial
for offset in range(delta_idx, max_passos * delta_idx + 1, delta_idx):
    # tenta para frente
    idx_forward = indice_ponto_inflexao + offset
    if idx_forward < len(t):
        mse_fwd, y_fwd = calcular_y_modelo(idx_forward)
        if mse_fwd < melhor_mse:
            melhor_mse = mse_fwd
            melhor_y = y_fwd
            melhor_indice = idx_forward

    # tenta para trás
    idx_backward = indice_ponto_inflexao - offset
    if idx_backward >= 0:
        mse_bwd, y_bwd = calcular_y_modelo(idx_backward)
        if mse_bwd < melhor_mse:
            melhor_mse = mse_bwd
            melhor_y = y_bwd
            melhor_indice = idx_backward

    if melhor_mse < tolerancia:
        break

print(f"Melhor índice de inflexão: {melhor_indice}")
print(f"Melhor MSE: {melhor_mse:.6f}")

indice_ponto_inflexao = np.where(np.diff(np.sign(d2xdt_hat)))[0][0]
ponto_inflexao = (t[melhor_indice], x_hat[melhor_indice])
Mi = dxdt_hat[indice_ponto_inflexao]

x_reta = np.linspace(ponto_inflexao[0] - 1, ponto_inflexao[0] + 1, 100)
y_reta = Mi * (x_reta - ponto_inflexao[0]) + ponto_inflexao[1]

plt.plot(x_reta, y_reta, 'r--', label='Tangente')
plt.plot(ponto_inflexao[0], ponto_inflexao[1], 'ko', label='Ponto')
plt.show()

# Calcula ponto e tangente a partir do melhor índice encontrado
x0 = t[melhor_indice]
y0 = x_hat[melhor_indice]
Mi = dxdt_hat[melhor_indice]

# Escolhe alcance horizontal da reta tangente (ex.: ± 2 segundos ou limite do vetor t)
span = 1.0
x_reta = np.linspace(max(0, x0 - span), min(t[-1], x0 + span), 200)
y_reta = Mi * (x_reta - x0) + y0

# opcional: calcula tm e outras quantidades para legendas/debug
tm = x0 + (1 - y0) / Mi if Mi != 0 else np.nan

# Plot final com ponto e tangente
plt.figure(figsize=(8, 4))
plt.plot(t, x_hat, 'r', label='Saída filtrada (x_hat)')
plt.plot(t, melhor_y, 'b', label='Melhor ajuste (y_novo)')
plt.plot(x_reta, y_reta, 'k--', linewidth=2, label='Tangente no ponto de inflexão')
plt.plot(x0, y0, 'ko', markersize=6, label=f'Ponto de inflexão (idx={melhor_indice})')
plt.axvline(x=tm, color='gray', linestyle=':', label=f'tm = {tm:.3f}s')
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude normalizada')
plt.title('Ajuste automático do ponto de inflexão — ponto e tangente')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ========================================================================================================
# NÃO FUNCIONA MUITO BEM PARA XI MUITO PEQUENO
# FAZER CLASSE
# ========================================================================================================
