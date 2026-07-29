from pathlib import Path


def find_pdf_files(folder):

    folder = Path(folder)

    pdf_files = sorted(folder.glob("*.pdf"))

    return pdf_files