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

        # 테스트용 페이지 번호 기본 설정
        self.page_number_settings = {
            "same_position": True,
            "even_position": 4,
            "odd_position": 4,
            "font_size": 10,
            "start_number": 1,
            "horizontal_margin": 15,
            "vertical_margin": 15,
            "use_dash": False,
        }

        # 테스트용 표지 기본 설정
        self.cover_settings = {
            "title": "테스트 제목",
            "title_size": 30,
            "title_align": "가운데",
            "title_y": 220,

            "subtitle": "",
            "subtitle_size": 18,
            "subtitle_align": "가운데",
            "subtitle_y": 270,

            "items": [],
            "info_size": 12,
            "info_align": "왼쪽",
            "info_y": 500,
            "info_spacing": 28,

            "image_path": "",
            "image_size": 100,
            "image_y": 20,
            "image_align": "가운데",
        }

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

    def make_toc_items(self, pdf_list, titles):
        """현재 병합 엔진 형식에 맞는 목차 정보를 만든다."""

        return [
            {
                "type": "pdf",
                "path": pdf_path,
                "title": title,
            }
            for pdf_path, title in zip(pdf_list, titles)
        ]

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

        toc_items = self.make_toc_items(
            pdf_list,
            titles
        )

        output_path = self.test_folder / "multiple_toc.pdf"

        merge_pdf(
            toc_items,
            "목차 테스트",
            str(output_path),
            self.page_number_settings,
            self.cover_settings,
        )

        with fitz.open(output_path) as result:
            # 표지 1 + 목차 2 + 본문 24 = 27
            self.assertEqual(result.page_count, 27)

            self.assertIn(
                "Chapter 23",
                result[2].get_text()
            )

            self.assertIn(
                "Chapter 24",
                result[2].get_text()
            )

            self.assertEqual(
                len(result.get_toc()),
                24
            )

            # 첫 번째 본문은 PDF 전체의 4페이지
            self.assertEqual(
                result.get_toc()[0][2],
                4
            )

    def test_progress_log_and_merge_order(self):
        """콜백과 사용자가 지정한 병합 순서를 확인한다."""

        first_pdf = self.create_pdf(
            "first.pdf",
            "FIRST"
        )

        second_pdf = self.create_pdf(
            "second.pdf",
            "SECOND"
        )

        pdf_list = [
            str(second_pdf),
            str(first_pdf),
        ]

        titles = [
            "Second",
            "First",
        ]

        toc_items = self.make_toc_items(
            pdf_list,
            titles
        )

        output_path = self.test_folder / "ordered.pdf"

        progress_values = []
        log_messages = []

        merge_pdf(
            toc_items,
            "순서 테스트",
            str(output_path),
            self.page_number_settings,
            self.cover_settings,
            progress_callback=progress_values.append,
            log_callback=log_messages.append,
        )

        self.assertEqual(
            progress_values[0],
            0
        )

        self.assertEqual(
            progress_values[-1],
            100
        )

        self.assertEqual(
            progress_values,
            sorted(progress_values)
        )

        self.assertTrue(
            any(
                "second.pdf" in message
                for message in log_messages
            )
        )

        with fitz.open(output_path) as result:
            # 표지 1 + 목차 1 다음부터 본문
            self.assertIn(
                "SECOND",
                result[2].get_text()
            )

            self.assertIn(
                "FIRST",
                result[3].get_text()
            )

    def test_missing_input_file(self):
        """없는 입력 파일을 알기 쉬운 오류로 안내하는지 확인한다."""

        missing_path = self.test_folder / "missing.pdf"
        output_path = self.test_folder / "result.pdf"

        toc_items = [
            {
                "type": "pdf",
                "path": str(missing_path),
                "title": "Missing",
            }
        ]

        with self.assertRaisesRegex(
            FileNotFoundError,
            "PDF 파일을 찾을 수 없습니다"
        ):
            merge_pdf(
                toc_items,
                "오류 테스트",
                str(output_path),
                self.page_number_settings,
                self.cover_settings,
            )


if __name__ == "__main__":
    unittest.main()