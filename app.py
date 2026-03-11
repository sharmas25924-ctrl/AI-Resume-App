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
        # --- PHOTO IN CORNER (SIDEBAR TOP) ---
        if photo_path:
            try:
                # x=17.5 sidebar ke beech mein, y=10 ekdam top corner area mein
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55) # Photo ke niche gap taaki text overlap na ho
            except:
                self.ln(15)
        else:
            self.ln(15)

        # Sidebar Details
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, f"Phone: {data.get('phone','')}\nEmail: {data.get('email','')}\nLoc: {data.get('address','')}")
        
        self.ln(8)
        self.set_font("Arial", 'B', 12)
        self.set_x(5)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        self.multi_cell(60, 5, data.get('skills', ''))

        # Main Page Content (Right Side)
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font("Arial", 'B', 26)
        self.cell(130, 15, data.get('name', 'SONU').upper(), ln=True)
        
        self.set_text_color(60, 60, 60)
        self.set_font("Arial", 'I', 10)
        self.set_x(75)
        self.multi_cell(120, 5, data.get('summary', ''))
        self.line(75, 60, 200, 60) 

        # Experience & Education
        y_pos = 65
        for title, key in [("WORK EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATIONS", 'certs')]:
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font("Arial", 'B', 13)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", size=10)
            self.set_x(75)
            self.multi_cell(120, 5, data.get(key, ''))
            y_pos = self.get_y() + 5

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    themes = {"Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)}
    color = themes.get(color_theme, (51, 51, 51))
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "sonu_corner.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- Streamlit UI ---
st.set_page_config(page_title="Pro AI Resume Builder", layout="wide")
st.title("🚀 Pro AI Resume Builder")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📌 Personal Info")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email", "sharmas25924@gmail.com")
    phone = st.text_input("Phone")
    address = st.text_input("City")
    summary = st.text_area("Summary", "B.Com student specializing in management.")

with col2:
    st.subheader("💼 Career Details")
    experience = st.text_area("Work Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education Details", "B.Com Degree")
    
    # UI par button yahin rahega (Education ke niche)
    uploaded_photo = st.file_uploader("📸 Upload Your Photo", type=['jpg', 'png', 'jpeg'])
    
    skills = st.text_area("Skills", "Accounting, Tally, AI")
    certs = st.text_area("Certifications", "MS-CIT, Tally Prime")
    theme = st.selectbox("Color Theme", ["Midnight Blue", "Charcoal Grey", "Deep Red"])

if st.button("Generate Resume"):
    user_data = {
        'name': name, 'email': email, 'phone': phone, 'address': address, 
        'summary': summary, 'education': education, 'experience': experience, 
        'skills': skills, 'certs': certs
    }
    try:
        pdf_out = create_pdf(user_data, theme, uploaded_photo)
        st.download_button("📥 Save PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")
    except Exception as e:
        st.error(f"Error: {e}. Please use English text only.")
