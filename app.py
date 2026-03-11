import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os

class UltimateResume(FPDF):
    def add_page_border(self, color):
        self.set_draw_color(*color)
        self.set_line_width(1.0)
        self.rect(5, 5, 200, 287)

    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        # Font settings for Multilingual support
        # Note: 'FreeSans' supports Hindi/Marathi characters
        self.add_font('FreeSans', '', 'FreeSans.ttf', unicode=True)
        self.add_font('FreeSans', 'B', 'FreeSansBold.ttf', unicode=True)
        
        if photo_path:
            try:
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55)
            except: self.ln(15)
        else: self.ln(15)

        # --- SIDEBAR CONTACT ---
        self.set_text_color(255, 255, 255)
        self.set_font("FreeSans", 'B', 12)
        self.set_x(7)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("FreeSans", size=9)
        self.set_x(7)
        self.multi_cell(55, 5, f"Phone: {data.get('phone','')}\nEmail: {data.get('email','')}")
        
        self.ln(2)
        self.set_font("FreeSans", 'B', 10)
        self.set_x(7)
        self.cell(60, 5, "ADDRESS:", ln=True)
        self.set_font("FreeSans", size=9)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('address', ''))

        self.ln(8)
        self.set_font("FreeSans", 'B', 12)
        self.set_x(7)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font("FreeSans", size=9)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('skills', ''))

        # --- MAIN CONTENT ---
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font("FreeSans", 'B', 28)
        self.cell(130, 15, data.get('name', '').upper(), ln=True)
        
        self.set_text_color(80, 80, 80)
        self.set_font("FreeSans", '', 11)
        self.set_x(75)
        self.multi_cell(120, 6, data.get('summary', ''))
        self.set_draw_color(*color)
        self.line(75, 62, 200, 62) 

        y_pos = 68
        sections = [("WORK EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATIONS", 'certs')]
        for title, key in sections:
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font("FreeSans", 'B', 14)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("FreeSans", size=10)
            self.set_x(75)
            self.multi_cell(120, 5, data.get(key, ''))
            y_pos = self.get_y() + 5
            self.set_draw_color(220, 220, 220)
            self.line(75, y_pos, 200, y_pos)
            y_pos += 4

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    
    themes = {
        "Emerald Green": (0, 77, 64),
        "Royal Gold": (184, 134, 11),
        "Classic Black": (0, 0, 0),
        "Midnight Blue": (26, 35, 126),
        "Charcoal Grey": (51, 51, 51),
        "Deep Red": (139, 0, 0)
    }
    color = themes.get(color_theme, (0, 0, 0))
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "sonu_multilang.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    pdf.add_page_border(color)
    
    return pdf.output(dest='S').encode('utf-8') # Use utf-8 encoding

# --- Streamlit UI ---
st.set_page_config(page_title="Multilingual AI Resume Maker", layout="wide")
st.title("💎 Multilingual Resume Builder (English, Hindi, Marathi)")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", "Sonu Sharma") 
    email = st.text_input("Email", "sharmas25924@gmail.com")
    phone = st.text_input("Phone")
    address = st.text_area("Address (Address in any language)")
    summary = st.text_area("Summary (Summary in any language)")

with col2:
    experience = st.text_area("Experience (Experience in any language)")
    education = st.text_area("Education")
    uploaded_photo = st.file_uploader("📸 Upload Photo", type=['jpg', 'png', 'jpeg'])
    skills = st.text_area("Skills")
    certs = st.text_area("Certifications")
    theme = st.selectbox("Color Theme", ["Emerald Green", "Royal Gold", "Classic Black", "Midnight Blue", "Charcoal Grey", "Deep Red"])

if st.button("Generate Resume"):
    user_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'summary': summary, 'education': education, 'experience': experience, 'skills': skills, 'certs': certs}
    try:
        pdf_out = create_pdf(user_data, theme, uploaded_photo)
        st.download_button(
            label="📥 Download Multilingual PDF", 
            data=pdf_out, 
            file_name=f"{name}_Resume.pdf" 
        )
    except Exception as e:
        st.error(f"Error: {e}. Make sure Font files are present.")
