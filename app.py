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

    def add_content(self, data, color, lang_choice, photo_path=None):
        # Multilingual Font Support
        if lang_choice in ["Hindi", "Marathi"]:
            try:
                self.add_font('FreeSans', '', 'FreeSans.ttf', unicode=True)
                self.set_font('FreeSans', '', 10)
                font_to_use = 'FreeSans'
            except:
                st.warning("Font 'FreeSans.ttf' missing! Using Arial.")
                self.set_font("Arial", size=10)
                font_to_use = 'Arial'
        else:
            self.set_font("Arial", size=10)
            font_to_use = 'Arial'
        
        if photo_path:
            try:
                self.image(photo_path, x=17.5, y=10, w=35, h=45)
                self.ln(55)
            except: self.ln(15)
        else: self.ln(15)

        # --- SIDEBAR CONTACT ---
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
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('address', ''))

        self.ln(8)
        skills_title = "कौशल्य" if lang_choice == "Marathi" else ("कौशल" if lang_choice == "Hindi" else "SKILLS")
        self.set_font(font_to_use, 'B', 12)
        self.set_x(7)
        self.cell(60, 10, skills_title, ln=True)
        self.set_font(font_to_use, size=9)
        self.set_x(7)
        self.multi_cell(55, 5, data.get('skills', ''))

        # --- MAIN CONTENT ---
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
        if lang_choice == "Marathi":
            titles = [("अनुभव", 'experience'), ("शिक्षण", 'education'), ("प्रमाणपत्रे", 'certs')]
        elif lang_choice == "Hindi":
            titles = [("कार्य अनुभव", 'experience'), ("शिक्षा", 'education'), ("प्रमाण पत्र", 'certs')]
        else:
            titles = [("WORK EXPERIENCE", 'experience'), ("EDUCATION", 'education'), ("CERTIFICATIONS", 'certs')]

        for title, key in titles:
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
    themes = {
        "Emerald Green": (0, 77, 64), "Royal Gold": (184, 134, 11), "Classic Black": (0, 0, 0),
        "Midnight Blue": (26, 35, 126), "Charcoal Grey": (51, 51, 51), "Deep Red": (139, 0, 0)
    }
    color = themes.get(color_theme, (0, 0, 0))
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "sonu_resume.jpg")
        img = Image.open(photo_file)
        img = ImageOps.fit(img, (350, 450), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(photo_path)
    
    pdf.add_sidebar(color)
    pdf.add_content(data, color, lang_choice, photo_path)
    pdf.add_page_border(color)
    return pdf.output(dest='S').encode('latin-1' if lang_choice == "English" else 'utf-8')

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Maker", layout="wide")
st.title("💎 AI Resume Builder Pro")

col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 Contact")
    name = st.text_input("Name", "Sonu Sharma") 
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_area("Address")
    lang_choice = st.selectbox("Language / भाषा निवडा", ["English", "Hindi", "Marathi"])

with col2:
    st.subheader("💼 Career")
    summary = st.text_area("Summary")
    experience = st.text_area("Experience")
    education = st.text_area("Education")
    uploaded_photo = st.file_uploader("📸 Photo", type=['jpg', 'png', 'jpeg'])
    
    # --- COLOR THEME YAHAN WAPIS AA GAYA HAI ---
    theme_choice = st.selectbox("Color Theme", ["Emerald Green", "Royal Gold", "Classic Black", "Midnight Blue", "Charcoal Grey", "Deep Red"])
    
    skills = st.text_area("Skills")
    certs = st.text_area("Certifications")

if st.button("Generate Resume"):
    user_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'summary': summary, 'education': education, 'experience': experience, 'skills': skills, 'certs': certs}
    try:
        pdf_out = create_pdf(user_data, theme_choice, lang_choice, uploaded_photo)
        st.download_button(label=f"📥 Download {name}_Resume.pdf", data=pdf_out, file_name=f"{name}_Resume.pdf")
    except Exception as e:
        st.error(f"Error: {e}. Hindi/Marathi ke liye FreeSans.ttf upload karein.")
