from pypdf import PdfReader


def extract_text_from_pdf(pdf_file_path: str) -> str:
    pdf_reader = PdfReader(pdf_file_path)
    # Extraire le texte de toutes les pages du PDF
    all_text = ""
    for page_num, page in enumerate(pdf_reader.pages):
        all_text += f"--- Page {page_num + 1} ---\n"
        all_text += page.extract_text() or "Aucun texte extrait\n"
        all_text += "\n\n"
    return all_text
