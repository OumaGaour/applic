from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Line
import pdfplumber
import re


def generate_certificate(output_path, uid, candidate_name, course_name, notes, grad, org_name, birthday, institute_logo_path):
    # Create a PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    # Create a list to hold the elements of the PDF
    elements = []

    # Add institute logo and institute name
    if institute_logo_path:
        logo = Image(institute_logo_path, width=150, height=150)
        logo.hAlign = 'CENTER'
        elements.append(logo)

        institute_style = ParagraphStyle(
            "InstituteStyle",
            parent=getSampleStyleSheet()["Title"],
            fontName="Times-Roman",
            fontSize=16,
            spaceAfter=20,
        )
        institute = Paragraph(org_name, institute_style)
        elements.append(institute)

    # Add border
    elements.append(Spacer(1, 12))

    # Add title
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        spaceAfter=20,
    )
    title1 = Paragraph("Certificate of Completion", title_style)
    elements.append(title1)

    # Improve recipient information formatting
    recipient_style = ParagraphStyle(
        "RecipientStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=14,
        spaceAfter=6,
        leading=18,
    )

    recipient_text = f"Le président de l'Université Ibn Zohr atteste que <br/>\
        Étudiant(e) <font color='black'><b>{candidate_name}</b></font><br/>\
        <br/>\
        Code national de l'étudiant <font color='black'><b>{uid}</b></font><br/>\
        <br/>\
        a obtenu le DIPLÔME DE LA LICENCE PROFESSIONNELLE sur <font color='black'><b>{course_name}</b></font><br/>\
        <br/>\
        avec la note <font color='black'>{notes}</font><br/> et avec la monsion <font color='black'><b>{grad}</b></font><br/>\
        <br/>\
        offert par {org_name} le <font color='black'><b>{birthday}</b></font>"

    recipient = Paragraph(recipient_text, recipient_style)
    elements.append(recipient)

    # Build the PDF document
    doc.build(elements)

    print(f"Certificate generated and saved at: {output_path}")



import pdfplumber
import re

def extract_certificate(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        regex_patterns = {
            "org_name": r"^([^:]+)",
            "candidate_name": r"Étudiant\(e\)\s+(.+)",
            "uid": r"Code\s+national\s+de\s+l'étudiant\s+([\w\s]+)",
            "course_name": r"DIPLÔME\s+DE\s+LA\s+LICENCE\s+PROFESSIONNELLE\s+sur\s+([\w\s]+)",
            "notes": r"avec\s+la\s+note\s+(\w+)",
            "grad": r"avec\s+la\s+monsion\s+(\w+)",
            "birthday": r"offert\s+par\s+.+\s+le\s+(\d{1,2}/\d{1,2}/\d{4})"
        }

        certificate_info = {}
        for field, pattern in regex_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                certificate_info[field] = match.group(1).strip()
            else:
                raise ValueError(f"Failed to extract {field} from the certificate")

        return (
            certificate_info["uid"],
            certificate_info["candidate_name"],
            certificate_info["course_name"],
            certificate_info["notes"],
            certificate_info["grad"],
            certificate_info["org_name"],
            certificate_info["birthday"]
        )
    except Exception as e:
        raise ValueError("Error extracting certificate information") from e
