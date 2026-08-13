import fitz

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QFont,
    QColor,
    QImage,
    QPixmap,
)
from PySide6.QtWidgets import QFrame


class PageNumberPreviewWidget(QFrame):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(320, 450)

        # -------------------------
        # 페이지 번호 기본 설정
        # -------------------------
        self.same_position = True

        self.even_position = 5
        self.odd_position = 5

        self.font_size = 14
        self.start_number = 1

        self.horizontal_margin = 15
        self.vertical_margin = 15

        self.use_dash = False

        # -------------------------
        # 실제 PDF 미리보기
        # -------------------------
        self.pdf_preview = None

        # 실제 PDF 페이지 크기(pt)
        self.pdf_width = 595
        self.pdf_height = 842

        self.setStyleSheet("""
            background: white;
            border: 1px solid #cccccc;
            border-radius: 8px;
        """)

    def set_settings(self, data):
        """페이지 번호 설정값을 미리보기에 적용"""

        self.same_position = data["same_position"]

        self.even_position = data["even_position"]
        self.odd_position = data["odd_position"]

        self.font_size = data["font_size"]
        self.start_number = data["start_number"]

        self.horizontal_margin = data["horizontal_margin"]
        self.vertical_margin = data["vertical_margin"]

        self.use_dash = data["use_dash"]

        self.update()

    def set_pdf(self, pdf_path):
        """PDF 첫 페이지를 미리보기 이미지로 만든다."""

        document = None

        try:
            document = fitz.open(pdf_path)

            if document.page_count == 0:
                self.pdf_preview = None
                self.update()
                return

            page = document[0]

            # 실제 PDF 페이지 크기 저장
            self.pdf_width = page.rect.width
            self.pdf_height = page.rect.height

            # PDF 첫 페이지를 이미지로 변환
            pix = page.get_pixmap(
                matrix=fitz.Matrix(1.5, 1.5),
                alpha=False
            )

            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format_RGB888
            )

            # PyMuPDF 메모리와 분리
            self.pdf_preview = QPixmap.fromImage(
                image.copy()
            )

        except Exception as error:

            print(
                f"PDF 미리보기 생성 오류: {error}"
            )

            self.pdf_preview = None

        finally:

            if document is not None:
                document.close()

        self.update()

    def mm_to_pt(self, mm):
        """밀리미터(mm)를 PDF 포인트(pt)로 변환"""

        return mm * 72 / 25.4

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # -------------------------
        # PDF 미리보기 영역 계산
        # -------------------------
        if self.pdf_preview:

            scaled = self.pdf_preview.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            pdf_x = (
                self.width() - scaled.width()
            ) / 2

            pdf_y = (
                self.height() - scaled.height()
            ) / 2

            pdf_display_width = scaled.width()
            pdf_display_height = scaled.height()

            painter.drawPixmap(
                int(pdf_x),
                int(pdf_y),
                scaled
            )

        else:

            # PDF가 없을 때는 위젯 전체를 페이지로 사용
            pdf_x = 0
            pdf_y = 0

            pdf_display_width = self.width()
            pdf_display_height = self.height()

        # -------------------------
        # 페이지 번호 문자열
        # -------------------------
        if self.use_dash:
            text = f"-{self.start_number}-"
        else:
            text = str(self.start_number)

        # 미리보기에서는 첫 번째 본문 페이지,
        # 즉 홀수 페이지 설정을 표시
        position = self.odd_position

        # -------------------------
        # mm → PDF point
        # -------------------------
        h_margin_pt = self.mm_to_pt(
            self.horizontal_margin
        )

        v_margin_pt = self.mm_to_pt(
            self.vertical_margin
        )

        # -------------------------
        # 실제 PDF 기준 글자 크기 계산
        # -------------------------
        text_width_pt = (
            len(text)
            * self.font_size
            * 0.55
        )

        # -------------------------
        # 실제 PDF 기준 X 좌표
        # -------------------------
        if position in (0, 3):

            x_pt = h_margin_pt

        elif position in (1, 4):

            x_pt = (
                self.pdf_width
                - text_width_pt
            ) / 2

        else:

            x_pt = (
                self.pdf_width
                - h_margin_pt
                - text_width_pt
            )

        # -------------------------
        # 실제 PDF 기준 Y 좌표
        # -------------------------
        if position in (0, 1, 2):

            # 실제 file_merge.py와 같은 계산
            baseline_y_pt = (
                v_margin_pt
                + self.font_size
            )

        else:

            # 실제 file_merge.py와 같은 계산
            baseline_y_pt = (
                self.pdf_height
                - v_margin_pt
            )

        # -------------------------
        # 실제 PDF 좌표 → 미리보기 좌표
        # -------------------------
        scale_x = (
            pdf_display_width
            / self.pdf_width
        )

        scale_y = (
            pdf_display_height
            / self.pdf_height
        )

        x = (
            pdf_x
            + x_pt * scale_x
        )

        baseline_y = (
            pdf_y
            + baseline_y_pt * scale_y
        )

        # -------------------------
        # 미리보기 글꼴 크기
        # -------------------------
        preview_font_size = max(
            1,
            int(self.font_size * scale_y)
        )

        painter.setPen(
            QColor("#222222")
        )

        font = QFont(
            "맑은 고딕"
        )

        font.setPixelSize(
            preview_font_size
        )

        painter.setFont(font)

        # -------------------------
        # 페이지 번호 출력
        #
        # 실제 PDF의 insert_text()처럼
        # x, y를 글자의 기준선으로 사용
        # -------------------------
        painter.drawText(
            int(x),
            int(baseline_y),
            text
        )