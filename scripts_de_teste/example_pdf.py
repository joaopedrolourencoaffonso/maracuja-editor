from fpdf import FPDF

# Your markdown string
markdown_string = """
<h1>Project Report</h1>

<p>This is a **Markdown string** converted directly to PDF using **fpdf2**.</p>

## Key Features
* Zero system dependencies
* Fast implementation
* Supports *italics*, **bold**, and [links](https://pyfpdf.github.io/fpdf2/)

### Code Summary
The built-in `write_html` method renders basic Markdown directly!
"""

class MarkdownPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Generated via fpdf2", border=0, new_x="LMARGIN", new_y="NEXT", align="R")
        self.ln(5)

# Initialize PDF
pdf = MarkdownPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=11)

# Render Markdown string directly
pdf.write_html(markdown_string)

# Save to file
pdf.output("markdown_output.pdf")
print("PDF created successfully: markdown_output.pdf")