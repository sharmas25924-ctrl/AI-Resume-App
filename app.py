import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os
import base64

class UltimateResume(FPDF):
    def add_page_border(self, color):
        self.set_draw_color(*color)
        self.set_line_width(1.0)
        self.rect(5, 5, 200, 287)

    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, lang_choice, photo_path=None):
        # Font Logic: Unicode support ke liye fpdf2 zaroori hai
        font_to_use = "helvetica" # Default English font
        
        if lang_choice in ["Hindi", "Marathi"]:
            if os.path.exists("FreeSans.ttf"):
                self.add_font('FreeSans', '', 'FreeSans.ttf')
                font_to_use = 'FreeSans'
            else:
                st.warning("Font 'FreeSans.ttf' nahi mila. English (Arial) use ho raha hai.")

        if photo_path:
            try:
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55)
            except: self.ln(15)
        else: self.ln(15)

        # Sidebar Contact
        self.set_text_color(255, 255, 255)
        self.set_font(font_to_use, 'B', 12)
        self.set_x(7)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        contact_info = f"Phone: {data.get('phone','')}\nEmail: {data.get('email','')}"
        self.multi_cell(55, 5, contact_info)
        
        # Skills Section (Error Fix)
        self.ln(10)
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
        
        self.set_draw_color(*color)
        self.line(75, 62, 200, 62) 

        # Sections
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
    themes = {"Emerald Green": (0, 77, 64), "Royal Gold": (184, 134, 11), "Classic Black": (0, 0, 0),
              "Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)}
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
    
    pdf_output = pdf.output()
    return pdf_output

# --- UI ---
st.set_page_config(page_title="Resume Builder", layout="wide")
st.title("💎 AI Resume Builder")

c1, c2 = st.columns([1, 1])

with c1:
    name = st.text_input("Name", "Sonu Sharma")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    lang = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    summary = st.text_area("Summary")
    experience = st.text_area("Experience")
    education = st.text_area("Education")
    photo = st.file_uploader("Photo", type=['jpg','png'])
    theme = st.selectbox("Theme", ["Emerald Green", "Royal Gold", "Classic Black", "Midnight Blue", "Charcoal Grey", "Deep Red"])
    skills = st.text_area("Skills")
    certs = st.text_area("Certifications")

with c2:
    st.subheader("Preview")
    data = {'name': name, 'email': email, 'phone': phone, 'address': address, 
            'summary': summary, 'education': education, 'experience': experience, 
            'skills': skills, 'certs': certs}
    
    if st.button("Refresh Preview"):
        try:
            pdf_data = create_pdf(data, theme, lang, photo)
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.download_button("Download PDF", data=pdf_data, file_name=f"{name}_Resume.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
