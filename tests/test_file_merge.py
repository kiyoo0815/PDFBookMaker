import tempfile
import unittest
from pathlib import Path

import fitz

from file_merge import merge_pdf


class FileMergeTest(unittest.TestCase):
    """PDF 병합 엔진의 주요 기능을 확인한다."""

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.test_folder = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def create_pdf(self, filename, label, page_count=1):
        """테스트에 사용할 간단한 PDF를 만든다."""

        pdf_path = self.test_folder / filename
        document = fitz.open()

        for page_index in range(page_count):
            page = document.new_page(width=595, height=842)
            page.insert_text(
                (72, 100),
                f"{label} {page_index + 1}"
            )

        document.save(pdf_path)
        document.close()

        return pdf_path

    def test_multiple_toc_pages_and_bookmarks(self):
        """24개 항목에서 목차가 두 페이지로 나뉘는지 확인한다."""

        pdf_list = []
        titles = []

        for index in range(24):
            pdf_path = self.create_pdf(
                f"input_{index + 1}.pdf",
                f"SOURCE_{index + 1}"
            )
            pdf_list.append(str(pdf_path))
            titles.append(f"Chapter {index + 1}")

        output_path = self.test_folder / "multiple_toc.pdf"
        merge_pdf(pdf_list, titles, "목차 테스트", str(output_path))

        with fitz.open(output_path) as result:
            self.assertEqual(result.page_count, 27)
            self.assertIn("Chapter 23", result[1].get_text())
            self.assertIn("Chapter 24", result[2].get_text())
            self.assertEqual(len(result.get_toc()), 24)
            self.assertEqual(result.get_toc()[0][2], 4)

    def test_progress_log_and_merge_order(self):
        """콜백과 사용자가 지정한 병합 순서를 확인한다."""

        first_pdf = self.create_pdf("first.pdf", "FIRST")
        second_pdf = self.create_pdf("second.pdf", "SECOND")
        output_path = self.test_folder / "ordered.pdf"
        progress_values = []
        log_messages = []

        merge_pdf(
            [str(second_pdf), str(first_pdf)],
            ["Second", "First"],
            "순서 테스트",
            str(output_path),
            progress_callback=progress_values.append,
            log_callback=log_messages.append
        )

        self.assertEqual(progress_values[0], 0)
        self.assertEqual(progress_values[-1], 100)
        self.assertEqual(progress_values, sorted(progress_values))
        self.assertIn("second.pdf", log_messages[4])

        with fitz.open(output_path) as result:
            self.assertIn("SECOND", result[2].get_text())
            self.assertIn("FIRST", result[3].get_text())

    def test_missing_input_file(self):
        """없는 입력 파일을 알기 쉬운 오류로 안내하는지 확인한다."""

        missing_path = self.test_folder / "missing.pdf"
        output_path = self.test_folder / "result.pdf"

        with self.assertRaisesRegex(
            FileNotFoundError,
            "PDF 파일을 찾을 수 없습니다"
        ):
            merge_pdf(
                [str(missing_path)],
                ["Missing"],
                "오류 테스트",
                str(output_path)
            )


if __name__ == "__main__":
    unittest.main()
