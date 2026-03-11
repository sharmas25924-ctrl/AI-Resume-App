import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os

class UltimateResume(FPDF):
    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        # Sidebar Details (Photo yahan se hata di gayi hai)
        self.ln(10)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"Phone: {data['phone']}\nEmail: {data['email']}\nLoc: {data['address']}")
        
        self.ln(10)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "PERSONAL", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"DOB: {data['dob']}\nGender: {data['gender']}\nLang: {data['languages']}")

        self.ln(10)
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
        self.line(75, 60, 200, 60) 
        
        # Sections: Experience & Education
        y_pos = 65
        sections = [("WORK EXPERIENCE", data['experience']), ("EDUCATION", data['education'])]
        for title, content in sections:
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font("Arial", 'B', 13)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", size=10)
            self.set_x(75)
            self.multi_cell(120, 5, content)
            y_pos = self.get_y() + 5

        # PHOTO BELOW EDUCATION
        if photo_path:
            try:
                # Education ke niche gap dekar photo set ki hai
                current_y = self.get_y() + 10
                # Right side mein align karne ke liye x=75 rakha hai
                self.image(photo_path, x=75, y=current_y, w=35, h=45)
                y_pos = current_y + 50
            except:
                y_pos = self.get_y() + 5
        else:
            y_pos = self.get_y() + 5

        # CERTIFICATIONS (Sabse niche)
        self.set_xy(75, y_pos)
        self.set_text_color(*color)
        self.set_font("Arial", 'B', 13)
        self.cell(130, 8, "CERTIFICATIONS", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=10)
        self.set_x(75)
        self.multi_cell(120, 5, data['certs'])

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    themes = {"Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)}
    color = themes[color_theme]
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "sonu_main.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)

    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# UI Code (Same as before)
st.set_page_config(page_title="Pro Resume Maker", layout="wide")
st.sidebar.title("Settings")
theme = st.sidebar.selectbox("Color Theme", ["Midnight Blue", "Charcoal Grey", "Deep Red"])
uploaded_photo = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])

st.title("🚀 Pro AI Resume Builder")
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("City")
    dob = st.text_input("DOB")
    gender = st.selectbox("Gender", ["Male", "Female"])
    languages = st.text_input("Languages", "Hindi, Marathi, English")
with c2:
    summary = st.text_area("Summary", "B.Com student specializing in management.")
    skills = st.text_area("Skills", "Tally, AI, Management")
    experience = st.text_area("Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education", "B.Com Degree")
    photo =
    certs = st.text_area("Certifications", "MS-CIT, Tally Prime")

if st.button("Generate Resume"):
    data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'dob': dob, 'gender': gender, 'summary': summary, 'education': education, 'skills': skills, 'experience': experience, 'languages': languages, 'certs': certs}
    pdf_out = create_pdf(data, theme, uploaded_photo)
    st.download_button("📥 Save PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")36526

