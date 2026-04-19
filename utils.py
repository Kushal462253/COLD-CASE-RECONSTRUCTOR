from fpdf import FPDF
import os

class CaseReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(201, 168, 76)
        self.cell(0, 10, "COLD CASE RECONSTRUCTOR", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "AI-Powered Investigative Intelligence System", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_draw_color(201, 168, 76)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(201, 168, 76)
        self.cell(0, 8, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(201, 168, 76)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(200, 200, 200)
        clean = text.encode("latin-1", "replace").decode("latin-1")
        self.multi_cell(0, 5, clean)
        self.ln(3)


def generate_pdf(case_input, result):
    pdf = CaseReportPDF()
    pdf.set_margins(10, 15, 10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_fill_color(10, 10, 10)
    pdf.add_page()

    # Case title
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "CASE FILE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(180, 180, 180)
    clean_input = case_input.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 6, clean_input)
    pdf.ln(5)

    # Retrieved facts
    pdf.section_title("Retrieved Intelligence")
    pdf.body_text(result["retrieved_facts"])

    # Theories
    pdf.section_title("Reconstructed Theories")
    theories_list = result.get("theories_list", [])
    if theories_list:
        for i, theory in enumerate(theories_list):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 7, f"Theory {i+1}", new_x="LMARGIN", new_y="NEXT")
            pdf.body_text(theory)
    else:
        pdf.body_text(result["theories"])

    # Evidence
    pdf.section_title("Evidence Mapping")
    evidence_list = result.get("evidence_list", [])
    if evidence_list:
        for i, evidence in enumerate(evidence_list):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 7, f"Evidence - Theory {i+1}", new_x="LMARGIN", new_y="NEXT")
            pdf.body_text(evidence)
    else:
        pdf.body_text(result["evidence"])

    # Scores
    pdf.section_title("Consistency Scores")
    scores = result["scores"]
    for theory, score in scores.items():
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(201, 168, 76)
        label = theory.replace("_", " ").upper()
        pdf.cell(0, 6, f"{label}: {score}/100", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Narratives
    pdf.section_title("Investigative Narratives")
    narratives_list = result.get("narratives_list", [])
    if narratives_list:
        for i, narrative in enumerate(narratives_list):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 7, f"Narrative - Theory {i+1}", new_x="LMARGIN", new_y="NEXT")
            pdf.body_text(narrative)
    else:
        pdf.body_text(result["narratives"])

    # Verdict
    pdf.section_title("Final Verdict")
    pdf.body_text(result["verdict"])

    # Save to bytes
    pdf_bytes = pdf.output()
    return bytes(pdf_bytes)