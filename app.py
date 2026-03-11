import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps
import tempfile
import os
from streamlit_pdf_viewer import pdf_viewer

# --- PDF Logic ---
class UltimateResume(FPDF):
    def add_page_border(self, color):
        self.set_draw_color(*color)
        self.set_line_width(1.0)
        self.rect(5, 5, 200, 287)

    def add_sidebar_stripe(self, color):
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

        # Contact & Skills (Left Stripe)
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

        # Main Content (Right Side)
        self.set_text_color(*color)
        self.set_xy(75, 20)
        self.set_font(font_to_use, 'B', 24)
        self.cell(130, 15, data.get('name', 'SONU SHARMA').upper(), ln=True)
        
        self.set_text_color(80, 80, 80)
        self.set_font(font_to_use, '', 10)
        self.set_x(75)
        self.multi_cell(120, 5, data.get('summary', ''))
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
    themes = {"Emerald Green": (0, 77, 64), "Royal Gold": (184, 134, 11), "Classic Black": (0, 0, 0), "Deep
