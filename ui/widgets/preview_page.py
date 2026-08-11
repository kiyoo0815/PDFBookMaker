from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QWidget


class PreviewPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(220, 520)

        # 현재 페이지 번호 위치
        self.even_position = 4
        self.odd_position = 4

    # -----------------------------
    # 위치 변경
    # -----------------------------
    def set_page_number_position(self, even, odd):

        self.even_position = even
        self.odd_position = odd

        self.update()

    # -----------------------------
    # 그리기
    # -----------------------------
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 배경
        painter.fillRect(self.rect(), Qt.white)

        # 종이
        paper = QRect(10, 10, self.width()-20, self.height()-20)

        painter.setPen(QPen(QColor("#CCCCCC"), 1))
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(paper, 8, 8)

        # A4 표시
        painter.setPen(QColor("#BBBBBB"))
        painter.setFont(QFont("맑은 고딕", 24))

        painter.drawText(
            paper,
            Qt.AlignCenter,
            "A4"
        )