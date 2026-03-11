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
        # Default font Arial rakha hai taaki error na aaye
        font_to_use = "Arial"
        if lang_choice in ["Hindi", "Marathi"]:
            try:
                # Agar FreeSans.ttf file hai toh hi use hogi
                self.add_font('FreeSans', '', 'FreeSans.ttf', unicode=True)
                self.set_font('FreeSans', '', 10)
                font_to_use = 'FreeSans'
            except:
                st.info("Note: Hindi/Marathi ke liye FreeSans.ttf file upload karein. Filhaal Arial use ho raha hai.")
        
        self.set_font(font_to_use, size=10)
        
        if photo_path:
            try:
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55)
            except: self.ln(15)
        else: self.ln(15)

        # --- Sidebar Details ---
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
        # Yahan Error Fix kiya hai data.get use karke
        self.multi_cell(55, 5, data.get('skills', ''))

        # --- Main Content ---
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font(font_to_use, 'B', 28)
        self.cell(130, 15, data.get('name', 'SONU SHARMA').upper(), ln=True)
        
        self.set_text_color(80, 80, 80)
        self.set_font(font_to_use, 'I', 11)
        self.set_x(75)
        self.multi_cell(120, 6, data.get('summary', ''))
        
        self.set_draw_color(*color)
        self.line(75, 62, 200, 62) 

        # Dynamic Sections
        y_pos = 68
        sections = [("WORK EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATIONS", 'certs')]
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
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "sonu_temp.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, lang_choice, photo_path)
    pdf.add_page_border(color)
    
    # Return as bytes for preview and download
    return pdf.output(dest='S')

# --- Streamlit Frontend ---
st.set_page_config(page_title="Resume Pro", layout="wide")
st.title("💎 Professional Resume Builder")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Edit Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email", "sharmas25924@gmail.com")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    lang = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    summary = st.text_area("Summary")
    experience = st.text_area("Work Experience")
    education = st.text_area("Education")
    uploaded_photo = st.file_uploader("📸 Photo", type=['jpg', 'png', 'jpeg'])
    theme = st.selectbox("Color Theme", ["Emerald Green", "Royal Gold", "Classic Black", "Midnight Blue", "Charcoal Grey", "Deep Red"])
    skills = st.text_area("Skills (e.g. Tally, AI, Management)")
    certs = st.text_area("Certifications")

with col2:
    st.subheader("Live Preview")
    # Data gathering
    data = {'name': name, 'email': email, 'phone': phone, 'address': address, 
            'summary': summary, 'education': education, 'experience': experience, 
            'skills': skills, 'certs': certs}
    
    if st.button("Refresh Preview"):
        try:
            pdf_bytes = create_pdf(data, theme, lang, uploaded_photo)
            # Preview using base64
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Download Button
            st.download_button(label="📥 Download PDF", data=pdf_bytes, file_name=f"{name}_Resume.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
