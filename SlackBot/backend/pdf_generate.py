from fpdf import FPDF
import os

def generate_pdf(results, output_path="report.pdf"):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Use default Arial font
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, "Content Generation Report", ln=True, align="C")
    pdf.ln(5)

    for item in results:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Group {item['group']}", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 7, f"Keywords: {', '.join(item['keywords'])}")
        pdf.ln(2)

        pdf.multi_cell(0, 7, f"Post Idea: {item['post_idea']}")
        pdf.ln(2)

        pdf.multi_cell(0, 7, f"Outline:\n{item['outline']}")
        pdf.ln(5)

    pdf.output(output_path)
    return os.path.abspath(output_path)
