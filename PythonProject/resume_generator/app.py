import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER  # Import for center alignment

#validation
def validate_input(prompt, pattern, error_message):
    """Validates user input against a given regex pattern."""
    while True:
        user_input = input(prompt).strip()
        if re.match(pattern, user_input):
            return user_input
        else:
            print(f"Error: {error_message}")


def get_user_input():
    """Collects user input from the console with validation."""
    name = input("Enter your full name: ").strip()
    title = input("Enter your job title or profession: ").strip()
    email = validate_input("Enter your email: ", r"^[\w\.-]+@[\w\.-]+\.\w+$",
                           "Invalid email format. Example: example@email.com")
    phone = validate_input("Enter your phone number: ", r"^\+?\d{10,15}$",
                           "Invalid phone number. Use digits only (with optional +).")
    linkedin = validate_input("Enter your LinkedIn profile link: ", r"^https?:\/\/(www\.)?linkedin\.com\/.*$",
                              "Invalid LinkedIn URL. Example: https://www.linkedin.com/in/yourprofile")
    github = validate_input("Enter your GitHub profile link: ", r"^https?:\/\/(www\.)?github\.com\/.*$",
                            "Invalid GitHub URL. Example: https://github.com/yourusername")
    summary = input("Enter your professional summary: ").strip()

    experiences = []
    while True:
        job_title = input("Enter job title (or press enter to stop): ").strip()
        if not job_title:
            break
        company = input("Enter company name: ").strip()
        duration = input("Enter job duration (e.g., Jan 2020 - Present): ").strip()
        responsibilities = input("Enter responsibilities (separate by semicolon): ").split(";")
        experiences.append((job_title, company, duration, responsibilities))

    education = []
    while True:
        degree = input("Enter degree (or press enter to stop): ").strip()
        if not degree:
            break
        specialization = input("Enter specialization (e.g., Data Science, AI, Cybersecurity): ").strip()
        university = input("Enter university name: ").strip()
        grad_year = input("Enter graduation year: ").strip()
        education.append((degree, specialization, university, grad_year))

    skills = input("Enter your skills (separate by commas): ").split(",")

    achievements = input("Enter key achievements (separate by semicolon): ").split(";")

    return {
        "name": name,
        "title": title,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "summary": summary,
        "experiences": experiences,
        "education": education,
        "skills": skills,
        "achievements": achievements
    }


def generate_pdf(user_data):
    """Generates a structured resume PDF."""
    pdf_filename = "structured_resume.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    # Updated styles with larger fonts
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=24, textColor=colors.HexColor("#2E4053"),
                                 spaceAfter=10)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Heading2"], fontSize=16,
                                    textColor=colors.HexColor("#1F618D"))
    body_style = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=12, leading=16, spaceAfter=8)
    bullet_style = ParagraphStyle("Bullet", parent=styles["BodyText"], fontSize=12, leading=16, leftIndent=14,
                                  spaceAfter=4, bulletText="• ")

    # Center alignment style for contact info
    center_style = ParagraphStyle("Center", parent=body_style, alignment=TA_CENTER)

    content = []

    # Name and title
    content.append(
        Paragraph(f"{user_data['name']}<br/><font size=14 color='#1F618D'>{user_data['title']}</font>", title_style))
    content.append(Spacer(1, 12))

    # Contact details - Center Aligned
    contact_info = f"""
    ☎ {user_data['phone']} | ✉ {user_data['email']}<br/>
    🌐 <a href='{user_data['linkedin']}' color='blue'>LinkedIn</a> | 💻 <a href='{user_data['github']}' color='blue'>GitHub</a>
    """
    content.append(Paragraph(contact_info, center_style))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1F618D")))

    # Summary
    content.append(Spacer(1, 12))
    content.append(Paragraph("SUMMARY", subtitle_style))
    content.append(Paragraph(user_data["summary"], body_style))
    content.append(Spacer(1, 12))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#566573")))

    # Skills
    content.append(Spacer(1, 12))
    content.append(Paragraph("SKILLS", subtitle_style))
    skills_text = ", ".join([skill.strip() for skill in user_data["skills"]])
    content.append(Paragraph(skills_text, body_style))
    content.append(Spacer(1, 12))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#566573")))

    # Experience
    content.append(Spacer(1, 12))
    content.append(Paragraph("EXPERIENCE", subtitle_style))
    for job in user_data["experiences"]:
        content.append(Paragraph(f"<b>{job[0]}</b> - {job[1]}<br/><font size=12>{job[2]}</font>", body_style))
        for responsibility in job[3]:
            content.append(Paragraph(responsibility.strip(), bullet_style))
        content.append(Spacer(1, 12))

    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#566573")))

    # Education (with specialization)
    content.append(Spacer(1, 12))
    content.append(Paragraph("EDUCATION", subtitle_style))
    for edu in user_data["education"]:
        content.append(Paragraph(f"<b>{edu[0]} in {edu[1]}</b><br/>{edu[2]}, {edu[3]}", body_style))
        content.append(Spacer(1, 8))

    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#566573")))

    # Key Achievements
    content.append(Spacer(1, 12))
    content.append(Paragraph("KEY ACHIEVEMENTS", subtitle_style))
    for achievement in user_data["achievements"]:
        content.append(Paragraph(f"✅ {achievement.strip()}", body_style))

    doc.build(content)
    print(f"Resume PDF generated: {pdf_filename}")


if __name__ == "__main__":
    user_data = get_user_input()
    generate_pdf(user_data)
