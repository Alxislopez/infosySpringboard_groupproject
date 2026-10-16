# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alxislopez

import io
from docx import Document


def generate_pdf_report(project_data, risk_data, swot_data, agent_result, market_data):
    """Generate a PDF report using ReportLab which fully supports Unicode."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                 fontSize=18, spaceAfter=12, alignment=TA_CENTER,
                                 textColor=colors.HexColor('#CC0044'))
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, spaceAfter=6,
                        textColor=colors.HexColor('#111111'))
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, spaceAfter=4,
                        textColor=colors.HexColor('#333333'))
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, spaceAfter=4, leading=14)

    story = []

    # Title
    story.append(Paragraph("Failure Prediction AI – Comprehensive Assessment Report", title_style))
    story.append(Spacer(1, 6*mm))

    # Project Info
    story.append(Paragraph("Project Overview", h1))
    story.append(Paragraph(f"<b>Startup:</b> {project_data.get('startup_name', 'N/A')}", body))
    story.append(Paragraph(f"<b>Industry:</b> {project_data.get('industry', 'N/A')}", body))
    story.append(Paragraph(f"<b>Budget:</b> ${project_data.get('budget', 0):,}", body))
    story.append(Paragraph(f"<b>Description:</b> {project_data.get('description', 'N/A')}", body))
    story.append(Spacer(1, 6*mm))

    # Risk Assessment
    story.append(Paragraph("Risk Assessment", h1))
    risk_table_data = [["Risk Category", "Score"]]
    for k, v in risk_data.items():
        risk_table_data.append([k, f"{v}/5"])
    t = Table(risk_table_data, colWidths=[110*mm, 30*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CC0044')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f9f9f9'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 6*mm))

    # Market Analysis
    story.append(Paragraph("Market Analysis", h1))
    story.append(Paragraph(f"• Total Addressable Market (TAM): <b>${market_data.get('tam', 0)}B</b>", body))
    story.append(Paragraph(f"• Serviceable Addressable Market (SAM): <b>${market_data.get('sam', 0)}M</b>", body))
    story.append(Paragraph(f"• Serviceable Obtainable Market (SOM): <b>${market_data.get('som', 0)}M</b>", body))
    story.append(Spacer(1, 6*mm))

    # AI Recommendations
    if agent_result:
        story.append(Paragraph("Strategic AI Recommendations", h1))
        for rec in agent_result.get("recommendations", [])[:4]:
            priority = rec.get('priority', 'Medium')
            colour = '#b91c1c' if 'critical' in priority.lower() else '#c2410c' if 'high' in priority.lower() else '#15803d'
            story.append(Paragraph(
                f"<b>{rec.get('title', '')}</b> "
                f"<font color='{colour}'>[{priority.upper()}]</font>",
                h2))
            story.append(Paragraph(f"<b>Category:</b> {rec.get('category', '')}", body))
            story.append(Paragraph(rec.get('description', ''), body))
            story.append(Spacer(1, 3*mm))

    doc.build(story)
    return buf.getvalue()


def generate_docx_report(project_data, risk_data, swot_data, agent_result, market_data):
    doc = Document()
    doc.add_heading('Failure Prediction AI - Comprehensive Assessment', 0)

    doc.add_heading(f"Startup: {project_data.get('startup_name', 'N/A')}", level=1)
    doc.add_paragraph(f"Industry: {project_data.get('industry', 'N/A')} | Budget: ${project_data.get('budget', 0):,}")
    doc.add_paragraph(f"Description: {project_data.get('description', 'N/A')}")

    doc.add_heading('Risk Assessment', level=2)
    for k, v in risk_data.items():
        doc.add_paragraph(f"{k}: {v}/5", style='List Bullet')

    doc.add_heading('Market Analysis', level=2)
    doc.add_paragraph(f"TAM: ${market_data.get('tam', 0)}B", style='List Bullet')
    doc.add_paragraph(f"SAM: ${market_data.get('sam', 0)}M", style='List Bullet')
    doc.add_paragraph(f"SOM: ${market_data.get('som', 0)}M", style='List Bullet')

    if agent_result:
        doc.add_heading('Strategic AI Recommendations', level=2)
        for rec in agent_result.get("recommendations", [])[:4]:
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(f"{rec.get('title')} ({rec.get('priority')}): ").bold = True
            p.add_run(f"{rec.get('description')}")

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()
