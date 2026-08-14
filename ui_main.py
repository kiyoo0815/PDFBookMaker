import os
from ui.utils.pdf_title_reader import extract_pdf_info
from file_merge import merge_pdf
from ui.settings_dialog import SettingsDialog
from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QAbstractItemView
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
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
    QTableWidgetItem,
    QMessageBox,
    QInputDialog,
    QGroupBox,
    QSplitter,
    QFrame,
    QHeaderView
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==========================
        # 창 설정
        # ==========================

        self.setWindowTitle("PDF Book Maker v1.0 RC")
        self.resize(1200, 800)

        # 프로그램 설정 저장
        self.settings = QSettings("PDFBookMaker", "PDFBookMaker")

        # 이전 설정 불러오기
        last_output_folder = self.settings.value("output_folder", "")
        last_book_name = self.settings.value("book_name", "")

        # 마지막 창 크기 복원
        size = self.settings.value("window_size")

        if size:
            self.resize(size)

        # 마지막 창 위치 복원
        pos = self.settings.value("window_pos")

        if pos:
            self.move(pos)

        # ==========================
        # 프로그램 헤더
        # ==========================

        header = QLabel("📚 PDF Book Maker")
        header.setStyleSheet("""
        font-size:24pt;
        font-weight:bold;
        color:#2563eb;
        background:transparent;
        """)

        sub_title = QLabel("Professional PDF Book Creator")
        sub_title.setStyleSheet("""
        color:#6b7280;
        font-size:10pt;
        background:transparent;
        """)

        version = QLabel("v1.1")
        version.setStyleSheet("""
        color:#9ca3af;
        font-size:9pt;
        background:transparent;
        """)

        header_left = QVBoxLayout()
        header_left.setSpacing(2)
        header_left.addWidget(header)
        header_left.addWidget(sub_title)

        header_layout = QHBoxLayout()
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        header_layout.addWidget(version)

        header_frame = QFrame()
        header_frame.setLayout(header_layout)

        # ==========================
        # 입력 파일
        # ==========================

        input_label = QLabel("입력 파일")

        self.input_edit = QLineEdit()
        self.input_edit.setReadOnly(True)
        self.input_edit.setFocusPolicy(Qt.NoFocus)

        self.input_button = QPushButton("파일 선택")
        self.input_button.clicked.connect(self.select_input_files)
        self.input_button.setFixedSize(80, 32)

        self.section_button = QPushButton("목차 추가")
        self.section_button.clicked.connect(self.add_section_row)
        self.section_button.setFixedSize(80, 32)

        self.section_delete_button = QPushButton("목차 삭제")
        self.section_delete_button.clicked.connect(self.delete_section_row)
        self.section_delete_button.setFixedSize(80, 32)

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input_edit)

        input_layout.addWidget(self.input_button)
        input_layout.addWidget(self.section_button)
        input_layout.addWidget(self.section_delete_button)

        # ==========================
        # 출력 폴더
        # ==========================

        output_label = QLabel("출력 폴더")

        self.output_edit = QLineEdit()
        self.output_edit.setText(last_output_folder)

        self.output_button = QPushButton("찾아보기")
        self.output_button.clicked.connect(self.select_output_folder)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_button)
        self.output_button.setFixedSize(80, 32)

        # ==========================
        # 출력 파일명
        # ==========================

        book_label = QLabel("출력 파일명")

        self.book_name_edit = QLineEdit()
        self.book_name_edit.textChanged.connect(self.save_book_name)
        self.book_name_edit.setPlaceholderText("출력 파일명을 입력하세요.")
        self.book_name_edit.setText(last_book_name)

        # ==========================
        # 진행바
        # ==========================

        progress_label = QLabel("진행상황")

        self.progress = QProgressBar()
        self.progress.setFixedHeight(24)
        self.progress.setValue(0)

        # ==========================
        # PDF 목록
        # ==========================

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # ★ 여기 2줄 추가
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setCurrentCell(-1, -1)

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)

        self.table.itemSelectionChanged.connect(self.show_selected_title)

        # 전자책 제목 수정 기능
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.EditKeyPressed
        )

        self.table.setColumnCount(3)
        self.table.verticalHeader().setDefaultSectionSize(34)

        self.table.setHorizontalHeaderLabels(
            ["순서", "원본 파일명", "북마크 제목"]
        )

        for col in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(col)
            item.setTextAlignment(Qt.AlignCenter)

        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.setFocusPolicy(Qt.NoFocus)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setCurrentCell(-1, -1)

        # ==========================
        # 선택한 PDF 북마크
        # ==========================

        title_edit_label = QLabel("선택한 PDF 북마크")

        self.book_title_edit = QLineEdit()

        self.apply_button = QPushButton("적용")
        self.apply_button.clicked.connect(self.apply_title)
        self.apply_button.setFixedWidth(85)

        self.up_button = QPushButton("▲ 위로")
        self.down_button = QPushButton("▼ 아래로")

        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)

        self.book_title_edit.returnPressed.connect(self.apply_title)

        # ==========================
        # 로그창
        # ==========================

        log_label = QLabel("로그")

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(140)

        self.log.append("프로그램을 시작했습니다.")

        # ==========================
        # 실행 버튼
        # ==========================

        self.make_button = QPushButton("전자책 만들기")
        self.make_button.setFixedWidth(280)
        self.make_button.setFixedHeight(42)
        self.make_button.clicked.connect(self.make_book)
        self.book_name_edit.returnPressed.connect(self.make_book)

        primary_style = """
        QPushButton{
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
        }
        QPushButton:hover{
            background:#3b82f6;
        }
        QPushButton:pressed{
            background:#1d4ed8;
        }
        """

        self.make_button.setStyleSheet(primary_style)

        # ==========================
        # 로그 그룹
        # ==========================

        log_group = QGroupBox("📝 로그")
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log)
        log_group.setLayout(log_layout)

        # ==========================
        # 그룹 박스 생성
        # ==========================

        left_group = QGroupBox("📄 PDF 목록")
        left_layout = QVBoxLayout()
        left_layout.addWidget(input_label)
        left_layout.addLayout(input_layout)
        left_layout.addWidget(self.table)
        left_group.setLayout(left_layout)


        right_group = QGroupBox("📘 전자책 설정")
        right_layout = QVBoxLayout()

        right_layout.addWidget(output_label)
        right_layout.addLayout(output_layout)

        right_layout.addWidget(book_label)
        right_layout.addWidget(self.book_name_edit)

        # -------------------------------
        right_layout.addSpacing(12)
        # -------------------------------

        right_layout.addWidget(progress_label)
        right_layout.addWidget(self.progress)

        # -------------------------------
        right_layout.addSpacing(12)
        # -------------------------------

        bookmark_layout = QHBoxLayout()
        bookmark_layout.addWidget(self.book_title_edit)
        bookmark_layout.addWidget(self.apply_button)

        right_layout.addWidget(title_edit_label)
        right_layout.addLayout(bookmark_layout)

        right_layout.addSpacing(8)

        move_layout = QHBoxLayout()
        move_layout.addWidget(self.up_button)
        move_layout.addWidget(self.down_button)

        right_layout.addLayout(move_layout)

        # --------------------------------
        # 전자책 상세 설정 버튼
        # --------------------------------
        self.settings_button = QPushButton("⚙ 전자책 설정...")
        self.settings_button.setFixedHeight(38)
        self.settings_button.clicked.connect(self.open_settings_dialog)

        right_layout.addSpacing(15)
        right_layout.addWidget(self.settings_button)

        right_group.setLayout(right_layout)

        # ==========================
        # 메인 레이아웃
        # ==========================

        main_layout = QVBoxLayout()

        # 헤더
        main_layout.addWidget(header_frame)
        main_layout.addSpacing(15)

        # 좌우 분할
        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(left_group)
        splitter.addWidget(right_group)

        # 비율 (왼쪽 : 오른쪽 = 55 : 45)
        splitter.setStretchFactor(0, 55)
        splitter.setStretchFactor(1, 45)

        main_layout.addWidget(splitter)

        # 로그
        main_layout.addSpacing(10)
        main_layout.addWidget(log_group)

        # 버튼
        main_layout.addSpacing(10)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.make_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.settings_dialog = SettingsDialog(self)

        # ==========================
        # UI 스타일
        # ==========================

        self.setStyleSheet("""
        QWidget{
            font-family:'맑은 고딕';
            font-size:10pt;
            background:#f5f7fb;
        }

        QGroupBox{
            background:white;
            border:1px solid #d8dee9;
            border-radius:10px;
            margin-top:12px;
            font-weight:bold;
            padding-top:10px;
        }

        QGroupBox::title{
            subcontrol-origin: margin;
            left:12px;
            padding:0 6px;
            color:#2563eb;
            background:white;
        }

        QLineEdit{
            background:white;
            border:1px solid #cfd8e3;
            border-radius:6px;
            padding:6px;
        }

        QTextEdit{
            background:white;
            border:1px solid #cfd8e3;
            border-radius:6px;
        }

        QTableWidget{
            background:white;
            border:1px solid #cfd8e3;
            border-radius:6px;
            gridline-color:#e5e7eb;
        }

        /* Windows 기본 보라색(Current Cell) 방지 */
        QTableWidget::item:selected{
            background:#dbeafe;
            color:black;
        }

        QTableWidget::item:selected:active{
            background:#dbeafe;
            color:black;
        }

        QTableWidget::item:selected:!active{
            background:#dbeafe;
            color:black;
        }

        QTableWidget::item{
            selection-background-color:#dbeafe;
            selection-color:black;
        }

        QHeaderView::section{
            background:qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #ffffff,
                stop:1 #e6edf7
            );

            color:#1f2937;

            border-top:1px solid #ffffff;
            border-left:1px solid #ffffff;
            border-right:1px solid #d2dae6;
            border-bottom:2px solid #9fb2cb;

            padding:8px;

            font-weight:bold;
        }

        /* 기본 버튼 (회색) */
        QPushButton{
            background:#f3f4f6;
            color:#374151;
            border:1px solid #d1d5db;
            border-radius:8px;
            padding:8px;
        }

        QPushButton:hover{
            background:#e5e7eb;
        }

        QPushButton:pressed{
            background:#d1d5db;
        }

        QProgressBar{
            border:1px solid #cfd8e3;
            border-radius:6px;
            background:white;
            text-align:center;
            min-height:24px;
        }

        QProgressBar::chunk{
            background:#2563eb;
            border-radius:5px;
        }
        """)

    def open_settings_dialog(self):

        # 병합 순서 기준 첫 번째 PDF를 가져온다.
        try:
            ordered_files = self.get_ordered_pdf_files()
        except ValueError:
            ordered_files = []

        # PDF가 선택되어 있으면 첫 번째 PDF를 미리보기에 전달
        if ordered_files:
            self.settings_dialog.set_preview_pdf(
                ordered_files[0]
            )

        self.settings_dialog.exec()

    def select_input_files(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "PDF 파일 선택",
            "",
            "PDF 파일 (*.pdf)"
        )

        if files:
            self.selected_files = files
            self.input_edit.setText(f"PDF 파일 {len(files)}개 선택됨")            

            # 테이블 초기화
            self.table.setRowCount(0)

            # 이전 장 제목 저장
            previous_chapter = ""

            # 파일 목록 추가
            for i, file in enumerate(files):

                filename = Path(file).name
                chapter, lesson = extract_pdf_info(file)

                # 장이 바뀌면 목차 제목을 자동 추가
                if chapter and chapter != previous_chapter:

                    self.add_section_row_auto(chapter)

                    previous_chapter = chapter

                # PDF 행 추가
                row = self.table.rowCount()

                self.table.insertRow(row)

                order_item = QTableWidgetItem(str(i + 1))
                order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)
                order_item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, 0, order_item)

                file_item = QTableWidgetItem(filename)
                file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
                file_item.setTextAlignment(Qt.AlignCenter)

                # 화면에는 파일명만 표시하고 실제 경로는 항목에 함께 저장한다.
                file_item.setData(Qt.UserRole, file)

                # ★ 행 종류 저장
                file_item.setData(Qt.UserRole + 1, "pdf")

                self.table.setItem(row, 1, file_item)

                title = lesson if lesson else filename
                title_item = QTableWidgetItem(title)
                title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
                title_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, title_item)
        if self.table.rowCount() > 0:
            self.table.selectRow(0)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "출력 폴더 선택"
        )

        if folder:
            self.output_edit.setText(folder)
            self.log.append(f"출력 폴더 선택 : {folder}")

            # 마지막 출력 폴더 저장
            self.settings.setValue("output_folder", folder)

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
                item.setTextAlignment(Qt.AlignCenter)

    def get_ordered_pdf_files(self):
        """테이블에 표시된 순서대로 PDF 경로를 가져온다."""

        ordered_files = []

        for row in range(self.table.rowCount()):

            file_item = self.table.item(row, 1)

            if not file_item:
                raise ValueError("PDF 목록 정보를 읽을 수 없습니다.")

            # ★ 행 종류 확인
            row_type = file_item.data(Qt.UserRole + 1)

            # ★ 목차 제목은 건너뛴다.
            if row_type == "section":
                continue

            file_path = file_item.data(Qt.UserRole)

            if not file_path:
                raise ValueError("PDF 파일 경로를 읽을 수 없습니다.")

            ordered_files.append(file_path)

        return ordered_files

    def update_progress(self, value):
        """병합 엔진이 전달한 진행률을 화면에 표시한다."""

        self.progress.setValue(value)
        QApplication.processEvents()

    def append_merge_log(self, message):
        """병합 엔진이 전달한 작업 내용을 로그에 표시한다."""

        self.log.append(message)
        QApplication.processEvents()

    def make_book(self):

        # 파일을 선택하지 않은 경우
        if not hasattr(self, "selected_files") or not self.selected_files:
            QMessageBox.warning(
                self,
                "알림",
                "PDF 파일을 먼저 선택해 주세요."
            )
            return

        try:
            ordered_files = self.get_ordered_pdf_files()
        except ValueError as error:
            self.log.append(str(error))

            QMessageBox.critical(
                self,
                "오류",
                str(error)
            )
            return

        self.log.append("=" * 40)
        self.log.append(f"선택된 PDF : {len(ordered_files)}개")
        self.log.append("")

        for pdf in ordered_files:
            filename = Path(pdf).name
            self.log.append(filename)

        self.log.append("")
        self.log.append("전자책 제작 준비 완료!")

        book_name = self.book_name_edit.text().strip()
     
        if not book_name:
            QMessageBox.warning(
                self,
                "알림",
                "출력 파일명을 입력해 주세요."
            )

            self.book_name_edit.setFocus()
            return

        output_folder = self.output_edit.text().strip()

        if not output_folder:
            QMessageBox.warning(
                self,
                "알림",
                "출력 폴더를 선택해 주세요."
            )

            self.output_edit.setFocus()
            return

        output_file = os.path.join(
            output_folder,
            f"{book_name}.pdf"
        )

        if os.path.exists(output_file):

            reply = QMessageBox.question(
                self,
                "파일 확인",
                "같은 이름의 파일이 이미 있습니다.\n덮어쓰시겠습니까?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.No:
                return

        titles = []

        toc_items = []

        for row in range(self.table.rowCount()):

            file_item = self.table.item(row, 1)
            title_item = self.table.item(row, 2)

            row_type = file_item.data(Qt.UserRole + 1)

            if row_type == "section":

                toc_items.append({
                    "type": "section",
                    "title": title_item.text()
                })

            else:

                toc_items.append({
                    "type": "pdf",
                    "path": file_item.data(Qt.UserRole),
                    "title": title_item.text()
                })

        self.progress.setValue(0)
        self.make_button.setEnabled(False)

        page_number_settings = self.settings_dialog.get_page_number_settings()

        cover_settings = self.settings_dialog.get_cover_settings()

        try:
            merge_pdf(
                toc_items,
                self.book_name_edit.text(),
                output_file,
                page_number_settings,
                cover_settings,
                progress_callback=self.update_progress,
                log_callback=self.append_merge_log
            )
        except Exception as error:
            self.progress.setValue(0)
            error_message = f"전자책 생성 실패: {error}"
            self.log.append(error_message)

            QMessageBox.critical(
                self,
                "오류",
                error_message
            )
            return
        finally:
            self.make_button.setEnabled(True)

        QMessageBox.information(
            self,
            "완료",
            "전자책이 생성되었습니다."
        )

    def save_book_name(self):
        self.settings.setValue(
            "book_name",
            self.book_name_edit.text()
        )

    def closeEvent(self, event):
        # 창 크기 저장
        self.settings.setValue("window_size", self.size())

        # 창 위치 저장
        self.settings.setValue("window_pos", self.pos())

        super().closeEvent(event)

    def add_section_row(self):

        text, ok = QInputDialog.getText(
            self,
            "목차 추가",
            "목차 제목을 입력하세요.\n(비워두면 빈 목차가 추가됩니다.)"
        )

        if not ok:
            return

        row = self.table.currentRow()

        if row < 0:
            row = self.table.rowCount()

        self.table.insertRow(row)

        # 순서
        order_item = QTableWidgetItem("")
        order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)
        order_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, order_item)

        # 원본 파일명
        file_item = QTableWidgetItem("")
        file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)

        # ★ 목차 제목 행
        file_item.setData(Qt.UserRole + 1, "section")

        self.table.setItem(row, 1, file_item)

        # 제목
        title_item = QTableWidgetItem(text)
        title_item.setTextAlignment(Qt.AlignLeft)

        self.table.setItem(row, 2, title_item)

        self.table.selectRow(row)

        # 아무것도 입력하지 않았으면 바로 수정 가능
        if text.strip() == "":
            self.table.editItem(title_item)

    def add_section_row_auto(self, title):

        row = self.table.rowCount()

        self.table.insertRow(row)

        order_item = QTableWidgetItem("")
        self.table.setItem(row, 0, order_item)

        file_item = QTableWidgetItem("")
        file_item.setData(Qt.UserRole + 1, "section")
        self.table.setItem(row, 1, file_item)

        title_item = QTableWidgetItem(title)
        title_item.setTextAlignment(Qt.AlignLeft)

        self.table.setItem(row, 2, title_item)

    def delete_section_row(self):

        row = self.table.currentRow()

        if row < 0:
            return

        file_item = self.table.item(row, 1)

        if not file_item:
            return

        if file_item.data(Qt.UserRole + 1) != "section":
            QMessageBox.information(
                self,
                "알림",
                "목차 행만 삭제할 수 있습니다."
            )
            return

        self.table.removeRow(row)   