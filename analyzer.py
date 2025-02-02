import re
import pdfplumber
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_dates(text):
    date_patterns = [
        r"(\w+)\s+(\d{4})\s*-\s*(\w+)\s+(\d{4})", 
        r"(\d{4})\s*-\s*(\d{4})"  
    ]

    matches = []
    
    for pattern in date_patterns:
        for match in re.findall(pattern, text):
            matches.append(match)
    
    return matches

def convert_dates_to_experience(date_ranges):
    total_experience = 0 
    for date_range in date_ranges:
        if len(date_range) == 4: 
            start_month, start_year, end_month, end_year = date_range
            try:
                start_date = datetime.strptime(f"{start_month} {start_year}", "%B %Y")
                end_date = datetime.strptime(f"{end_month} {end_year}", "%B %Y")
                experience_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                total_experience += experience_months
            except ValueError:
                continue  

        elif len(date_range) == 2:  
            start_year, end_year = date_range
            try:
                start_year, end_year = int(start_year), int(end_year)
                experience_months = (end_year - start_year) * 12
                total_experience += experience_months
            except ValueError:
                continue  

    return round(total_experience / 12, 1) if total_experience > 0 else "Not provided"
def extract_experience(text):
    date_ranges = extract_dates(text)

    if "EDUCATION" in text:
        education_section = text.split("EDUCATION")[1] 
        education_dates = extract_dates(education_section)  
        date_ranges = [date for date in date_ranges if date not in education_dates]

    experience = convert_dates_to_experience(date_ranges)
    return f"{experience} years" if experience != "Not provided" else experience

def extract_skills(text):
    skill_keywords = [
        "Python", "Java", "Machine Learning", "Data Analysis", "SQL", "JavaScript",
        "C++", "React", "Node.js", "AWS", "Django", "TensorFlow", "Deep Learning",
        "Flask", "Excel", "Communication", "Leadership", "Problem Solving", "Public Speaking"
    ]
    
    extracted_skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    return extracted_skills if extracted_skills else ["Not found"]

def generate_feedback(skills, experience):
    feedback = []

    required_skills = ["Python", "Machine Learning", "SQL", "Data Analysis"]
    missing_skills = [skill for skill in required_skills if skill not in skills]

    if missing_skills:
        feedback.append(f"Consider adding these skills to your resume: {', '.join(missing_skills)}.")

    if experience == "Not provided":
        feedback.append("Consider explicitly mentioning your years of experience in relevant job roles.")

    return feedback if feedback else ["Your resume looks well-structured!"]

def analyze_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)

    skills = extract_skills(resume_text)
    experience = extract_experience(resume_text)
    feedback = generate_feedback(skills, experience)

    return {"skills": skills, "experience": experience, "feedback": feedback}
