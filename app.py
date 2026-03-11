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
        # Multilingual Font Handling
        font_to_use = "Arial"
        if lang_choice in ["Hindi", "Marathi"]:
            try:
                self.add_font('FreeSans', '', 'FreeSans.ttf', unicode=True)
                self.set_font('FreeSans', '', 10)
                font_to_use = 'FreeSans'
            except:
                st.warning("Font 'FreeSans.ttf' missing! Showed in Arial.")
        
        self.set_font(font_to_use, size=10)
        
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
        contact_title = "संपर्क" if lang_choice in ["Hindi", "Marathi"] else "CONTACT"
        self.cell(60, 10, contact_title, ln=True)
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        self.multi_cell(55, 5, f"Phone: {data.get('phone','')}\nEmail: {data.get('email','')}")
        
        self.ln(2)
        addr_title = "पत्ता:" if lang_choice in ["Hindi", "Marathi"] else "ADDRESS:"
        self.set_font(font_to_use, 'B', 10)
        self.set_x(7)
        self.cell(60, 5, addr_title, ln=True)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('address', ''))

        self.ln(8)
        self.set_font(font_to_use, 'B', 12)
        self.set_x(7)
        skills_title = "कौशल्य" if lang_choice == "Marathi" else ("कौशल" if lang_choice == "Hindi" else "SKILLS")
        self.cell(60, 10, skills_title, ln=True)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('skills', ''))

        # Main Content
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font(font_to_use, 'B', 28)
        self.cell(130, 15, data.get('name', '').upper(), ln=True)
        
        self.set_text_color(80, 80, 80)
        self.set_font(font_to_use, 'I', 11)
        self.set_x(75)
        self.multi_cell(120, 6, data.get('summary', ''))
        self.set_draw_color(*color)
        self.line(75, 62, 200, 62) 

        y_pos = 68
        titles = {"English": [("WORK EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATIONS", 'certs')],
                  "Hindi": [("कार्य अनुभव", 'experience'), ("शिक्षा", 'education'), ("प्रमाण पत्र", 'certs')],
                  "Marathi": [("अनुभव", 'experience'), ("शिक्षण", 'education'), ("प्रमाणपत्रे", 'certs')]}
        
        for title, key in titles.get(lang_choice, titles["English"]):
            self.set_xy(75, y_pos)
            self.set_text_color(*color)
            self.set_font(font_to_use, 'B', 14)
            self.cell(130, 8, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font(font_to_use, size=10)
            self.set_x(75)
            self.multi_cell(120, 5, data.get(key, ''))
            y_pos = self.get_y() + 5
            self.set_draw_color(220, 220, 220)
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
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "preview_photo.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, lang_choice, photo_path)
    pdf.add_page_border(color)
    return pdf.output(dest='S')

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Maker Preview", layout="wide")

# UI Layout: Input Left, Preview Right
col_input, col_preview = st.columns([1, 1])

with col_input:
    st.header("📝 Edit Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email", "sharmas25924@gmail.com")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    lang = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    summary = st.text_area("Summary")
    experience = st.text_area("Experience")
    education = st.text_area("Education")
    uploaded_photo = st.file_uploader("📸 Photo", type=['jpg', 'png', 'jpeg'])
    theme = st.selectbox("Color Theme", ["Emerald Green", "Royal Gold", "Classic Black", "Midnight Blue", "Charcoal Grey", "Deep Red"])
    skills = st.text_area("Skills")
    certs = st.text_area("Certifications")

with col_preview:
    st.header("👀 Live Preview")
    user_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'summary': summary, 'education': education, 'experience': experience, 'skills': skills, 'certs': certs}
    
    if st.button("Refresh Preview"):
        try:
            pdf_bytes = create_pdf(user_data, theme, lang, uploaded_photo)
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Download button inside preview
            st.download_button(label="📥 Download This PDF", data=pdf_bytes, file_name=f"{name}_Resume.pdf")
        except Exception as e:
            st.error(f"Error: {e}. Check if font file is missing.")
