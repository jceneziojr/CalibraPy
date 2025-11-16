from typing import Union
from datetime import datetime
import io

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from report_codes.static import CaracteristicasEstaticas, car_est
from report_codes.id_0_ordem import OrdemZero, modelo_0ordem
from report_codes.id_1_ordem import PrimeiraOrdem, modelo_1ordem
from report_codes.id_2_ordem_subam import SundaresanSubamortecido, modelo_sub
from report_codes.id_2_ordem_sobream import SundaresanSobreamortecido, modelo_sob
from report_codes.id_2_ordem_critico import SundaresanCriticamenteAmortecido, modelo_crit


class RelatorioCalibracao:
    """gerador do relatório de calibração estática e dinâmica."""

    # dicionario pra tratar do tipo de identificação
    CONFIG = {
        "0a_ordem": {
            "titulo": "Modelo de ordem 0:",
            "latex": lambda c: (0, c.K),
            "linhas": lambda c: [["Ganho", f"{c.K:.4f}"]],
        },
        "1a_ordem": {
            "titulo": "Modelo de primeira ordem:",
            "latex": lambda c: (1, c.K, c.tau),
            "linhas": lambda c: [
                ["Ganho", f"{c.K:.4f}"],
                ["Constante de tempo", f"{c.tau:.4f}"],
            ],
        },
        "2a_ordem_subamortecido": {
            "titulo": "Modelo de segunda ordem subamortecido:",
            "latex": lambda c: (2, c.K, c.tau_d, c.xi, c.wn),
            "linhas": lambda c: [
                ["Ganho", f"{c.K:.4f}"],
                ["Atraso puro de tempo", f"{c.tau_d:.4f}"],
                ["Coeficiente de amortecimento", f"{c.xi:.4f}"],
                ["Frequência natural", f"{c.wn:.4f}"],
            ],
        },
        "2a_ordem_sobreamortecido": {
            "titulo": "Modelo de segunda ordem sobreamortecido:",
            "latex": lambda c: (2, c.K, c.tau_d, c.xi, c.wn),
            "linhas": lambda c: [
                ["Ganho", f"{c.K:.4f}"],
                ["Atraso puro de tempo", f"{c.tau_d:.4f}"],
                ["Coeficiente de amortecimento", f"{c.xi:.4f}"],
                ["Frequência natural", f"{c.wn:.4f}"],
            ],
        },
        "2a_ordem_critico": {
            "titulo": "Modelo de segunda ordem criticamente amortecido:",
            "latex": lambda c: (2, c.K, c.tau_d, c.xi, c.wn),
            "linhas": lambda c: [
                ["Ganho", f"{c.K:.4f}"],
                ["Atraso puro de tempo", f"{c.tau_d:.4f}"],
                ["Coeficiente de amortecimento", f"{c.xi:.4f}"],
                ["Frequência natural", f"{c.wn:.4f}"],
            ],
        }
    }

    def __init__(self, pdf_file: str, sensor: str, responsavel: str,
                 sta: CaracteristicasEstaticas,
                 dyn: Union[
                     OrdemZero, PrimeiraOrdem,
                     SundaresanSobreamortecido, SundaresanSubamortecido,
                     SundaresanCriticamenteAmortecido
                 ],
                 unidade: str):

        self.pdf_file = pdf_file
        self.sensor = sensor
        self.responsavel = responsavel
        self.sta = sta
        self.dyn = dyn
        self.unidade = unidade
        self.story = []

        self.style_title = ParagraphStyle("Titulo", fontName="Courier",
                                          fontSize=16, alignment=1,
                                          spaceAfter=20)

        self.style_section = ParagraphStyle("Secao", fontName="Courier",
                                            fontSize=12, alignment=1,
                                            spaceAfter=10)

        self.style_small = ParagraphStyle("Pequeno", fontName="Courier",
                                          fontSize=9, alignment=1,
                                          spaceAfter=10)

    @staticmethod
    def fig_to_img(fig, w=None, h=None):
        # retorna um figure de um plt
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        return Image(buf, width=w, height=h)

    @staticmethod
    def latex_to_img(eq, w=None, h=None):
        # converte eq latex pra um plt
        fig = plt.figure(figsize=(3, 1))
        fig.subplots_adjust(0, 0, 1, 1)
        plt.text(0.5, 0.5, f"${eq}$", ha="center", va="center", fontsize=20)
        plt.axis("off")
        return RelatorioCalibracao.fig_to_img(fig, w, h)

    @staticmethod
    def polyfit_to_latex(coeffs, var="x", unidade=None):
        # faz a eq da curva de calibração estática
        termos = []
        grau = len(coeffs) - 1

        for i, c in enumerate(coeffs):
            if abs(c) < 1e-10:
                continue
            pot = grau - i
            termo = f"{abs(c):.4f}"
            if pot > 1:
                termo += f"{var}^{{{pot}}}"
            elif pot == 1:
                termo += var
            sinal = "+" if c >= 0 else "-"
            termos.append((sinal, termo))

        if not termos:
            eq = "y = 0"
        else:
            sinal1, t1 = termos[0]
            eq = f"y = {'-' if sinal1 == '-' else ''}{t1}"
            for s, t in termos[1:]:
                eq += f" {s} {t}"

        if unidade:
            eq += f"\\ \\left[\\frac{{V}}{{{unidade}}}\\right]"

        return eq

    @staticmethod
    def tf_to_latex(ordem, *p):
        # faz a equação latex
        if ordem == 0:
            return fr"G(s) = {p[0]:.4f}"
        if ordem == 1:
            return fr"G(s) = \frac{{{p[0]:.4f}}}{{{p[1]:.4f}s + 1}}"
        if ordem == 2:
            K, tau_d, xi, wn = p
            num = fr"{K:.4f} e^{{-{tau_d:.4f}s}}"
            den = fr"s^2 + {2 * xi * wn:.4f}s + {wn ** 2:.4f}"
            return fr"G(s) = \frac{{{num}}}{{{den}}}"

    def add_header(self):
        # cabeçalho
        self.story.append(Paragraph("Relatório de calibração", self.style_title))

        tabela = Table(
            [
                [f"Sensor: {self.sensor}"],
                [f"Responsável: {self.responsavel}"],
                [f"Data e hora: {datetime.now().strftime('%d/%m/%Y -- %H:%M')}"]
            ],
            colWidths=[450]
        )

        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        self.story.append(tabela)
        self.story.append(Spacer(1, 20))

    def add_static(self):
        # parte do estático
        self.story.append(Paragraph("Características estáticas", self.style_section))

        # curva calibração
        img = self.fig_to_img(self.sta.fig_ccs, 400, 200)
        img.hAlign = "CENTER"
        self.story.append(img)

        eq = self.polyfit_to_latex(self.sta.curva_calib_estatica)
        self.story.append(self.latex_to_img(eq, 120 + (self.sta.ordem_ajuste - 1) * 20, 40))
        self.story.append(Spacer(1, 20))

        # sensibilidade
        img = self.fig_to_img(self.sta.fig_csens, 400, 200)
        img.hAlign = "CENTER"
        self.story.append(img)

        eq = self.polyfit_to_latex(self.sta.sensibilidade, unidade=self.unidade)
        self.story.append(self.latex_to_img(eq, 120 + (self.sta.ordem_ajuste - 1) * 20, 40))

        self.story.append(PageBreak())

        # tabela resumo
        linhas = [
            ["Erro Aleatório - EA", f"{self.sta.erro_aleatorio_global:.2f} [{self.unidade}]"],
            ["Repetibilidade (%)", f"{self.sta.repetibilidade_max:.2f}%"],
            ["Erro de linearidade - L (%)" if self.sta.ordem_ajuste == 1 else "Erro de conformidade - C (%)",
             f"{self.sta.erro_ajuste:.2f}%"],
            ["Erro de histerese - H (%)", f"{self.sta.erro_histerese:.2f}%"],
            ["Fundo de escala - FES", f"{self.sta.points[-1]:.2f} [{self.unidade}]"]
        ]

        tabela = Table(linhas, colWidths=[9 * cm, 4 * cm])
        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        self.story.append(tabela)
        self.story.append(Spacer(1, 20))

        img = self.fig_to_img(self.sta.fig_hist, 400, 200)
        img.hAlign = "CENTER"
        self.story.append(img)

        self.story.append(PageBreak())

    def add_dynamic(self):
        # parte do dinâmico
        cfg = self.CONFIG[self.dyn.TIPO_AJUSTE]

        self.story.append(Paragraph(cfg["titulo"], self.style_small))

        eq_tf = self.tf_to_latex(*cfg["latex"](self.dyn))
        self.story.append(self.latex_to_img(eq_tf, 150, 50))
        self.story.append(Spacer(1, 10))

        img = self.fig_to_img(self.dyn.fig_dyn, 400, 200)
        img.hAlign = "CENTER"
        self.story.append(img)

        self.story.append(Paragraph("Características dinâmicas", self.style_section))
        self.story.append(Spacer(1, 10))

        tabela = Table(cfg["linhas"](self.dyn), colWidths=[9 * cm, 4 * cm])
        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.story.append(tabela)

    @staticmethod
    def footer(canvas, doc):
        # rodapé
        canvas.setFont("Courier", 10)
        canvas.setLineWidth(1)
        canvas.line(40, 60, A4[0] - 40, 60)
        canvas.drawString(40, 45, "Relatório gerado no CalibraPy")
        canvas.drawRightString(A4[0] - 40, 45, f"{doc.page}")

    def build(self):
        doc = SimpleDocTemplate(
            self.pdf_file,
            pagesize=A4,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )

        self.add_header()
        self.add_static()
        self.add_dynamic()

        doc.build(self.story,
                  onFirstPage=self.footer,
                  onLaterPages=self.footer)


rel = RelatorioCalibracao(pdf_file="relatorio_calibracao.pdf",
                          sensor="Termopar XYZ-200",
                          responsavel="Júlio César",
                          sta=car_est,
                          dyn=modelo_crit,
                          unidade="cm")

rel.build()
