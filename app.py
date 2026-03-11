import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os

# --- PDF Generation Logic ---
class UltimateResume(FPDF):
    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        self.ln(10)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"Phone: {data['phone']}\nEmail: {data['email']}\nLoc: {data['address']}")
        
        self.ln(5)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, data['skills'])

        # Right Side Content
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font("Arial", 'B', 26)
        self.cell(130, 15, data['name'].upper(), ln=True)
        
        self.set_text_color(60, 60, 60)
        self.set_font("Arial", 'I', 10)
        self.set_x(75)
        self.multi_cell(120, 5, data['summary'])
        self.line(75, 60, 200, 60) 

        # Experience & Education
        y_pos = 65
        for title, content in [("WORK EXPERIENCE", data['experience']), ("EDUCATION", data['education'])]:
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font("Arial", 'B', 13)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", size=10)
            self.set_x(75)
            self.multi_cell(120, 5, content)
            y_pos = self.get_y() + 5

        # Photo on PDF (Small size)
        if photo_path:
            self.image(photo_path, x=75, y=y_pos + 5, w=30, h=35)
            y_pos += 45

        # Certifications
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
        photo_path = os.path.join(temp_dir, "sonu_final.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (300, 350), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Pro Resume Maker", layout="wide")
st.title("🚀 Pro AI Resume Builder")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Personal Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("City")
    dob = st.text_input("DOB")
    gender = st.selectbox("Gender", ["Male", "Female"])
    languages = st.text_input("Languages", "Hindi, Marathi, English")

with col2:
    st.subheader("💼 Career & Education")
    summary = st.text_area("Summary", "B.Com student specializing in management.")
    experience = st.text_area("Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education", "B.Com Degree")
    
    # NEW: Photo Upload Bar below Education
    uploaded_photo = st.file_uploader("📸 Upload Your Photo Here", type=['jpg', 'png', 'jpeg'])
    
    certs = st.text_area("Certifications", "MS-CIT, Tally Prime")
    theme = st.selectbox("Color Theme", ["Midnight Blue", "Charcoal Grey", "Deep Red"])

if st.button("Generate Resume"):
    data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'dob': dob, 'gender': gender, 'summary': summary, 'education': education, 'experience': experience, 'languages': languages, 'certs': certs}
    pdf_out = create_pdf(data, theme, uploaded_photo)
    st.download_button("📥 Save PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")
