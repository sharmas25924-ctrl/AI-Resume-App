import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# --- Resume Design Class (Final Fix) ---
class UltimateResume(FPDF):
    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        # 1. NEW: Passport-Size Photo placement (Centered & Small)
        if photo_path:
            try:
                # Isko exact fit karne ke liye values set ki hain
                self.image(photo_path, x=15, y=10, w=40)
                # Text ko photo ke niche lane ke liye exact gap:
                self.ln(50) 
            except Exception as e:
                self.ln(20)
                st.warning(f"Photo error: {e}")
        else:
            self.ln(20)

        # 2. Sidebar Contact Info
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 14)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        # Use simple format for better fitting
        self.cell(60, 6, f"Phone: {data['phone']}", ln=True)
        self.cell(60, 6, f"Email: {data['email']}", ln=True)
        self.cell(60, 6, f"Loc: {data['address']}", ln=True)
        
        # 3. Personal Info
        self.ln(5)
        self.set_font("Arial", 'B', 14)
        self.set_x(5)
        self.cell(60, 10, "PERSONAL", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.cell(60, 6, f"DOB: {data['dob']}", ln=True)
        self.cell(60, 6, f"Gender: {data['gender']}", ln=True)
        # Multi_cell handles long text
        self.multi_cell(60, 6, f"Lang: {data['languages']}")

        # 4. Skills Section
        self.ln(5)
        self.set_font("Arial", 'B', 14)
        self.set_x(5)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 6, data['skills'])

        # --- Main Body (Right Side) ---
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font("Arial", 'B', 28)
        self.cell(130, 15, data['name'].upper(), ln=True)
        
        self.set_text_color(50, 50, 50)
        self.set_font("Arial", 'I', 11)
        self.set_x(75)
        self.multi_cell(120, 6, data['summary'])
        
        self.ln(5)
        self.set_draw_color(*color)
        self.line(75, 65, 200, 65) 
        
        # Work Experience
        self.set_xy(75, 72)
        self.set_text_color(*color)
        self.set_font("Arial", 'B', 14)
        self.cell(130, 10, "WORK EXPERIENCE", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=10)
        self.set_x(75)
        self.multi_cell(120, 6, data['experience'])
        
        # Education
        self.ln(5)
        self.set_x(75)
        self.set_text_color(*color)
        self.set_font("Arial", 'B', 14)
        self.cell(130, 10, "EDUCATION", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=10)
        self.set_x(75)
        self.multi_cell(120, 6, data['education'])
        
        # Certifications
        self.ln(5)
        self.set_x(75)
        self.set_text_color(*color)
        self.set_font("Arial", 'B', 14)
        self.cell(130, 10, "CERTIFICATIONS", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=10)
        self.set_x(75)
        self.multi_cell(120, 6, data['certs'])

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    themes = {"Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)}
    color = themes[color_theme]
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "temp_photo.png")
        img = Image.open(photo_file)
        # Passport ratio aspect: 35mm x 45mm
        # We process this in Pillow before FPDF
        # Ise standardized size (400x514) mein save karte hain
        img = img.resize((400, 514), Image.LANCZOS)
        img.save(photo_path)
    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    # Important: UTF-8 encoding is NOT fully supported by default Arial in FPDF
    # This might cause a 'latin-1' error if non-English chars are used.
    # If Sonu gets a latin-1 error, he must only use English text in input fields.
    try:
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    except UnicodeEncodeError:
        st.error("Text mein koi non-English character hai (jaise Marathi). FPDF default Arial sirf English support karta hai. Us character ko hataiye ya English mein likhiye.")
        st.stop()
    return pdf_bytes

# --- Streamlit Frontend ---
st.set_page_config(page_title="AI Resume Maker", layout="wide")
st.sidebar.title("💎 Design")
theme = st.sidebar.selectbox("Color Theme", ["Midnight Blue", "Charcoal Grey", "Deep Red"])
uploaded_photo = st.sidebar.file_uploader("Upload Your Passport-Size Photo", type=['jpg', 'png', 'jpeg'])

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email", "SHARMAS25924@GMAIL.COM")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    dob = st.text_input("DOB")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    languages = st.text_input("Languages", "Hindi, English, Marathi")
with col2:
    summary = st.text_area("Summary", "B.Com student specializing in management.")
    skills = st.text_area("Skills", "Accounting, Tally, AI, Operations")
    experience = st.text_area("Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education", "B.Com - University Name")
    certs = st.text_area("Certifications", "MS-CIT, Tally Prime, AI Prompting")

user_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'dob': dob, 'gender': gender, 'summary': summary, 'education': education, 'skills': skills, 'experience': experience, 'languages': languages, 'certs': certs}

if st.button("Generate My Professional Resume"):
    if name and email:
        pdf_out = create_pdf(user_data, theme, uploaded_photo)
        st.download_button("Click here to Save PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")
