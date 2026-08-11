from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QComboBox,
    QSpinBox,
    QSlider,
    QFileDialog,
)


class CoverPage(QWidget):

    coverChanged = Signal(dict)

    def __init__(self):
        super().__init__()

        # ======================================
        # 메인 레이아웃
        # ======================================
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        # ======================================
        # 왼쪽 메뉴
        # ======================================
        left_layout = QVBoxLayout()

        title = QLabel("# 표지")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        left_layout.addWidget(title)

        self.menu = QListWidget()
        self.menu.addItems([
            "제목",
            "부제목",
            "하단 정보",
            "그림",
        ])

        left_layout.addWidget(self.menu)

        main_layout.addLayout(left_layout, 1)

        # ======================================
        # 가운데 Stack
        # ======================================
        self.stack = QStackedWidget()

        # --------------------------------------
        # 제목 페이지
        # --------------------------------------
        title_page = QWidget()
        layout = QVBoxLayout(title_page)

        layout.addWidget(QLabel("내용"))

        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("글꼴"))

        self.title_font = QComboBox()
        self.title_font.addItems([
            "맑은 고딕",
            "나눔고딕",
            "나눔명조",
        ])
        layout.addWidget(self.title_font)

        layout.addWidget(QLabel("글자 크기"))

        self.title_size = QSpinBox()
        self.title_size.setRange(8, 72)
        self.title_size.setValue(22)
        layout.addWidget(self.title_size)

        layout.addStretch()

        self.stack.addWidget(title_page)

        layout.addWidget(QLabel("정렬"))

        self.title_align = QComboBox()

        self.title_align.addItems([
            "왼쪽",
            "가운데",
            "오른쪽",
        ])

        layout.addWidget(self.title_align)

        self.title_align.currentIndexChanged.connect(
            self.emit_cover_changed
        )

        # --------------------------------------
        # 부제목 페이지
        # --------------------------------------
        subtitle_page = QWidget()
        layout = QVBoxLayout(subtitle_page)

        layout.addWidget(QLabel("내용"))

        self.subtitle_edit = QLineEdit()
        layout.addWidget(self.subtitle_edit)

        layout.addWidget(QLabel("글꼴"))

        self.subtitle_font = QComboBox()
        self.subtitle_font.addItems([
            "맑은 고딕",
            "나눔고딕",
            "나눔명조",
        ])
        layout.addWidget(self.subtitle_font)

        layout.addWidget(QLabel("글자 크기"))

        self.subtitle_size = QSpinBox()
        self.subtitle_size.setRange(8, 72)
        self.subtitle_size.setValue(12)
        layout.addWidget(self.subtitle_size)

        layout.addStretch()

        self.stack.addWidget(subtitle_page)

        layout.addWidget(QLabel("정렬"))

        self.subtitle_align = QComboBox()

        self.subtitle_align.addItems([
            "왼쪽",
            "가운데",
            "오른쪽",
        ])

        layout.addWidget(self.subtitle_align)

        self.subtitle_align.currentIndexChanged.connect(
            self.emit_cover_changed
        )

        # --------------------------------------
        # 표지 정보 페이지
        # --------------------------------------
        info_page = QWidget()
        layout = QVBoxLayout(info_page)

        layout.addWidget(QLabel("표지 정보"))

        self.table = QTableWidget(4, 2)

        self.table.setHorizontalHeaderLabels([
            "항목",
            "내용",
        ])

        self.table.setItem(0, 0, QTableWidgetItem("작성자"))
        self.table.setItem(0, 1, QTableWidgetItem("깨비"))

        self.table.setItem(1, 0, QTableWidgetItem("학교"))
        self.table.setItem(1, 1, QTableWidgetItem("부산디지털대학교"))

        self.table.setItem(2, 0, QTableWidgetItem("과목"))
        self.table.setItem(2, 1, QTableWidgetItem("컴퓨터활용능력"))

        self.table.setItem(3, 0, QTableWidgetItem("버전"))
        self.table.setItem(3, 1, QTableWidgetItem("v1.0"))

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("추가")
        self.delete_button = QPushButton("삭제")

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_item)

        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        layout.addWidget(QLabel("글꼴"))

        self.info_font = QComboBox()
        self.info_font.addItems([
            "맑은 고딕",
            "나눔고딕",
            "나눔명조",
        ])
        layout.addWidget(self.info_font)

        layout.addWidget(QLabel("글자 크기"))

        self.info_size = QSpinBox()
        self.info_size.setRange(8, 72)
        self.info_size.setValue(11)
        layout.addWidget(self.info_size)

        layout.addStretch()

        self.stack.addWidget(info_page)

        layout.addWidget(QLabel("정렬"))

        self.info_align = QComboBox()

        self.info_align.addItems([
            "왼쪽",
            "가운데",
            "오른쪽",
        ])

        layout.addWidget(self.info_align)

        self.info_align.currentIndexChanged.connect(
            self.emit_cover_changed
        )

        # ======================================
        # 그림 페이지
        # ======================================
        image_page = QWidget()
        layout = QVBoxLayout(image_page)

        layout.addWidget(QLabel("그림"))

        self.image_path = QLineEdit()
        self.image_path.setReadOnly(True)

        layout.addWidget(self.image_path)

        self.image_button = QPushButton("그림 선택")
        layout.addWidget(QLabel("크기 (%)"))

        # -----------------------------
        # 그림 정렬
        # -----------------------------
        layout.addWidget(QLabel("정렬"))

        self.image_align = QComboBox()

        self.image_align.addItems([
            "가운데",
            "왼쪽",
            "오른쪽",
        ])

        layout.addWidget(self.image_align)

        layout.addWidget(QLabel("위치"))

        self.image_y_slider = QSlider(Qt.Horizontal)

        self.image_y_slider.setRange(0, 250)
        self.image_y_slider.setValue(20)

        layout.addWidget(self.image_y_slider)

        self.image_size = QSpinBox()
        self.image_size.setRange(10, 300)
        self.image_size.setValue(100)

        layout.addWidget(self.image_size)
        layout.addWidget(self.image_button)
        self.image_size.valueChanged.connect(
            self.emit_cover_changed
        )

        self.image_button.clicked.connect(
            self.select_image
        )

        self.image_y_slider.valueChanged.connect(
            self.emit_cover_changed
        )

        self.image_align.currentIndexChanged.connect(
            self.emit_cover_changed
        )

        layout.addStretch()

        self.stack.addWidget(image_page)

        # ======================================
        # 배치
        # ======================================
        main_layout.addWidget(self.stack, 2)

        # ======================================
        # 연결
        # ======================================
        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)

        # Signal
        self.title_edit.textChanged.connect(self.emit_cover_changed)
        self.subtitle_edit.textChanged.connect(self.emit_cover_changed)

        self.title_font.currentTextChanged.connect(self.emit_cover_changed)
        self.subtitle_font.currentTextChanged.connect(self.emit_cover_changed)
        self.info_font.currentTextChanged.connect(self.emit_cover_changed)

        self.title_size.valueChanged.connect(self.emit_cover_changed)
        self.subtitle_size.valueChanged.connect(self.emit_cover_changed)
        self.info_size.valueChanged.connect(self.emit_cover_changed)

        self.table.itemChanged.connect(self.emit_cover_changed)

    # ======================================
    # 설정 반환
    # ======================================
    def get_cover_settings(self):

        items = []

        for row in range(self.table.rowCount()):

            key = ""
            value = ""

            item0 = self.table.item(row, 0)
            item1 = self.table.item(row, 1)

            if item0:
                key = item0.text()

            if item1:
                value = item1.text()

            items.append({
                "label": key,
                "value": value,
            })

        print("subtitle =", self.subtitle_align.currentText())

        return {

            "title": self.title_edit.text(),
            "subtitle": self.subtitle_edit.text(),

            "title_font": self.title_font.currentText(),
            "title_size": self.title_size.value(),
            "title_align": self.title_align.currentText(),

            "subtitle_font": self.subtitle_font.currentText(),
            "subtitle_size": self.subtitle_size.value(),

            "info_font": self.info_font.currentText(),
            "info_size": self.info_size.value(),

            "items": items,

            "image_path": self.image_path.text(),
            "image_size": self.image_size.value(),
            "image_y": self.image_y_slider.value(),
            "image_align": self.image_align.currentText(),            

            "subtitle_align": self.subtitle_align.currentText(),
            "info_align": self.info_align.currentText(),
        }

    # ======================================
    # Signal
    # ======================================
    def emit_cover_changed(self):

        self.coverChanged.emit(
            self.get_cover_settings()
        )

    # ---------------------------------
    # 하단 정보 추가
    # ---------------------------------
    def add_item(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))

        self.table.setCurrentCell(row, 0)

        self.emit_cover_changed()


    # ---------------------------------
    # 하단 정보 삭제
    # ---------------------------------
    def delete_item(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.table.removeRow(row)

        self.emit_cover_changed()

    def select_image(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "그림 선택",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:

            self.image_path.setText(path)

            self.emit_cover_changed()