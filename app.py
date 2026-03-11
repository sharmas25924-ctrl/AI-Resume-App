import streamlit as st
from fpdf import FPDF

# --- PDF Design Function ---
def create_pdf(name, email, phone, skills, experience):
    pdf = FPDF()
    pdf.add_page()
    
    # Border
    pdf.rect(5, 5, 200, 287)
    
    # Header: Name
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(0, 51, 102) # Dark Blue
    pdf.cell(200, 15, txt=name, ln=True, align='C')
    
    # Contact Info
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.ln(10)

    # Line separator
    pdf.line(10, 40, 200, 40)
    pdf.ln(5)

    # Section: Skills
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="TECHNICAL & SOFT SKILLS", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt=skills)
    pdf.ln(5)

    # Section: Experience
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="WORK EXPERIENCE & PROJECTS", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt=experience)

    return pdf.output(dest='S').encode('latin-1')

# --- UI Layout ---
st.set_page_config(page_title="AI Resume Pro", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Professional AI Resume Builder")
st.info("B.Com Students aur Business Owners ke liye khaas design!")

# Two column layout for input
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Aapka Pura Naam", "Sonu Sharma")
        email = st.text_input("Email ID", "sonu@example.com")
    with col2:
        phone = st.text_input("Mobile Number", "+91 0000000000")
        degree = st.text_input("Education/Degree", "B.Com")

    skills = st.text_area("Skills (Example: Accounting, Tally, AI, Management)")
    experience = st.text_area("Experience (Example: Hotel Jay Malhar Management, College Projects)")

# Action Button
if st.button("Generate & Download My Resume"):
    if not name or not email:
        st.warning("Kripya Naam aur Email zarur bharein!")
    else:
        pdf_bytes = create_pdf(name, email, phone, skills, experience)
        st.success("✅ Aapka professional resume taiyar hai!")
        
        st.download_button(
            label="📥 Download PDF Now",
            data=pdf_bytes,
            file_name=f"{name}_Professional_Resume.pdf",
            mime="application/pdf"
        )