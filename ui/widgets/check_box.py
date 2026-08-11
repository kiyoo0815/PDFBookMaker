from PySide6.QtCore import Qt, QRect, QSize, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QWidget


class CheckBox(QWidget):

    toggled = Signal(bool)

    def __init__(self, text="", checked=False):
        super().__init__()

        self.text = text
        self.checked = checked

        self.setFixedHeight(28)

        self.setCursor(Qt.PointingHandCursor)

    # -----------------------------
    # 상태 확인
    # -----------------------------
    def isChecked(self):
        return self.checked

    # -----------------------------
    # 상태 변경
    # -----------------------------
    def setChecked(self, checked):

        if self.checked == checked:
            return

        self.checked = checked
        self.update()

        self.toggled.emit(self.checked)

    # -----------------------------
    # 클릭
    # -----------------------------
    def mousePressEvent(self, event):

        self.setChecked(not self.checked)

    # -----------------------------
    # 크기
    # -----------------------------
    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(220, 28)

    # -----------------------------
    # 그리기
    # -----------------------------
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # □
        box = QRect(2, 5, 18, 18)

        painter.setBrush(Qt.white)
        painter.setPen(QPen(QColor("#666666"), 1))
        painter.drawRoundedRect(box, 3, 3)

        # ✔
        if self.checked:

            painter.setPen(QPen(QColor("#2F80ED"), 2))

            painter.drawLine(6, 14, 10, 18)
            painter.drawLine(10, 18, 17, 9)

        # 글자
        painter.setPen(Qt.black)
        painter.setFont(QFont("맑은 고딕", 10))

        painter.drawText(
            QRect(28, 0, self.width() - 30, self.height()),
            Qt.AlignVCenter,
            self.text
        )