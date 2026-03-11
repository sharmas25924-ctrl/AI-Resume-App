import streamlit as st
from fpdf import FPDF

# --- PDF Generation Function ---
def create_pdf(name, email, phone, linkedin, summary, education, skills, experience, languages):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(200, 10, txt=name, ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 7, txt=f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.cell(200, 7, txt=f"LinkedIn: {linkedin}", ln=True, align='C')
    pdf.ln(5)
    pdf.line(10, 35, 200, 35)
    pdf.ln(5)

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

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Maker", layout="centered")

st.title("📄 Pro AI Resume Builder")

with st.expander("👤 Personal Details", expanded=True):
    name = st.text_input("Full Name", "Sonu Sharma")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email ID")
    with col2:
        phone = st.text_input("Mobile Number")
    linkedin = st.text_input("LinkedIn Profile Link")

with st.expander("📝 Summary & Education"):
    summary = st.text_area("Summary", "B.Com student with experience in business management.")
    education = st.text_area("Education", "B.Com - [College Name]\nSSC/HSC - [School Name]")

with st.expander("🛠 Skills & Experience"):
    skills = st.text_area("Skills", "Accounting, Tally, AI Tools")
    experience = st.text_area("Experience", "Hotel Jay Malhar Management")
    languages = st.text_input("Languages", "Hindi, English")

if st.button("Generate & Download PDF"):
    if not name or not email:
        st.error("Naam aur Email bharna zaruri hai!")
    else:
        try:
            pdf_bytes = create_pdf(name, email, phone, linkedin, summary, education, skills, experience, languages)
            st.success("✅ Resume Taiyar Hai!")
            st.download_button(
                label="📥 Download Resume PDF",
                data=pdf_bytes,
                file_name=f"{name}_Resume.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Ek galti hui: {e}")
