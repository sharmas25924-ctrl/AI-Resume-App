import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# --- Resume Design Class ---
class UltimateResume(FPDF):
    def add_sidebar(self, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 70, 297, 'F')

    def add_content(self, data, color, photo_path=None):
        # 1. Sidebar Photo placement
        if photo_path:
            try:
                self.image(photo_path, x=12, y=10, w=45)
                self.ln(50) 
            except:
                self.ln(20)
        else:
            self.ln(20)

        # 2. Sidebar Contact Info
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 14)
        self.set_x(5)
        self.cell(60, 10, "CONTACT", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        contact_info = f"Phone: {data['phone']}\nEmail: {data['email']}\nLoc: {data['address']}"
        self.multi_cell(60, 6, contact_info)
        
        # 3. Personal Info
        self.ln(5)
        self.set_font("Arial", 'B', 14)
        self.set_x(5)
        self.cell(60, 10, "PERSONAL", ln=True)
        self.set_font("Arial", size=9)
        self.set_x(5)
        pers_info = f"DOB: {data['dob']}\nGender: {data['gender']}\nLang: {data['languages']}"
        self.multi_cell(60, 6, pers_info)

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

def create_pdf(data, color_theme, photo_file):
    pdf = UltimateResume()
    pdf.add_page()
    
    themes = {
        "Midnight Blue": (26, 35, 126), 
        "Charcoal Grey": (51, 51, 51), 
        "Deep Red": (139, 0, 0)
    }
    color = themes[color_theme]
    
    photo_path = None
    if photo_file:
        temp_dir = tempfile.gettempdir()
        photo_path = os.path.join(temp_dir, "temp_resume_photo.png")
        img = Image.open(photo_file)
        img.thumbnail((400, 400))
        img.save(photo_path)

    pdf.add_sidebar(color)
    pdf.add_content(data, color, photo_path)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- Streamlit UI ---
st.set_page_config(page_title="Ultimate Resume Maker", layout="wide")

st.sidebar.title("🎨 Design Studio")
theme = st.sidebar.selectbox("Choose Theme Color", ["Midnight Blue", "Charcoal Grey", "Deep Red"])
uploaded_photo = st.sidebar.file_uploader("Upload Profile Photo", type=['jpg', 'png', 'jpeg'])

st.title("📸 Professional AI Resume Builder")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📌 Personal Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    dob = st.text_input("DOB")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    languages = st.text_input("Languages", "Hindi, English, Marathi")

with col2:
    st.subheader("💼 Career & Education")
    summary = st.text_area("About Me", "B.Com student specializing in management.")
    skills = st.text_area("Skills", "Accounting\nTally\nAI")
    experience = st.text_area("Experience", "Managing Hotel Jay Malhar Operations")
    education = st.text_area("Education", "B.Com - University Name")

user_data = {
    'name': name, 'email': email, 'phone': phone, 'address': address, 
    'dob': dob, 'gender': gender, 'summary': summary, 
    'education': education, 'skills': skills, 'experience': experience, 'languages': languages
}

if st.button("🚀 Generate My Premium Resume"):
    if name and email:
        try:
            pdf_out = create_pdf(user_data, theme, uploaded_photo)
            st.balloons()
            st.download_button(label="📥 Download PDF", data=pdf_out, file_name=f"{name}_Resume.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Naam aur Email zaroori hai!")
