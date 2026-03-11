import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

class UltimateResume(FPDF):
    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        # PHOTO SIZE FIX: Small Passport Size
        if photo_path:
            try:
                # x=17 sidebar ke beech mein hai, w=35 chota size hai
                self.image(photo_path, x=17, y=12, w=35)
                self.ln(55) # Photo ke niche gap
            except:
                self.ln(20)
        else:
            self.ln(20)

        # CONTACT SECTION
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"Phone: {data['phone']}\nEmail: {data['email']}\nLoc: {data['address']}")
        
        # PERSONAL SECTION
        self.ln(5)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "PERSONAL", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"DOB: {data['dob']}\nGender: {data['gender']}\nLang: {data['languages']}")

        # SKILLS SECTION
        self.ln(5)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, data['skills'])

        # MAIN CONTENT (RIGHT SIDE)
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font("Arial", 'B', 26)
        self.cell(130, 15, data['name'].upper(), ln=True)
        
        self.set_text_color(60, 60, 60)
        self.set_font("Arial", 'I', 10)
        self.set_x(75)
        self.multi_cell(120, 5, data['summary'])
        
        self.set_draw_color(*color)
        self.line(75, 60, 200, 60) 
        
        # Sections: Experience, Education, Certs
        sections = [
            ("WORK EXPERIENCE", data['experience']),
            ("EDUCATION", data['education']),
            ("CERTIFICATIONS", data['certs'])
        ]
        
        current_y = 65
        for title, content in sections:
            self.set_xy(75, current_y)
            self.set_text_color(*color)
            self.set_font("Arial", 'B', 13)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", size=10)
            self.set_x(75)
            self.multi_cell(120, 5, content)
            current_y = self.get_y() + 5

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    themes = {"Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)}
    color = themes[color_theme]
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "resume_pic.png")
        img = Image.open(photo_file)
        # Passport ratio fix
        img = img.convert("RGB")
        img.save(photo_path)

    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.set_page_config(page_title="AI Resume Maker", layout="wide")
st.sidebar.title("Resume Settings")
theme = st.sidebar.selectbox("Theme Color", ["Midnight Blue", "Charcoal Grey", "Deep Red"])
uploaded_photo = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])

st.title("🚀 Professional AI Resume Builder")
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email", "sharmas25924@gmail.com")
    phone = st.text_input("Phone")
    address = st.text_input("City, State")
    dob = st.text_input("DOB (DD/MM/YYYY)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    languages = st.text_input("Languages", "Hindi, English, Marathi")
with c2:
    summary = st.text_area("Summary", "B.Com student with management skills.")
    skills = st.text_area("Skills", "Tally, AI, Operations")
    experience = st.text_area("Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education", "B.Com Degree")
    certs = st.text_area("Certifications", "MS-CIT, Tally Prime")

user_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'dob': dob, 'gender': gender, 'summary': summary, 'education': education, 'skills': skills, 'experience': experience, 'languages': languages, 'certs': certs}

if st.button("Generate & Download Resume"):
    try:
        pdf_out = create_pdf(user_data, theme, uploaded_photo)
        st.download_button("📥 Click to Download PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")
    except Exception as e:
        st.error(f"Error: {e}. Please use English text only.")
