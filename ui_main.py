
from PySide6.QtCore import Qt
from pathlib import Path
from file_merge import find_pdf_files
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==========================
        # 창 설정
        # ==========================

        self.setWindowTitle("PDF Book Maker v0.2")
        self.resize(800, 600)

        # ==========================
        # 책 제목
        # ==========================

        title_label = QLabel("책 제목")
        self.title_edit = QLineEdit()

        # ==========================
        # 입력 파일
        # ==========================

        input_label = QLabel("입력 파일")

        self.input_edit = QLineEdit()
        self.input_edit.setReadOnly(True)

        self.input_button = QPushButton("파일 선택")
        self.input_button.clicked.connect(self.select_input_files)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.input_button)

        # ==========================
        # 출력 폴더
        # ==========================

        output_label = QLabel("출력 폴더")

        self.output_edit = QLineEdit()

        self.output_button = QPushButton("찾아보기")
        self.output_button.clicked.connect(self.select_output_folder)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_button)

        # ==========================
        # 진행바
        # ==========================

        progress_label = QLabel("진행상황")

        self.progress = QProgressBar()
        self.progress.setValue(0)

        # ==========================
        # PDF 목록
        # ==========================

        self.table = QTableWidget()

        self.table.verticalHeader().setVisible(False)

        self.table.itemSelectionChanged.connect(self.show_selected_title)

        # ▼ v0.4 : 전자책 제목 수정 기능
        # self.table.setEditTriggers(QTableWidget.DoubleClicked)

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            ["순서", "원본 파일명", "전자책 제목"]
        )

        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 300)

        # ==========================
        # 선택한 PDF 정보
        # ==========================

        info_label = QLabel("선택한 PDF 정보")

        title_edit_label = QLabel("전자책 제목")

        self.book_title_edit = QLineEdit()

        self.apply_button = QPushButton("적용")
        self.apply_button.clicked.connect(self.apply_title)

        self.up_button = QPushButton("▲ 위로")
        self.down_button = QPushButton("▼ 아래로")

        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)

        # ==========================
        # 로그창
        # ==========================

        log_label = QLabel("로그")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.log.append("프로그램을 시작했습니다.")

        # ==========================
        # 실행 버튼
        # ==========================

        self.make_button = QPushButton("전자책 만들기")
        self.make_button.clicked.connect(self.make_book)

        # ==========================
        # 전체 배치
        # ==========================

        layout = QVBoxLayout()

        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)

        layout.addWidget(input_label)
        layout.addLayout(input_layout)

        layout.addWidget(output_label)
        layout.addLayout(output_layout)

        layout.addWidget(progress_label)
        layout.addWidget(self.progress)

        layout.addWidget(self.table)

        layout.addWidget(info_label)

        layout.addWidget(title_edit_label)
        layout.addWidget(self.book_title_edit)

        layout.addWidget(self.apply_button)

        move_layout = QHBoxLayout()
        move_layout.addWidget(self.up_button)
        move_layout.addWidget(self.down_button)

        layout.addLayout(move_layout)

        layout.addWidget(log_label)
        layout.addWidget(self.log)

        layout.addWidget(self.make_button)

        self.setLayout(layout)

    def select_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "PDF 파일 선택",
            "",
            "PDF 파일 (*.pdf);;ZIP 파일 (*.zip)"
        )

        if files:
            self.selected_files = files
            self.input_edit.setText(f"{len(files)}개 파일 선택")

            # 테이블 초기화
            self.table.setRowCount(0)

            # 파일 목록 추가
            for i, file in enumerate(files):
                self.table.insertRow(i)

                filename = Path(file).name

                order_item = QTableWidgetItem(str(i + 1))
                order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, 0, order_item)

                file_item = QTableWidgetItem(filename)
                file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, 1, file_item)

                title_item = QTableWidgetItem(filename)
                self.table.setItem(i, 2, title_item)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "출력 폴더 선택"
        )

        if folder:
            self.output_edit.setText(folder)
            self.log.append(f"출력 폴더 선택 : {folder}")

    def show_selected_title(self):

        row = self.table.currentRow()

        if row < 0:
            return

        title = self.table.item(row, 2).text()

        self.book_title_edit.setText(title)

    def apply_title(self):

        row = self.table.currentRow()

        if row < 0:
            return

        title = self.book_title_edit.text()

        self.table.item(row, 2).setText(title)

    def move_up(self):

        row = self.table.currentRow()

        # 첫 번째 행이면 이동 불가
        if row <= 0:
            return

        # 위 행과 현재 행의 데이터를 서로 교환
        for col in range(self.table.columnCount()):

            current = self.table.takeItem(row, col)
            upper = self.table.takeItem(row - 1, col)

            self.table.setItem(row - 1, col, current)
            self.table.setItem(row, col, upper)

        # 이동한 행 선택 유지
        self.table.selectRow(row - 1)

        self.update_order()

    def move_down(self):

        row = self.table.currentRow()

        # 마지막 행이면 이동 불가
        if row >= self.table.rowCount() - 1:
            return

        # 현재 행과 아래 행 교환
        for col in range(self.table.columnCount()):

            current = self.table.takeItem(row, col)
            lower = self.table.takeItem(row + 1, col)

            self.table.setItem(row + 1, col, current)
            self.table.setItem(row, col, lower)

        # 선택 유지
        self.table.selectRow(row + 1)

        self.update_order()

    def update_order(self):

        for row in range(self.table.rowCount()):

            item = self.table.item(row, 0)

            if item:
                item.setText(str(row + 1))

    def make_book(self):

        # 파일을 선택하지 않은 경우
        if not hasattr(self, "selected_files") or not self.selected_files:
            self.log.append("PDF 파일을 먼저 선택하세요.")
            return

        self.log.append("=" * 40)
        self.log.append(f"선택된 PDF : {len(self.selected_files)}개")
        self.log.append("")

        for pdf in self.selected_files:
            filename = Path(pdf).name
            self.log.append(filename)

        self.log.append("")
        self.log.append("전자책 제작 준비 완료!")