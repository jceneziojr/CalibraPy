import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Courier New'

points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

forward_dict = {
    0: [0.94, 0.91, 0.97, 0.94, 0.88],
    1: [2.86, 2.89, 2.92, 2.80, 3.15],
    2: [4.82, 4.88, 4.90, 4.87, 5.03],
    3: [7.14, 6.82, 6.99, 6.96, 6.97],
    4: [8.94, 8.82, 8.95, 8.80, 9.07],
    5: [10.92, 11.08, 11.07, 11.01, 10.97],
    6: [13.19, 13.07, 12.84, 13.19, 13.09],
    7: [15.04, 14.91, 15.16, 15.15, 15.01],
    8: [17.09, 17.12, 16.91, 17.09, 17.09],
    9: [18.97, 19.16, 18.99, 18.91, 19.06],
    10: [21.10, 21.15, 20.98, 21.08, 20.81]
}

backward_dict = {
    0: [0.99, 1.06, 1.08, 1.17, 1.02],
    1: [3.06, 3.11, 3.19, 3.10, 2.88],
    2: [5.04, 5.12, 4.94, 5.00, 4.98],
    3: [7.04, 7.11, 7.16, 7.17, 7.04],
    4: [9.07, 8.95, 9.10, 9.10, 8.81],
    5: [10.82, 11.10, 11.00, 11.06, 10.92],
    6: [12.90, 12.91, 13.04, 13.06, 12.91],
    7: [15.18, 14.93, 14.93, 15.02, 15.05],
    8: [16.87, 17.02, 17.15, 17.10, 16.97],
    9: [19.03, 18.88, 18.94, 19.00, 19.05],
    10: [20.88, 21.12, 21.15, 21.02, 21.18]
}


class CaracteristicasEstaticas:

    def __init__(self, points, forward_dict, backward_dict, ordem_ajuste=1):
        self.points = points
        self.forward_dict = forward_dict
        self.backward_dict = backward_dict
        self.ordem_ajuste = ordem_ajuste

        # Cálculos
        self._calcular_medias()
        self._calcular_erro_aleatorio()
        self._calcular_repetibilidade()
        self._ajuste_polinomial()
        self._avaliacao_do_ajuste()
        self._calcular_histerese()
        self._gerar_plots()

    # ============================================================
    def _calcular_medias(self):
        """Médias forward / backward e pontos médios."""
        self.fwd_avg = [float(np.mean(self.forward_dict[p])) for p in self.points]
        self.bwd_avg = [float(np.mean(self.backward_dict[p])) for p in self.points]
        self.avg_pts = [(f + b) / 2 for f, b in zip(self.fwd_avg, self.bwd_avg)]

    # ============================================================
    def _calcular_erro_aleatorio(self):
        """Erro aleatório local e global."""
        self.erro_aleatorio_local = {}
        self.erro_aleatorio_global = 0

        for idx, p in enumerate(self.points):

            media_do_ponto = self.avg_pts[idx]
            todas = self.forward_dict[p] + self.backward_dict[p]

            EA_abs = np.abs([y - media_do_ponto for y in todas])
            max_local = float(np.max(EA_abs))
            self.erro_aleatorio_local[p] = max_local

            if max_local > self.erro_aleatorio_global:
                self.erro_aleatorio_global = max_local

    # ============================================================
    def _calcular_repetibilidade(self):
        """Diferença max-min % para cada ponto."""
        repetibilidade = {}

        for p in self.points:
            repetibilidade[p] = float(
                (np.max(self.forward_dict[p] + self.backward_dict[p]) -
                 np.min(self.forward_dict[p] + self.backward_dict[p])) * 100 / self.points[-1]
            )

        self.repetibilidade = repetibilidade
        self.repetibilidade_max = max(repetibilidade.values())

    # ============================================================
    def _ajuste_polinomial(self):
        """Ajuste polinomial e sensibilidade."""
        self.curva_calib_estatica = np.polyfit(self.points, self.avg_pts, self.ordem_ajuste)
        self.sensibilidade = np.polyder(self.curva_calib_estatica)

    # ============================================================
    def _avaliacao_do_ajuste(self):
        """Erro de linearidade ou conformidade."""
        valores = np.polyval(self.curva_calib_estatica, self.points)
        diffs = np.abs(np.array(valores) - np.array(self.avg_pts))

        Dfm = np.max(diffs)
        self.erro_ajuste = (Dfm / self.points[-1]) * 100

    # ============================================================
    def _calcular_histerese(self):
        """Histerese: diferença entre forward e backward."""
        diferencas = np.abs(np.array(self.fwd_avg) - np.array(self.bwd_avg))
        Hmax = np.max(diferencas)
        self.erro_histerese = (Hmax / self.points[-1]) * 100

    # ============================================================
    def _gerar_plots(self):
        """Gera as três figuras: curva, sensibilidade e histerese."""
        x_plot = np.linspace(min(self.points) - max(self.points) * 0.15, max(self.points) + max(self.points) * 0.15,
                             300)  # coloco 10% a mais de pontos em cada direção para fazer o plot

        # Curva de calibração
        self.fig_ccs, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.points, self.avg_pts, 'o', label='Pontos adquiridos', markersize=8, )
        ax.plot(x_plot, np.poly1d(self.curva_calib_estatica)(x_plot), '-', label='Curva')
        ax.set_xlabel('Entrada', fontsize=14)
        ax.set_ylabel('Saída', fontsize=14)
        ax.set_title('Curva de calibração estática', fontsize=14)
        ax.grid(True)
        ax.legend()
        self.fig_ccs.tight_layout()

        # Sensibilidade
        self.fig_csens, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(x_plot, np.poly1d(self.sensibilidade)(x_plot), '-', label='Sensibilidade')
        ax1.set_xlabel('Entrada', fontsize=14)
        ax1.set_ylabel('Sensibilidade', fontsize=14)
        ax1.set_title('Curva de sensibilidade', fontsize=14)
        ax1.grid(True)
        ax1.margins(y=0.9)
        ax1.legend()
        self.fig_csens.tight_layout()

        # Histerese
        self.fig_hist, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(self.points, self.fwd_avg, 'o', label='Forward', markersize=8, )
        ax2.plot(self.points, self.bwd_avg, 'x', label='Backward', markersize=8, )
        ax2.set_xlabel('Entrada', fontsize=14)
        ax2.set_ylabel('Saída', fontsize=14)
        ax2.set_title('Análise de histerese', fontsize=14)
        ax2.grid(True)
        ax2.margins(y=0.9)
        ax2.legend()
        self.fig_hist.tight_layout()


car_est = CaracteristicasEstaticas(points=points, forward_dict=forward_dict, backward_dict=backward_dict,
                                   ordem_ajuste=1)
