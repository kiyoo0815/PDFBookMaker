from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class ToggleSwitch(QWidget):

    toggled = Signal(bool)

    def __init__(self, checked=True):
        super().__init__()

        self.checked = checked

        self.setFixedSize(46, 24)

    # --------------------------
    # 현재 상태
    # --------------------------
    def isChecked(self):
        return self.checked

    # --------------------------
    # 상태 변경
    # --------------------------
    def setChecked(self, checked):

        if self.checked == checked:
            return

        self.checked = checked
        self.update()

        self.toggled.emit(self.checked)

    # --------------------------
    # 마우스 클릭
    # --------------------------
    def mousePressEvent(self, event):

        self.setChecked(not self.checked)

    # --------------------------
    # 그리기
    # --------------------------
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ON 색상
        if self.checked:
            bg = QColor("#2F80ED")
            x = 24

        # OFF 색상
        else:
            bg = QColor("#C8CDD5")
            x = 2

        # 배경
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(
            QRectF(0, 0, 46, 24),
            12,
            12
        )

        # 버튼
        painter.setBrush(Qt.white)
        painter.drawEllipse(
            QRectF(x, 2, 20, 20)
        )