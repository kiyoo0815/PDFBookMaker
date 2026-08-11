from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont

from ui.utils.page_number_helper import calculate_position
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

class PreviewCanvas(QFrame):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(520)

        self.setStyleSheet("""
            background:white;
            border:1px solid #cccccc;
            border-radius:8px;
        """)

        self.position = 4
        self.page_number = "1"

        # 글꼴
        self.font_name = "맑은 고딕"
        self.font_size = 11

        # 여백
        self.horizontal_margin = 20
        self.vertical_margin = 20

        # 하이픈 사용
        self.use_dash = False

    def set_font(self, font_name):

        self.font_name = font_name
        self.update()

    def set_page_number(self, text):

        self.page_number = str(text)
        self.update()

    def set_position(self, position):
        self.position = position
        self.update()

    def set_font_size(self, size):

        self.font_size = size
        self.update()

    def set_margin(self, horizontal, vertical):

        self.horizontal_margin = horizontal
        self.vertical_margin = vertical
        self.update()

    def set_use_dash(self, use_dash):

        self.use_dash = use_dash
        self.update()

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setFont(
            QFont(
                self.font_name,
                self.font_size
            )
        )

        painter.setPen(QColor("#222222"))

        if self.use_dash:
            preview_text = f"-{self.page_number}-"
        else:
            preview_text = self.page_number

        x, y = calculate_position(
            width=self.width(),
            height=self.height(),
            position=self.position,
            text=preview_text,
            font=painter.font(),
            horizontal_margin=self.horizontal_margin,
            vertical_margin=self.vertical_margin,
        )

        painter.drawText(x, y, preview_text)

        if self.use_dash:
            text = f"-{self.page_number}-"
        else:
            text = self.page_number

        painter.drawText(x, y, text)

class PreviewWidget(QWidget):

    def update_page_number(self, data):

        self.page_number = data

        # 위치
        self.preview_canvas.set_position(
            data["even_position"]
        )

        # 글꼴 크기
        self.preview_canvas.set_font_size(
            data["font_size"]
        )

        # 여백
        self.preview_canvas.set_margin(
            data["horizontal_margin"],
            data["vertical_margin"]
        )

        # 시작번호
        self.preview_canvas.set_page_number(
            data["start_number"]
        )

        self.preview_canvas.set_use_dash(
            data["use_dash"]
        )

    def __init__(self):
        super().__init__()

        self.page_number = {}

        self.setFixedWidth(300)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # -------------------------
        # 미리보기 제목
        # -------------------------
        title = QLabel("미리보기")
        title.setStyleSheet("""
            font-size:14pt;
            font-weight:bold;
        """)

        main_layout.addWidget(title)

        self.preview_canvas = PreviewCanvas()

        main_layout.addWidget(self.preview_canvas)

        # -------------------------
        # 확대/축소
        # -------------------------
        zoom_layout = QHBoxLayout()

        zoom_out = QPushButton("－")
        zoom = QLabel("100%")
        zoom.setAlignment(Qt.AlignCenter)
        zoom_in = QPushButton("＋")

        zoom_layout.addWidget(zoom_out)
        zoom_layout.addWidget(zoom)
        zoom_layout.addWidget(zoom_in)

        main_layout.addLayout(zoom_layout)

        # -------------------------
        # 버튼
        # -------------------------
        button_layout = QHBoxLayout()

        close_button = QPushButton("닫기")

        button_layout.addStretch()
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

        close_button.clicked.connect(
            self.close_dialog
        )

    def close_dialog(self):

        parent = self.parent()

        while parent is not None:

            if isinstance(parent, QDialog):
                parent.close()
                return

            parent = parent.parent()