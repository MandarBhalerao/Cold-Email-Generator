import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    all_text = "\n".join(pages) if pages else ""
    print(all_text)
    return all_text

def extract_resume_details(resume_text):
    # Example regex patterns to extract different parts of the resume
    name_match = re.search(r"Name:\s*(.*)", resume_text)
    name = name_match.group(1).strip() if name_match else "Name not found"

    education_match = re.search(r"Education:(.*?)(?=\nExperience:)", resume_text, re.DOTALL)
    education = education_match.group(1).strip() if education_match else "Education details not found"

    experience_match = re.search(r"Experience:(.*?)(?=\nProjects:)", resume_text, re.DOTALL)
    experience = experience_match.group(1).strip() if experience_match else "Experience details not found"

    projects_match = re.search(r"Projects:(.*?)(?=\nSkills:)", resume_text, re.DOTALL)
    projects = projects_match.group(1).strip() if projects_match else "Project details not found"

    skills_match = re.search(r"Skills:(.*)", resume_text)
    skills = skills_match.group(1).strip() if skills_match else "Skills details not found"

    achievements_match = re.search(r"Achievements:(.*)", resume_text)
    achievements = achievements_match.group(1).strip() if achievements_match else "Achievements not found"

    return {
        "name": name,
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": skills,
        "achievements": achievements
    }

def generate_cold_email(details):
    return f"""
You are {details['name']}, a graduate from {details['education']}. Your professional experience includes {details['experience']}. You have led projects such as {details['projects']} and are skilled in {details['skills']}. You have also achieved {details['achievements']}.

Your task is to write a cold email to a potential employer or client, showcasing your skills and experiences detailed above. Mention your hands-on experience with technologies and how you can contribute to solving real-world problems.

Remember, you are {details['name']}, ready to make a significant impact in your new role.
    """

def process_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    details = extract_resume_details(text)
    email_prompt = generate_cold_email(details)

    output_path = "Cold_Email_Prompt.txt"
    with open(output_path, "w") as file:
        file.write(email_prompt)
    
    return output_path

# Example usage
# pdf_path = "C:\Users\Admin\Downloads\Mandar_Bhalerao_IISc.pdf"  # Use the actual path to the PDF file
pdf_path = "C:/Users/Admin/Downloads/Mandar_Bhalerao_IISc.pdf"

output_path = process_resume(pdf_path)
print(f"Cold email prompt saved at: {output_path}")
