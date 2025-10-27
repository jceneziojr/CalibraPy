import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import pynumdiff
from scipy.signal import lti, step


def eta_from_lambda(lmbd_target):
    def f(eta):
        _x = np.log(eta) / (eta - 1)
        return _x * np.exp(-_x) - lmbd_target

    # procura um intervalo onde há troca de sinal
    eta_vals = np.linspace(0.0001, 0.9999, 1000)
    f_vals = [f(e) for e in eta_vals]

    # identifica pares consecutivos onde há troca de sinal
    sign_changes = np.where(np.sign(f_vals[:-1]) != np.sign(f_vals[1:]))[0]
    if len(sign_changes) == 0:
        raise ValueError("Nenhuma troca de sinal encontrada — talvez λ esteja fora do domínio possível.")

    # usa o primeiro intervalo que muda de sinal
    a, b = eta_vals[sign_changes[0]], eta_vals[sign_changes[0] + 1]

    sol = root_scalar(f, bracket=(a, b), method='brentq')
    return sol.root


# Parâmetros do sistema de segunda ordem (sobreamortecido)
K = 2.0  # ganho estático
wn = 2.0  # frequência natural [rad/s]
zeta = 2  # fator de amortecimento (>1 para sobreamortecido)

t_final = 30  # duração da simulação [s]
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
np.random.seed(42)
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
plt.figure(figsize=(8, 5))
plt.plot(lmbd, eta, linewidth=2)
plt.ylabel(r'$\eta$', fontsize=14)
plt.xlabel(r'$\lambda$', fontsize=14)
plt.title(r'Curva $\lambda(\eta) = \frac{\ln(\eta)}{\eta - 1} e^{-\frac{\ln(\eta)}{\eta - 1}}$', fontsize=14)
plt.grid(True)
plt.show()

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

from sklearn.metrics import mean_squared_error


# =========================
# AJUSTE AUTOMÁTICO DO PONTO DE INFLEXÃO
# =========================

def calcular_y_modelo(indice_ponto_inflexao):
    """Calcula o modelo (y_novo) a partir de um índice de ponto de inflexão."""
    x0, y0 = t[indice_ponto_inflexao], x_hat[indice_ponto_inflexao]
    Mi = dxdt_hat[indice_ponto_inflexao]

    tm = x0 + (1 - y0) / Mi
    valor_lambda = (tm - m1) * Mi

    try:
        eta_valor = eta_from_lambda(valor_lambda)
    except ValueError:
        return np.inf, None  # λ fora do domínio, penaliza erro alto

    tau_1 = (eta_valor ** (eta_valor / (1 - eta_valor))) / Mi
    tau_2 = (eta_valor ** (1 / (1 - eta_valor))) / Mi
    tau_d = m1 - tau_1 - tau_2

    wn_2 = 1 / (tau_1 * tau_2)
    wn_n = wn_2 ** 0.5
    constante = (tau_2 + tau_1) / (tau_1 * tau_2)
    xi = constante / (2 * wn_n)

    num = [wn_n ** 2]
    den = [1, 2 * xi * wn_n, wn_n ** 2]
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
max_passos = 30  # distância máxima (em índices) para procurar a partir do índice inicial
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

# Se certificar que temos um y modelo válido
if melhor_y is None:
    raise RuntimeError("Melhor modelo não foi gerado — verifique a busca ou os parâmetros.")

# Calcula ponto e tangente a partir do melhor índice encontrado
x0 = t[melhor_indice]
y0 = x_hat[melhor_indice]
Mi = dxdt_hat[melhor_indice]

# Escolhe alcance horizontal da reta tangente (ex.: ± 2 segundos ou limite do vetor t)
span = 2.0
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
