import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


def get_user_input():
    """Collects user input from the console."""
    name = input("Enter your full name: ")

    email = input("Enter your email (must contain '@'): ")
    while "@" not in email:
        print("Invalid email. Please enter a valid email with '@'.")
        email = input("Enter your email (must contain '@'): ")

    phone = input("Enter your phone number: ")
    address = input("Enter your address: ")
    degree = input("Enter your degree (e.g., B.Tech, M.Sc.): ")
    specialization = input("Enter your specialization (e.g., Computer Science): ")
    university = input("Enter your university name: ")
    graduation_year = input("Enter your graduation year: ")
    skills = input("Enter your skills (separate by commas): ")
    linkedin = input("Enter your LinkedIn profile link: ")
    github = input("Enter your GitHub profile link: ")
    projects = input("Enter your projects (separate by commas): ")
    experiences = input(
        "Enter your work experiences (separate by semicolons, format: Job Title at Company - Duration): "
    )
    certifications = input("Enter your certifications (separate by commas): ")

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "degree": degree,
        "specialization": specialization,
        "university": university,
        "graduation_year": graduation_year,
        "skills": skills,
        "linkedin": linkedin,
        "github": github,
        "projects": projects,
        "experiences": experiences,
        "certifications": certifications,
    }


def generate_pdf(user_data):
    """Generates a well-structured resume PDF."""
    folder_path = r"C:\Users\s.paranidharan\OneDrive - Perficient, Inc\poc 4"
    pdf_filename = os.path.join(folder_path, "advanced_resume.pdf")

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    # Define Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        spaceAfter=10,
        textColor=colors.HexColor("#2E4053"),
        underline=True,
    )
    header_style = ParagraphStyle(
        "Header",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor("#1F618D"),
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=12,
        spaceAfter=4,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["BodyText"],
        fontSize=10,
        leading=12,
        leftIndent=14,
        spaceAfter=4,
        bulletText="✓ ",
        bulletFontName="Times-Bold",
    )

    # Resume Content
    content = []

    # Header Section (Name and Contact Information)
    content.append(Paragraph(user_data["name"], title_style))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1F618D")))

    contact_info = f"{user_data['address']} | {user_data['phone']} | {user_data['email']}<br/><br/>"
    contact_info += f"LinkedIn: <a href='{user_data['linkedin']}' color='blue'>{user_data['linkedin']}</a><br/>"
    contact_info += f"GitHub: <a href='{user_data['github']}' color='blue'>{user_data['github']}</a>"
    content.append(Paragraph(contact_info, body_style))
    content.append(Spacer(1, 12))

    # Education Section
    content.append(Paragraph("Education", header_style))
    education_details = f"{user_data['degree']} in {user_data['specialization']}<br/>{user_data['university']}, Class of {user_data['graduation_year']}"
    content.append(Paragraph(education_details, body_style))
    content.append(Spacer(1, 12))
    content.append(HRFlowable(width="80%", thickness=1, color=colors.HexColor("#566573")))

    # Skills Section
    content.append(Paragraph("Skills", header_style))
    skills_list = user_data["skills"].split(",")
    for skill in skills_list:
        content.append(Paragraph(skill.strip(), bullet_style))
    content.append(Spacer(1, 12))

    # Experience Section
    content.append(Paragraph("Experience", header_style))
    experiences_list = user_data["experiences"].split(";")
    for experience in experiences_list:
        content.append(Paragraph(experience.strip(), bullet_style))
    content.append(Spacer(1, 12))

    # Projects Section
    content.append(Paragraph("Projects", header_style))
    projects_list = user_data["projects"].split(",")
    for project in projects_list:
        content.append(Paragraph(project.strip(), bullet_style))
    content.append(Spacer(1, 12))

    # Certifications Section
    content.append(Paragraph("Certifications", header_style))
    certifications_list = user_data["certifications"].split(",")
    for certification in certifications_list:
        content.append(Paragraph(certification.strip(), bullet_style))
    content.append(Spacer(1, 12))

    # Build the document
    doc.build(content)
    print(f"Advanced resume PDF generated successfully: {pdf_filename}")


if __name__ == "__main__":
    user_data = get_user_input()
    generate_pdf(user_data)
