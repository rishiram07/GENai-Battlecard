import json
import os
from fpdf import FPDF
import re

# Define design templates
TEMPLATES = {
    'modern': {
        'font': 'Helvetica',
        'font_size': 10,
        'header_color': (0, 0, 0),  # Black text
        'bg_color': (0, 102, 204),  # Dark Blue background
        'section_color': (200, 200, 255),  # Light Blue sections
        'border_color': (0, 102, 204),  # Dark Blue border
        'border_width': 0.5,  # Border width for sections
    },
    'classic': {
        'font': 'Arial',
        'font_size': 11,
        'header_color': (0, 0, 0),  # Black text
        'bg_color': (255, 255, 255),  # White background
        'section_color': (255, 255, 255),  # White sections
        'border_color': (0, 0, 0),  # No border
        'border_width': 0,  # No border
    },
    'professional': {
        'font': 'Times',
        'font_size': 9,
        'header_color': (0, 0, 0),  # Black text
        'bg_color': (255, 255, 255),  # White background
        'section_color': (220, 220, 220),  # Light Gray sections
        'border_color': (200, 200, 200),  # Light Gray border
        'border_width': 0.5,  # Border width for sections
    }
}

# Function to fetch battlecard content
def fetch_battlecard_content(competitor):
    content = battlecards_data.get(competitor, "Content not found")
    return content

# Function to format text with simple HTML-like tags
def format_text(text):
    # Replace bold tags
    text = re.sub(r'<b>(.*?)</b>', r'\1', text)
    return text

# Function to create PDF for battlecard with a selected template
def create_battlecard_pdf(competitor, content, output_dir, template_name='classic'):
    template = TEMPLATES.get(template_name, TEMPLATES['classic'])
    
    class PDF(FPDF):
        def __init__(self, template, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.template = template

        def header(self):
            self.set_font(self.template['font'], 'B', 12)
            self.set_text_color(*self.template['header_color'])
            self.set_fill_color(*self.template['bg_color'])
            self.cell(0, 10, f'Battlecard - {competitor}', 0, 1, 'C', 1)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font(self.template['font'], 'I', 8)
            self.set_text_color(*self.template['header_color'])
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        def chapter_title(self, title):
            self.set_font(self.template['font'], 'B', 10)
            self.set_fill_color(*self.template['section_color'])
            self.set_text_color(*self.template['header_color'])
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(4)

        def chapter_body(self, body):
            self.set_font(self.template['font'], '', self.template['font_size'])
            self.set_text_color(*self.template['header_color'])
            body = format_text(body)  # Format text with tags
            self.multi_cell(0, 6, body)
            self.ln(4)

        def add_section_separator(self):
            self.set_y(self.get_y() + 5)
            if self.template['border_width'] > 0:
                self.set_draw_color(*self.template['border_color'])
                self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

    pdf = PDF(template)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Parse and split the content into sections
    sections = content.split("\n\n**")
    if sections[0].startswith("**"):
        sections[0] = sections[0][2:]

    # Add each section to the PDF
    for section in sections:
        if '**' in section:
            title, body = section.split('**', 1)
            title = title.strip()
            body = body.strip()

            pdf.add_section_separator()

            if title.lower() == "products":
                products = body.split("\n* ")
                top_5_products = products[:5]
                body = '\n'.join(f"* {product.strip('* ')}" for product in top_5_products)

            pdf.chapter_title(title)
            pdf.chapter_body(body)
    
    pdf_output_path = os.path.join(output_dir, f"{competitor}_battlecard.pdf")
    pdf.output(pdf_output_path)

# Function to save content as a .txt file
def save_battlecard_txt(competitor, content, output_dir):
    txt_output_path = os.path.join(output_dir, f"{competitor}_battlecard.txt")
    try:
        with open(txt_output_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing to file {txt_output_path}: {e}")

# Main function to handle battlecard design
def design_battlecards(template_name='classic'):
    output_dir = 'battlecards'
    os.makedirs(output_dir, exist_ok=True)

    # Load battlecards data
    try:
        with open('battlecards.json', 'r') as file:
            global battlecards_data
            battlecards_data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading battlecards data: {e}")
        return
    
    # Process each competitor and create PDFs and text files
    for competitor in battlecards_data:
        content = fetch_battlecard_content(competitor)
        create_battlecard_pdf(competitor, content, output_dir, template_name=template_name)
        save_battlecard_txt(competitor, content, output_dir)

if __name__ == "__main__":
    design_battlecards()