import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os
from streamlit_pdf_viewer import pdf_viewer

# --- PDF Generation Logic ---
class UltimateResume(FPDF):
    def add_page_border(self, color):
        self.set_draw_color(*color)
        self.set_line_width(1.0)
        self.rect(5, 5, 200, 287)

    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, lang_choice, photo_path=None):
        font_to_use = "helvetica"
        if lang_choice in ["Hindi", "Marathi"] and os.path.exists("FreeSans.ttf"):
            self.add_font('FreeSans', '', 'FreeSans.ttf')
            font_to_use = 'FreeSans'

        if photo_path:
            try:
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55)
            except: self.ln(15)
        else: self.ln(15)

        # Sidebar Details
        self.set_text_color(255, 255, 255)
        self.set_font(font_to_use, 'B', 12)
        self.set_x(7)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        self.multi_cell(55, 5, f"Phone: {data.get('phone','')}\nEmail: {data.get('email','')}")
        
        self.ln(5)
        self.set_font(font_to_use, 'B', 12)
        self.set_x(7)
        self.cell(60, 10, "SKILLS", ln=True)
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('skills', ''))

        # Main Body
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font(font_to_use, 'B', 28)
        self.cell(130, 15, data.get('name', 'SONU SHARMA').upper(), ln=True)
        
        self.set_text_color(80, 80, 80)
        self.set_font(font_to_use, '', 11)
        self.set_x(75)
        self.multi_cell(120, 6, data.get('summary', ''))
        self.line(75, 62, 200, 62) 

        y_pos = 68
        sections = [("EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATES", 'certs')]
        for title, key in sections:
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font(font_to_use, 'B', 14)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font(font_to_use, size=10)
            self.set_x(75)
            self.multi_cell(120, 5, data.get(key, ''))
            y_pos = self.get_y() + 5
            self.line(75, y_pos, 200, y_pos)
            y_pos += 4

def create_pdf(data, color_theme, lang_choice, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    themes = {"Emerald Green": (0, 77, 64), "Royal Gold": (184, 134, 11), "Classic Black": (0, 0, 0), "Deep Red": (139, 0, 0)}
    color = themes.get(color_theme, (0, 0, 0))
    
    photo_path = None
    if photo_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            img = Image.open(photo_file)
            img = ImageOps.fit(img, (350, 450), Image.LANCZOS).convert("RGB")
            img.save(tmp.name)
            photo_path = tmp.name
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, lang_choice, photo_path)
    pdf.add_page_border(color)
    
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_pdf.name)
    return tmp_pdf.name

# --- Responsive UI Design ---
st.set_page_config(page_title="AI Resume Maker", layout="wide")

# Sidebar for Theme & Language (Mobile par ye menu button ke andar chupa hota hai)
st.sidebar.title("🎨 Customization")
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi", "Marathi"])
theme = st.sidebar.selectbox("Theme Color", ["Emerald Green", "Royal Gold", "Classic Black", "Deep Red"])
uploaded_photo = st.sidebar.file_uploader("📸 Upload Photo", type=['jpg', 'png'])

st.title("🚀 AI Resume Builder Pro")
st.info("💡 Tip: Mobile par input bharne ke baad niche 'Show Preview' par click karein.")

# Main Layout
col_input, col_preview = st.columns([1, 1])

with col_input:
    st.subheader("👤 Personal Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    address = st.text_area("Address")
    
    st.subheader("💼 Professional Details")
    summary = st.text_area("Profile Summary")
    experience = st.text_area("Experience (Company, Role, Years)")
    education = st.text_area("Education (Degree, College)")
    skills = st.text_area("Skills (Python, AI, Management)")
    certs = st.text_area("Certifications")

with col_preview:
    st.subheader("📄 Live Resume Preview")
    user_data = {'name': name, 'phone': phone, 'email': email, 'address': address, 
                 'summary': summary, 'education': education, 'experience': experience, 
                 'skills': skills, 'certs': certs}
    
    # Button to trigger preview
    if st.button("🔄 Update & Show Preview", use_container_width=True):
        try:
            pdf_path = create_pdf(user_data, theme, lang, uploaded_photo)
            # Mobile-friendly width
            pdf_viewer(input=pdf_path, width=700)
            
            with open(pdf_path, "rb") as f:
                st.download_button(label="📥 Download Resume (PDF)", 
                                 data=f, 
                                 file_name=f"{name}_Resume.pdf",
                                 mime="application/pdf",
                                 use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
