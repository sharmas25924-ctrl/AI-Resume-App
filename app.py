import streamlit as st
from fpdf import FPDF

# --- Modern PDF Class ---
class ModernResume(FPDF):
    def add_modern_header(self, name, email, phone, linkedin, address, color):
        self.set_fill_color(*color)
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 24)
        self.cell(0, 15, name.upper(), ln=True, align='C')
        self.set_font("Arial", size=10)
        self.cell(0, 5, f"{email}  |  {phone}  |  {address}", ln=True, align='C')
        self.cell(0, 5, f"LinkedIn: {linkedin}", ln=True, align='C')
        self.ln(15)

    def add_section_title(self, title, color):
        self.set_font("Arial", 'B', 12)
        self.set_text_color(*color)
        self.cell(0, 10, title, ln=True)
        self.set_draw_color(*color)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(2)

def create_pdf(name, email, phone, address, dob, gender, linkedin, summary, education, skills, experience, languages, template_choice):
    pdf = ModernResume()
    pdf.add_page()
    
    # Color Themes
    colors = {
        "Modern Dark": (44, 62, 80),
        "Royal Blue": (0, 51, 102),
        "Wine Red": (128, 0, 0)
    }
    selected_color = colors[template_choice]

    # Header
    pdf.add_modern_header(name, email, phone, linkedin, address, selected_color)
    
    # Reset Text Color for Body
    pdf.set_text_color(0, 0, 0)

    # Professional Summary
    pdf.add_section_title("PROFESSIONAL SUMMARY", selected_color)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, summary)
    pdf.ln(5)

    # Education & Personal
    col_width = 90
    pdf.add_section_title("EDUCATION & PERSONAL", selected_color)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(col_width, 7, "Education History:")
    pdf.cell(col_width, 7, "Personal Details:")
    pdf.ln(7)
    
    pdf.set_font("Arial", size=10)
    # Using a simple trick for two-column look in FPDF
    top_y = pdf.get_y()
    pdf.multi_cell(col_width, 6, education)
    pdf.set_xy(110, top_y)
    pdf.multi_cell(col_width, 6, f"DOB: {dob}\nGender: {gender}\nLanguages: {languages}")
    pdf.ln(10)

    # Experience
    pdf.set_xy(10, pdf.get_y() + 5)
    pdf.add_section_title("EXPERIENCE & PROJECTS", selected_color)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, experience)
    pdf.ln(5)

    # Skills
    pdf.add_section_title("KEY SKILLS", selected_color)
    pdf.set_font("Arial", 'B', 11)
    pdf.multi_cell(0, 7, skills)

    return pdf.output(dest='S').encode('latin-1')

# --- Streamlit UI ---
st.set_page_config(page_title="Modern Resume AI", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🚀 Modern AI Resume Builder</h1>", unsafe_allow_html=True)

# Sidebar Design Options
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=100)
st.sidebar.title("Design Gallery")
template_choice = st.sidebar.select_slider("Choose Your Vibe:", options=["Modern Dark", "Royal Blue", "Wine Red"])

# Input Forms
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("👤 Personal Details")
    name = st.text_input("Full Name", "Sonu Sharma")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    dob = st.text_input("DOB (e.g. 15 Aug 2002)")
    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    linkedin = st.text_input("LinkedIn Profile URL")

with col2:
    st.subheader("💼 Career Details")
    summary = st.text_area("Professional Summary", placeholder="Apne baare mein 2 line likhein...")
    education = st.text_area("Education", placeholder="B.Com, University Name, Year")
    experience = st.text_area("Experience", placeholder="Hotel Jay Malhar Management, etc.")
    skills = st.text_area("Skills", placeholder="Tally, AI, Management")
    languages = st.text_input("Languages", "Hindi, English")

st.divider()

if st.button(f"✨ Generate {template_choice} Resume"):
    if not name or not email:
        st.error("Naam aur Email zaroori hai!")
    else:
        pdf_bytes = create_pdf(name, email, phone, address, dob, gender, linkedin, summary, education, skills, experience, languages, template_choice)
        st.balloons()
        st.download_button(label="📥 Download Modern PDF", data=pdf_bytes, file_name=f"{name}_Modern_Resume.pdf", mime="application/pdf")
