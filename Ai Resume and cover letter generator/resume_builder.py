# resume_builder.py

import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# --- Color Definitions ---
PRIMARY_COLOR = HexColor("#2c3e50")
SECONDARY_COLOR = HexColor("#3498db")
TEXT_COLOR = HexColor("#34495e")
LIGHT_GRAY = HexColor("#ecf0f1")

def generate_pdf(data, template_name, profile_photo_path=None):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    if template_name == 'modern':
        draw_modern_template(c, width, height, data, profile_photo_path)
    elif template_name == 'creative':
        draw_creative_template(c, width, height, data, profile_photo_path)
    else:
        draw_classic_template(c, width, height, data, profile_photo_path)

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def draw_section(c, x, y_start, title, content_list, font_name="Helvetica-Bold", font_size=12, color=PRIMARY_COLOR):
    c.setFillColor(color)
    c.setFont(font_name, font_size)
    c.drawString(x, y_start, title.upper())
    y = y_start - 20
    
    c.setFillColor(TEXT_COLOR)
    
    item_y = y
    for item in content_list:
        text = c.beginText()
        text.setTextOrigin(x + 10, item_y)
        text.setFont("Helvetica", 10)
        
        lines = item.split('\n')
        for line in lines:
            if line.strip().startswith('**') and line.strip().endswith('**'):
                text.setFont("Helvetica-Bold", 10)
                text.textLine(line.replace('**', ''))
                text.setFont("Helvetica", 10) 
            else:
                text.textLine(line)
        
        c.drawText(text)
        item_y -= (len(lines) * 14) + 6
        
    return item_y

def draw_classic_template(c, width, height, data, profile_photo_path):
    c.setFont("Times-Bold", 24)
    c.drawCentredString(width / 2.0, height - 72, data['name'])
    c.setFont("Times-Roman", 11)
    c.drawCentredString(width / 2.0, height - 90, data['contact_info'])
    
    y_position = height - 130
    
    y_position = draw_section(c, 72, y_position, "Professional Summary", [data['summary']], font_name="Times-Bold")
    y_position = draw_section(c, 72, y_position, "Work Experience",
                              [f"**{exp['job_title']} at {exp['company']} ({exp['dates']})**\n" +
                               "\n".join([f"• {resp}" for resp in exp['responsibilities']])
                               for exp in data['experience']], font_name="Times-Bold")
    y_position = draw_section(c, 72, y_position, "Education",
                              [f"**{edu['degree']}**, {edu['institution']} ({edu['years']})"
                               for edu in data['education']], font_name="Times-Bold")
    if data.get('projects'):
        y_position = draw_section(c, 72, y_position, "Projects",
                                  [f"**{proj['title']}**\n  {proj['description']}"
                                   for proj in data['projects']], font_name="Times-Bold")
    y_position = draw_section(c, 72, y_position, "Skills", [", ".join(data['skills'])], font_name="Times-Bold")
    
    # Logic for certifications and achievements is here
    if data.get('certifications'):
        y_position = draw_section(c, 72, y_position, "Certifications", [f"• {cert}" for cert in data['certifications']], font_name="Times-Bold")
    if data.get('achievements'):
        y_position = draw_section(c, 72, y_position, "Achievements", [f"• {ach}" for ach in data['achievements']], font_name="Times-Bold")

# ... (draw_modern_template and draw_creative_template should also contain the checks for certifications and achievements) ...

def draw_modern_template(c, width, height, data, profile_photo_path):
    # ... (header and sidebar code) ...
    main_x = width * 0.35
    c.setFillColor(TEXT_COLOR)
    y_position = height - 72
    y_position = draw_section(c, main_x, y_position, "Professional Summary", [data['summary']])
    y_position = draw_section(c, main_x, y_position, "Work Experience",
                              [f"**{exp['job_title']} at {exp['company']} ({exp['dates']})**\n" +
                               "\n".join([f"• {resp}" for resp in exp['responsibilities']])
                               for exp in data['experience']])
    # ... (other sections) ...
    if data.get('certifications'):
        y_position = draw_section(c, main_x, y_position, "Certifications", [f"• {cert}" for cert in data['certifications']])
    if data.get('achievements'):
        y_position = draw_section(c, main_x, y_position, "Achievements", [f"• {ach}" for ach in data['achievements']])


def generate_cover_letter_pdf(data):
    # ... (this function is unchanged and correct)
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    story = []
    contact_info_parts = data['contactInfo'].get('contact_info', '').split(',')
    name = data['contactInfo'].get('name', '')
    ptext = f"<b>{name}</b>"
    story.append(Paragraph(ptext, styles["Normal"]))
    for part in contact_info_parts:
        story.append(Paragraph(part.strip(), styles["Normal"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), styles["Normal"]))
    story.append(Spacer(1, 0.25 * inch))
    letter_text = data['letterText'].replace('\n', '<br/>')
    story.append(Paragraph(letter_text, styles["Normal"]))
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer