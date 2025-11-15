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

from calcs import car_est
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


def polyfit_to_latex(coeffs, var="x"):
    termos = []
    grau = len(coeffs) - 1

    for i, c in enumerate(coeffs):
        pot = grau - i
        if abs(c) < 1e-10:
            continue

        # Determinar sinal
        sinal = "+" if c >= 0 else "-"

        # Valor absoluto para não duplicar o sinal
        c_abs = abs(c)

        # Formatação do termo
        if pot > 1:
            termo = f"{c_abs:.4f}{var}^{{{pot}}}"
        elif pot == 1:
            termo = f"{c_abs:.4f}{var}"
        else:
            termo = f"{c_abs:.4f}"

        termos.append((sinal, termo))

    # Montar string final
    if not termos:
        return "y = 0"

    # Primeiro termo não deve ter "+" na frente
    sinal1, termo1 = termos[0]
    equacao = f"y = {'-' if sinal1 == '-' else ''}{termo1}"

    # Restante dos termos
    for sinal, termo in termos[1:]:
        equacao += f" {sinal} {termo}"

    return equacao


def gerar_relatorio_calibracao(
        arquivo_pdf: str,
        sensor_name: str,
        resp_name: str,
        figure_ccs,
        pol_eq_ccs,
        figure_csens,
        pol_eq_csens,
        ordem_aj,
        erro_aj,
        erro_hist,
        repet,
        erro_al,
        figure_hist
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

    img_ccs = fig_to_rl_image(figure_ccs, width=400, height=200)  # imagem curva de calibração estática
    img_ccs.hAlign = "CENTER"
    story.append(img_ccs)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Equação da curva de calibração estática:", estilo_secao))

    eq_ccs = polyfit_to_latex(pol_eq_ccs)

    img_eq_ccs = latex_to_rl_image(eq_ccs, width=120, height=40)

    img_eq_ccs.hAlign = "CENTER"
    story.append(img_eq_ccs)

    story.append(Spacer(1, 20))

    img_csens = fig_to_rl_image(figure_csens, width=400, height=200)  # imagem curva de sensibilidade
    img_csens.hAlign = "CENTER"
    story.append(img_csens)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Equação da curva de sensibilidade:", estilo_secao))

    eq_csens = polyfit_to_latex(pol_eq_csens)

    img_eq_csens = latex_to_rl_image(eq_csens, width=120, height=40)

    img_eq_csens.hAlign = "CENTER"
    story.append(img_eq_csens)

    story.append(PageBreak())

    # story.append(Paragraph(f"Repetibilidade = {repet:.2f}%", estilo_secao))
    #
    # if ordem_aj == 1:
    #     story.append(Paragraph(f"Erro de linearidade L(%) = {erro_aj:.2f}%", estilo_secao))
    # else:
    #     story.append(Paragraph(f"Erro de conformidade C(%) = {erro_aj:.2f}%", estilo_secao))
    #
    # story.append(Paragraph(f"Erro de histerese H(%) = {erro_hist:.2f}%", estilo_secao))

    # Linhas da tabela
    # Monta as linhas
    linhas = [
        ["Repetibilidade (%)", f"{repet:.2f}%"],
        ["Erro Aleatório EA", f"{erro_al:.2f}"]
    ]

    if ordem_aj == 1:
        linhas.append(["Erro de linearidade L (%)", f"{erro_aj:.2f}%"])
    else:
        linhas.append(["Erro de conformidade C (%)", f"{erro_aj:.2f}%"])

    linhas.append(["Erro de histerese H (%)", f"{erro_hist:.2f}%"])

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
    img_hist = fig_to_rl_image(figure_hist, width=400, height=200)  # imagem histerese
    img_hist.hAlign = "CENTER"
    story.append(img_hist)

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
        pol_eq_ccs=car_est.curva_calib_estatica,
        figure_ccs=car_est.fig_ccs,
        figure_csens=car_est.fig_csens,
        pol_eq_csens=car_est.sensibilidade,
        ordem_aj=car_est.ordem_ajuste,
        erro_aj=car_est.erro_ajuste,
        erro_hist=car_est.erro_histerese,
        repet=car_est.repetibilidade_max,
        erro_al=car_est.erro_aleatorio_global,
        figure_hist=car_est.fig_hist
    )
