from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget


class PositionSelector(QWidget):

    positionChanged = Signal(int)

    def __init__(self, title="짝수 페이지"):
        super().__init__()

        self.title = title

        # 위젯 전체 크기
        self.setFixedSize(180, 260)

        # 선택된 버튼 번호
        # 0 1 2
        # 3 4 5

        self.selected = 4      # 기본 : 아래 가운데

        # 종이 위치
        self.paper = QRect(25, 25, 130, 190)

        # 위치 선택점 좌표 (종이 안쪽)
        self.points = [
            (48, 48),    # 좌상
            (90, 48),    # 상단 중앙
            (132, 48),   # 우상

            (48, 174),   # 좌하
            (90, 174),   # 하단 중앙
            (132, 174),  # 우하
        ]

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ==========================
        # 종이
        # ==========================
        painter.setBrush(Qt.white)
        painter.setPen(QPen(QColor("#888888"), 2))
        painter.drawRoundedRect(self.paper, 4, 4)

        # ==========================
        # 제목
        # ==========================
        painter.setPen(Qt.black)
        painter.setFont(QFont("맑은 고딕", 10, QFont.Bold))

        painter.drawText(
            QRect(
                self.paper.left(),
                self.paper.top() + 78,
                self.paper.width(),
                25
            ),
            Qt.AlignCenter,
            self.title
        )
        # ==========================
        # 위치 선택 버튼
        # ==========================
        for i, (x, y) in enumerate(self.points):

            if i == self.selected:
                painter.setBrush(QColor("#2F80ED"))
                painter.setPen(QPen(QColor("#2F80ED"), 2))
            else:
                painter.setBrush(Qt.white)
                painter.setPen(QPen(QColor("#999999"), 2))

            painter.drawEllipse(x, y, 14, 14)

    def mousePressEvent(self, event):

        click_x = event.position().x()
        click_y = event.position().y()

        for i, (x, y) in enumerate(self.points):

            # 버튼 크기(14×14)
            if x <= click_x <= x + 14 and y <= click_y <= y + 14:

                self.set_selected(i, emit_signal=True)

                return

    def showEvent(self, event):
        super().showEvent(event)
        self.update()

    def set_selected(self, index, emit_signal=False):
        """
        선택 위치 변경

        emit_signal=False : 프로그램이 변경
        emit_signal=True  : 사용자 클릭처럼 Signal도 발생
        """

        if self.selected == index:
            return

        self.selected = index
        self.update()

        if emit_signal:
            self.positionChanged.emit(index)