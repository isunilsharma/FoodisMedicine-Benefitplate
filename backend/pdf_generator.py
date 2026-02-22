"""Generate PDF checklists using ReportLab"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from typing import List, Dict, Any
from io import BytesIO
from datetime import datetime

from models import ProgramMatch

def generate_checklist_pdf(
    user_name: str,
    zip_code: str,
    county: str,
    state: str,
    programs: List[ProgramMatch]
) -> BytesIO:
    """Generate a PDF checklist for matched programs"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          topMargin=0.5*inch, bottomMargin=0.5*inch,
                          leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=8,
        spaceBefore=16
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )
    
    # Title
    story.append(Paragraph("Your Food & Nutrition Benefits Checklist", title_style))
    story.append(Paragraph(
        f"Prepared for {user_name} | {county}, {state} (ZIP: {zip_code})",
        subtitle_style
    ))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')}",
        subtitle_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=12,
        italic=True
    )
    story.append(Paragraph(
        "<b>Disclaimer:</b> This tool provides informational guidance and is not a government agency. "
        "Eligibility varies by program and may require verification by the program provider. "
        "We do not provide medical advice.",
        disclaimer_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Programs
    for idx, program in enumerate(programs, 1):
        # Program header
        story.append(Paragraph(f"<b>{idx}. {program.program_name}</b>", heading_style))
        
        # Program type and status
        benefit_type_label = program.benefit_type.value.replace('_', ' ').title()
        status_label = program.eligibility_status.value.replace('_', ' ').title()
        story.append(Paragraph(
            f"<b>Type:</b> {benefit_type_label} | <b>Status:</b> {status_label}",
            body_style
        ))
        
        # Why you match
        if program.why_you_match:
            story.append(Paragraph(
                f"<b>Why you may qualify:</b> {program.why_you_match}",
                body_style
            ))
        
        # Required documents
        if program.document_checklist and "required" in program.document_checklist:
            story.append(Paragraph("<b>Required Documents:</b>", body_style))
            for doc in program.document_checklist["required"]:
                story.append(Paragraph(f"☐ {doc}", body_style))
        
        # Optional documents
        if program.document_checklist and "optional" in program.document_checklist:
            if program.document_checklist["optional"]:
                story.append(Paragraph("<b>Optional Documents:</b>", body_style))
                for doc in program.document_checklist["optional"]:
                    story.append(Paragraph(f"☐ {doc}", body_style))
        
        # How to apply
        story.append(Paragraph("<b>How to Apply:</b>", body_style))
        if program.how_to_apply_url:
            story.append(Paragraph(f"Website: {program.how_to_apply_url}", body_style))
        if program.contact_phone:
            story.append(Paragraph(f"Phone: {program.contact_phone}", body_style))
        
        # Spacer between programs
        if idx < len(programs):
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("_" * 80, body_style))
            story.append(Spacer(1, 0.2*inch))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#9CA3AF'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "For questions about specific programs, please contact the program directly using the information above.",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
