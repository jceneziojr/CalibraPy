import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import shutil
import re
import io

from calcs import fig_ccs


def fig_to_rl_image(fig, width=None, height=None):
    """Converte uma figura matplotlib em um objeto Image do reportlab."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return Image(buf, width=width, height=height)


def gerar_relatorio_calibracao(
        arquivo_pdf: str,
        sensor_name: str,
        resp_name: str,
        figure_ccs
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

    story.append(tabela)

    story.append(Spacer(1, 100))  # espaço cabeçalho até primeiro tópico

    img_ccs = fig_to_rl_image(figure_ccs, width=500, height=250)  # imagem curva de calibração estática
    story.append(img_ccs)

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
        fig_ccs=fig_ccs
    )
