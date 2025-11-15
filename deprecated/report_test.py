from typing import Union

import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import shutil
import re
import io

from report_codes.static import car_est, CaracteristicasEstaticas
from report_codes.id_0_ordem import OrdemZero, modelo_0ordem
from report_codes.id_1_ordem import PrimeiraOrdem, modelo_1ordem
from report_codes.id_2_ordem_subam import SundaresanSubamortecido, modelo_sub
from report_codes.id_2_ordem_sobream import SundaresanSobreamortecido, modelo_sob

import matplotlib.pyplot as plt


def fig_to_rl_image(fig, width=None, height=None):
    """Converte uma figura matplotlib em um objeto Image do reportlab."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    return Image(buf, width=width, height=height)


def latex_to_rl_image(eq, width=None, height=None):
    fig = plt.figure(figsize=(3, 1))
    fig.subplots_adjust(0, 0, 1, 1)
    plt.text(0.5, 0.5, f"${eq}$", ha="center", va="center", fontsize=20)
    plt.axis("off")
    return fig_to_rl_image(fig, width=width, height=height)


def polyfit_to_latex(coeffs, var="x", unidade=None):
    termos = []
    grau = len(coeffs) - 1

    for i, c in enumerate(coeffs):
        pot = grau - i
        if abs(c) < 1e-10:
            continue

        sinal = "+" if c >= 0 else "-"
        c_abs = abs(c)

        if pot > 1:
            termo = f"{c_abs:.4f}{var}^{{{pot}}}"
        elif pot == 1:
            termo = f"{c_abs:.4f}{var}"
        else:
            termo = f"{c_abs:.4f}"

        termos.append((sinal, termo))

    if not termos:
        equacao = "y = 0"
    else:
        sinal1, termo1 = termos[0]
        equacao = f"y = {'-' if sinal1 == '-' else ''}{termo1}"
        for sinal, termo in termos[1:]:
            equacao += f" {sinal} {termo}"

    if unidade is not None:
        equacao += f"\\ \\left[\\frac{{V}}{{{unidade}}}\\right]"

    return equacao


def tf_to_latex(ordem, *params):
    if ordem == 0:
        K = params[0]
        return fr"G(s) = {K:.4f}"

    elif ordem == 1:
        K, tau = params
        return fr"G(s) = \frac{{{K:.4f}}}{{{tau:.4f}s + 1}}"

    elif ordem == 2:
        K, tau_d, xi, wn = params
        num = fr"{K:.4f} e^{{-{tau_d:.4f}s}}"
        den = fr"{wn ** 2:.4f} + {2 * xi * wn:.4f}s + s^2"
        return fr"G(s) = \frac{{{num}}}{{{den}}}"


def gerar_relatorio_calibracao(
        arquivo_pdf: str,
        sensor_name: str,
        resp_name: str,
        class_sta: CaracteristicasEstaticas,
        class_dyn: Union[OrdemZero, PrimeiraOrdem, SundaresanSobreamortecido, SundaresanSubamortecido],
        unidade: str
):
    doc = SimpleDocTemplate(
        arquivo_pdf,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    # -------------------------------------------------------
    # CABEÇALHO
    # -------------------------------------------------------

    estilo_titulo = ParagraphStyle(
        name="Titulo",
        fontName="Courier",
        fontSize=16,
        alignment=1,  # 0=esq,1=centro,2=dir
        spaceAfter=20
    )

    story.append(Paragraph("Relatório de calibração", estilo_titulo))
    story.append(Spacer(1, 20))

    dados_tabela = [
        [f"Sensor: {sensor_name}"],
        [f"Responsável: {resp_name}"],
        [f"Data e hora: {datetime.now().strftime('%d/%m/%Y -- %H:%M')}"]
    ]

    tabela = Table(
        dados_tabela,
        colWidths=[450]
    )

    tabela.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))

    estilo_secao = ParagraphStyle(
        name="Secao",
        fontName="Courier",
        fontSize=9,
        alignment=1,
        spaceAfter=10,
    )

    story.append(tabela)

    story.append(Spacer(1, 20))  # espaço cabeçalho até primeiro tópico

    # -------------------------------------------------------
    # CARAC ESTÁTICAS
    # -------------------------------------------------------

    estilo_titulos_sub = ParagraphStyle(
        name="Secao",
        fontName="Courier",
        fontSize=12,
        alignment=1,
        spaceAfter=10,
    )

    story.append(Paragraph("Características estáticas", estilo_titulos_sub))

    img_ccs = fig_to_rl_image(class_sta.fig_ccs, width=400, height=200)  # imagem curva de calibração estática
    img_ccs.hAlign = "CENTER"
    story.append(img_ccs)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Equação da curva de calibração estática:", estilo_secao))

    eq_ccs = polyfit_to_latex(class_sta.curva_calib_estatica)

    img_eq_ccs = latex_to_rl_image(eq_ccs, width=120 + (class_sta.ordem_ajuste - 1) * 20, height=40)

    img_eq_ccs.hAlign = "CENTER"
    story.append(img_eq_ccs)

    story.append(Spacer(1, 20))

    img_csens = fig_to_rl_image(class_sta.fig_csens, width=400, height=200)  # imagem curva de sensibilidade
    img_csens.hAlign = "CENTER"
    story.append(img_csens)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Equação da curva de sensibilidade:", estilo_secao))

    eq_csens = polyfit_to_latex(class_sta.sensibilidade, unidade=unidade)

    img_eq_csens = latex_to_rl_image(eq_csens, width=120 + (class_sta.ordem_ajuste - 1) * 20, height=40)

    img_eq_csens.hAlign = "CENTER"
    story.append(img_eq_csens)

    story.append(PageBreak())

    # Linhas da tabela
    # Monta as linhas
    linhas = [
        ["Erro Aleatório - EA", f"{class_sta.erro_aleatorio_global:.2f} [{unidade}]"],
        ["Repetibilidade (%)", f"{class_sta.repetibilidade_max:.2f}%"],
    ]

    if class_sta.ordem_ajuste == 1:
        linhas.append(["Erro de linearidade - L (%)", f"{class_sta.erro_ajuste:.2f}%"])
    else:
        linhas.append(["Erro de conformidade - C (%)", f"{class_sta.erro_ajuste:.2f}%"])

    linhas.append(["Erro de histerese - H (%)", f"{class_sta.erro_histerese:.2f}%"])
    linhas.append(["Fundo de escala - FES", f"{class_sta.points[-1]:.2f} [{unidade}]"])

    # Cria a tabela
    tabela = Table(
        linhas,
        colWidths=[9 * cm, 4 * cm],  # ajuste se quiser
    )

    # Aplica o estilo solicitado
    tabela.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(tabela)

    story.append(Spacer(1, 20))
    img_hist = fig_to_rl_image(class_sta.fig_hist, width=400, height=200)  # imagem histerese
    img_hist.hAlign = "CENTER"
    story.append(img_hist)

    story.append(PageBreak())

    # -------------------------------------------------------
    # CARAC DINÂMICAS
    # -------------------------------------------------------

    story.append(Paragraph("Características dinâmicas", estilo_titulos_sub))

    # tf_to_latex

    if class_dyn.TIPO_AJUSTE == "0a_ordem":
        story.append(Paragraph("Modelo de ordem 0:", estilo_secao))

        eq_tf = tf_to_latex(0, class_dyn.K)
        img_tf = latex_to_rl_image(eq_tf, width=120, height=40)
        story.append(img_tf)

        story.append(Spacer(1, 10))

        img_dyn = fig_to_rl_image(class_dyn.fig_dyn, width=400, height=200)  # imagem dinamico
        img_dyn.hAlign = "CENTER"
        story.append(img_dyn)

        linhas_dyn = [["Ganho", f"{class_dyn.K:.4f}"]]

    elif class_dyn.TIPO_AJUSTE == "1a_ordem":
        story.append(Paragraph("Modelo de primeira ordem:", estilo_secao))

        eq_tf = tf_to_latex(1, class_dyn.K, class_dyn.tau, )
        img_tf = latex_to_rl_image(eq_tf, width=120, height=40)
        story.append(img_tf)

        story.append(Spacer(1, 10))

        img_dyn = fig_to_rl_image(class_dyn.fig_dyn, width=400, height=200)  # imagem dinamico
        img_dyn.hAlign = "CENTER"
        story.append(img_dyn)

        linhas_dyn = [
            ["Ganho", f"{class_dyn.K:.4f}"],
            ["Constante de tempo", f"{class_dyn.tau:.4f}"]
        ]

    elif class_dyn.TIPO_AJUSTE == "2a_ordem_subamortecido":
        story.append(Paragraph("Modelo de segunda ordem subamortecido:", estilo_secao))

        eq_tf = tf_to_latex(2, class_dyn.K, class_dyn.tau_d, class_dyn.xi, class_dyn.wn)
        img_tf = latex_to_rl_image(eq_tf, width=120, height=40)
        story.append(img_tf)

        story.append(Spacer(1, 10))

        img_dyn = fig_to_rl_image(class_dyn.fig_dyn, width=400, height=200)  # imagem dinamico
        img_dyn.hAlign = "CENTER"
        story.append(img_dyn)

        linhas_dyn = [
            ["Ganho", f"{class_dyn.K:.4f}"],
            ["Atraso puro de tempo", f"{class_dyn.tau_d:.4f}"],
            ["Coeficiente de amortecimento", f"{class_dyn.xi:.4f}"],
            ["Frequência natural", f"{class_dyn.wn:.4f}"],
        ]

    story.append(Spacer(1, 10))

    story.append(Paragraph("Parâmetros do modelo dinâmico", estilo_secao))

    tabela_dyn = Table(
        linhas_dyn,
        colWidths=[9 * cm, 4 * cm],  # ajuste se quiser
    )
    tabela_dyn.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(tabela_dyn)

    def rodape(canvas, doc):
        canvas.setFont("Courier", 10)

        # Linha horizontal
        canvas.setLineWidth(1)
        canvas.line(
            40, 60,  # x1, y1
            A4[0] - 40, 60  # x2, y2
        )

        # Texto à esquerda
        canvas.drawString(40, 45, "Relatório gerado no CalibraPy")

        # Texto à direita
        canvas.drawRightString(A4[0] - 40, 45, f"{doc.page}")

    doc.build(story, onLaterPages=rodape, onFirstPage=rodape)


if __name__ == "__main__":
    gerar_relatorio_calibracao(
        arquivo_pdf="relatorio_calibracao.pdf",
        sensor_name="Termopar XYZ-200",
        resp_name="Júlio César",
        class_sta=car_est,
        class_dyn=modelo_sub,
        unidade="pos"
    )
