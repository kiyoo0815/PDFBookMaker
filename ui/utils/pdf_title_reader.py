import fitz
import re


import fitz


def extract_pdf_info(pdf_path):

    try:

        doc = fitz.open(pdf_path)

        page = doc[0]

        page_height = page.rect.height

        blocks = page.get_text("blocks")

        lines = []

        for block in blocks:

            x0, y0, x1, y1, text, *_ = block

            # -------------------------
            # 머리글 제거
            # -------------------------
            if y0 < 80:
                continue

            # -------------------------
            # 페이지 번호 제거
            # -------------------------
            if y1 > page_height - 80:
                continue

            for line in text.splitlines():

                line = line.strip()

                if line:
                    lines.append(line)

        doc.close()

        chapter = ""
        lesson = ""

        if len(lines) >= 1:
            chapter = lines[0]

        if len(lines) >= 2:
            lesson = lines[1]

        return chapter, lesson

    except Exception as e:

        print(e)

        return "", ""