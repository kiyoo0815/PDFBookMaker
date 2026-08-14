from ui.widgets.check_box import CheckBox
from ui.widgets.position_selector import PositionSelector
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
)


class PageNumberPage(QWidget):

    previewChanged = Signal(dict)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # -----------------------------
        # 제목
        # -----------------------------
        title = QLabel("# 페이지 번호")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        layout.addWidget(title)

        # -----------------------------
        # 동일 적용
        # -----------------------------
        self.same_position = CheckBox("짝수/홀수 동일하게 적용", True)
        self.same_position.toggled.connect(self.same_position_changed)

        layout.addWidget(self.same_position)

        # -----------------------------
        # PositionSelector
        # -----------------------------

        selector_layout = QHBoxLayout()

        selector_layout.setSpacing(30)
        selector_layout.setAlignment(Qt.AlignLeft)

        self.even_selector = PositionSelector("짝수 페이지")
        self.odd_selector = PositionSelector("홀수 페이지")

        # 기본 위치 : 오른쪽 아래
        self.even_selector.set_selected(5, emit_signal=False)
        self.odd_selector.set_selected(5, emit_signal=False)

        self.even_selector.positionChanged.connect(self.even_position_changed)
        self.odd_selector.positionChanged.connect(self.odd_position_changed)

        selector_layout.addWidget(self.even_selector)
        selector_layout.addWidget(self.odd_selector)

        layout.addLayout(selector_layout)

        # -----------------------------
        # 글꼴 크기
        # -----------------------------
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("크기"))

        self.font_size = QSpinBox()
        self.font_size.setRange(6, 72)
        self.font_size.setValue(14)

        size_layout.addWidget(self.font_size)
        layout.addLayout(size_layout)

        # -----------------------------
        # 시작 번호
        # -----------------------------
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("시작 번호"))

        self.start_number = QSpinBox()
        self.start_number.setRange(1, 9999)
        self.start_number.setValue(1)

        start_layout.addWidget(self.start_number)
        layout.addLayout(start_layout)

        # -----------------------------
        # 가로 여백
        # -----------------------------
        h_margin_layout = QHBoxLayout()
        h_margin_layout.addWidget(QLabel("가로 여백"))

        self.h_margin = QSpinBox()
        self.h_margin.setRange(0, 100)
        self.h_margin.setValue(15)

        h_margin_layout.addWidget(self.h_margin)
        h_margin_layout.addWidget(QLabel("mm"))

        layout.addLayout(h_margin_layout)

        # -----------------------------
        # 세로 여백
        # -----------------------------
        v_margin_layout = QHBoxLayout()
        v_margin_layout.addWidget(QLabel("세로 여백"))

        self.v_margin = QSpinBox()
        self.v_margin.setRange(0, 100)
        self.v_margin.setValue(15)

        v_margin_layout.addWidget(self.v_margin)
        v_margin_layout.addWidget(QLabel("mm"))

        layout.addLayout(v_margin_layout)

        # -----------------------------
        # 페이지 번호 형식
        # -----------------------------
        self.use_dash = CheckBox(
            "하이픈(-) 사용",
            False
        )

        self.use_dash.toggled.connect(
            self.update_preview
        )

        layout.addWidget(self.use_dash)

        self.font_size.valueChanged.connect(self.update_preview)

        self.start_number.valueChanged.connect(self.update_preview)

        self.h_margin.valueChanged.connect(self.update_preview)

        self.v_margin.valueChanged.connect(self.update_preview)

        layout.addStretch()

        # 기본값을 한 번 적용
        self.same_position_changed(
            self.same_position.isChecked()
        )

        self.update_preview()

    def even_position_changed(self, position):

        if self.same_position.isChecked():
            self.odd_selector.set_selected(
                position,
                emit_signal=False
            )

        self.update_preview()

    def odd_position_changed(self, position):

        if self.same_position.isChecked():
            self.even_selector.set_selected(
                position,
                emit_signal=False
            )

        self.update_preview()

    def same_position_changed(self, checked):

        if checked:
            # 체크하는 순간 짝수 페이지 위치를 홀수 페이지에 복사
            self.odd_selector.set_selected(
                self.even_selector.selected
            )

        self.update_preview()

    def update_preview(self):

        data = {

            # ------------------------
            # 위치
            # ------------------------
            "even_position": self.even_selector.selected,
            "odd_position": self.odd_selector.selected,
            "same_position": self.same_position.isChecked(),

            # ------------------------
            # 글꼴
            # ------------------------
            "font_size": self.font_size.value(),

            # ------------------------
            # 시작번호
            # ------------------------
            "start_number": self.start_number.value(),

            # ------------------------
            # 여백
            # ------------------------
            "horizontal_margin": self.h_margin.value(),
            "vertical_margin": self.v_margin.value(),

            "use_dash": self.use_dash.isChecked(),

        }

        self.previewChanged.emit(data)
