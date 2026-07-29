import fitz


def merge_pdf(pdf_list, output_file):

    print("PDF 병합 시작")

    # 새 PDF 생성
    merged = fitz.open()

    # 선택한 PDF를 순서대로 추가
    for pdf in pdf_list:

        doc = fitz.open(pdf)
        merged.insert_pdf(doc)
        doc.close()

    # 저장
    merged.save(output_file)
    merged.close()

    print(f"저장 완료 : {output_file}")