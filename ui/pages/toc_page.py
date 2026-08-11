from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class TocPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("📑 목차 설정")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)
        layout.addStretch()