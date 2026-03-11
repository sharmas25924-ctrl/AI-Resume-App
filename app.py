import streamlit as st
from fpdf import FPDF

def create_pdf(name, email, phone, linkedin, summary, education, skills, experience, languages):
    pdf = FPDF()
    pdf.add_page()
    
    # Header: Name
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(200, 10, txt=name, ln=True, align='C')
    
    # Contact Info
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 7, txt=f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.cell(200, 7, txt=f"LinkedIn: {linkedin}", ln=True, align='C')
    pdf.ln(5)
    pdf.line(10, 35, 200, 35)
    pdf.ln(5)

    # Sections Function
    def add_section(title, content):
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 8, txt=title, ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)
        pdf.multi_cell(0, 7, txt=content)
        pdf.ln(4)

    add_section("PROFESSIONAL SUMMARY", summary)
    add_section("EDUCATION", education)
    add_section("TECHNICAL & SOFT SKILLS", skills)
    add_section("EXPERIENCE & PROJECTS", experience)
    add_section("LANGUAGES", languages)

    return pdf.output(dest='S').encode('latin-1')

# --- UI Setup ---
st.set_page_config(page_title="Pro AI Resume Maker", layout="centered")

st.title("📄 Pro AI Resume Builder")
st.write("Professional details bharein aur apna resume download karein.")

# Input Sections
with st.expander("👤 Personal & Contact Details", expanded=True):
    name = st.text_input("Full Name", "Sonu Sharma")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email ID")
        phone = st.text_input("Mobile Number")
    with col2:
        linkedin = st.text_input("LinkedIn Profile Link")

with st.expander("📝 Summary & Education"):
    summary = st.text_area("Professional Summary", "B.Com student with experience in business management and digital art.")
    education = st.text_area("Education Details", "B.Com - [College Name], [Passing Year]\nSSC/HSC - [School Name], [Percentage]")

with st.expander("🛠 Skills & Experience"):
    skills = st.text_area("Skills", "Accounting, Tally Prime, AI Prompt Engineering, Social Media Branding")
    experience = st.text_area("Experience/Projects", "1. Hotel Jay Malhar: Managing operations and branding.\n2. Digital Art: Creating cinematic posters.")
    languages = st.text_input("Languages Known", "Hindi, English, Marathi")

# Button
if st.button("Preview & Download PDF"):
    if not name or not email:
        st.error("Naam aur Email bharna zaruri hai!")
    else:
        pdf_bytes = create_pdf(name, email, phone, linkedin, summary, education, skills, experience, languages)
        st.success("Aapka Full Professional Resume taiyar hai!")
        st.download_button(
            label="📥 Download My Professional Resume",
            data=pdf_bytes,
            file_name=f"{name}_Resume_Pro.pdf",
            mime="application/pdf"
        )
        )
