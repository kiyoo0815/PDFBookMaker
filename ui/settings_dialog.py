from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QTableWidgetItem,
)

from ui.pages.page_number_page import PageNumberPage
from ui.pages.cover_page import CoverPage
from ui.widgets.cover_preview_widget import CoverPreviewWidget
from ui.widgets.page_number_preview_widget import PageNumberPreviewWidget


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 전자책 상세 설정 저장
        self.settings = QSettings(
            "PDFBookMaker",
            "PDFBookMaker"
        )

        self.setWindowTitle("전자책 설정")
        self.resize(1280, 800)

        # ==========================================
        # 메인 레이아웃
        # ==========================================
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # ==========================================
        # 왼쪽 메뉴
        # ==========================================
        self.menu = QListWidget()
        self.menu.setFixedWidth(180)

        self.menu.setStyleSheet("""
        QListWidget{
            background:white;
            border:1px solid #d8dee9;
            border-radius:12px;
            outline:none;
            padding:8px;
        }

        QListWidget::item{
            min-height:44px;
            border-radius:8px;
            padding-left:12px;
            margin-top:3px;
            margin-bottom:3px;
            color:#374151;
        }

        QListWidget::item:hover{
            background:#eff6ff;
        }

        QListWidget::item:selected{
            background:#2563eb;
            color:white;
            font-weight:bold;
        }
        """)

        self.menu.addItems([
            "   🖼   표지",
            "   #    페이지 번호",
        ])

        # ==========================================
        # 가운데 페이지
        # ==========================================
        self.stack = QStackedWidget()

        self.cover_page = CoverPage()
        self.page_number_page = PageNumberPage()

        self.stack.addWidget(self.cover_page)
        self.stack.addWidget(self.page_number_page)

        # ==========================================
        # 오른쪽 미리보기
        # ==========================================
        self.preview_stack = QStackedWidget()

        # 표지 미리보기
        self.preview = CoverPreviewWidget()

        # 페이지 번호 미리보기
        self.page_number_preview = PageNumberPreviewWidget()

        self.preview_stack.addWidget(self.preview)
        self.preview_stack.addWidget(self.page_number_preview)

        # 표지 설정 → 표지 미리보기
        self.cover_page.coverChanged.connect(
            self.update_cover_preview
        )

        # 표지 설정 변경 → 자동 저장
        self.cover_page.coverChanged.connect(
            self.save_cover_settings
        )

        # 표지 드래그 → 설정값
        self.preview.positionChanged.connect(
            self.update_preview_position
        )

        # 페이지 번호 설정 → 페이지 번호 미리보기
        self.page_number_page.previewChanged.connect(
            self.page_number_preview.set_settings
        )

        # 페이지 번호 설정 변경 → 자동 저장
        self.page_number_page.previewChanged.connect(
            self.save_page_number_settings
        )

        # ==========================================
        # 레이아웃
        # ==========================================
        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.stack)
        main_layout.addWidget(self.preview_stack)

        # ==========================================
        # 메뉴 연결
        # ==========================================
        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.currentRowChanged.connect(
            self.preview_stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)

        # 저장된 페이지 번호 설정 불러오기
        self.load_page_number_settings()

        # 저장된 표지 설정 불러오기
        self.load_cover_settings()

    def get_page_number_settings(self):

        page = self.page_number_page

        return {
            "same_position": page.same_position.isChecked(),
            "even_position": page.even_selector.selected,
            "odd_position": page.odd_selector.selected,
            "font_size": page.font_size.value(),
            "start_number": page.start_number.value(),
            "horizontal_margin": page.h_margin.value(),
            "vertical_margin": page.v_margin.value(),
            "use_dash": page.use_dash.isChecked(),
        }

    def update_cover_preview(self, data):

        self.preview.set_title(data["title"])
        self.preview.set_subtitle(data["subtitle"])
        self.preview.set_items(data["items"])

        self.preview.set_title_style(
            data["title_font"],
            data["title_size"]
        )

        self.preview.set_title_align(
            data["title_align"]
        )

        self.preview.set_title_y(
            data["title_y"]
        )

        self.preview.set_subtitle_style(
            data["subtitle_font"],
            data["subtitle_size"]
        )

        self.preview.set_subtitle_align(
            data["subtitle_align"]
        )

        self.preview.set_subtitle_y(
            data["subtitle_y"]
        )

        self.preview.set_info_style(
            data["info_font"],
            data["info_size"]
        )

        self.preview.set_info_align(
            data["info_align"]
        )

        self.preview.set_info_y(
            data["info_y"]
        )

        self.preview.set_info_spacing(
            data["info_spacing"]
        )

        self.preview.set_image(
            data["image_path"],
            data["image_size"]
        )

        self.preview.set_image_position(
            data["image_y"]
        )

        self.preview.set_image_align(
            data["image_align"]
        )

    def get_cover_settings(self):
        return self.cover_page.get_cover_settings()

    def update_preview_position(self, target, value):

        if target == "title":

            self.cover_page.title_y.setValue(value)

        elif target == "subtitle":

            self.cover_page.subtitle_y.setValue(value)

        elif target == "info":

            self.cover_page.info_y.setValue(value)

        elif target == "image":
            self.cover_page.image_y.setValue(value)

    def set_preview_pdf(self, pdf_path):
        """페이지 번호 미리보기에 사용할 PDF 전달"""

        self.page_number_preview.set_pdf(
            pdf_path
        )

    def save_page_number_settings(self, data=None):
        """페이지 번호 설정 저장"""

        page = self.page_number_page

        self.settings.setValue(
            "page_number/same_position",
            page.same_position.isChecked()
        )

        self.settings.setValue(
            "page_number/even_position",
            page.even_selector.selected
        )

        self.settings.setValue(
            "page_number/odd_position",
            page.odd_selector.selected
        )

        self.settings.setValue(
            "page_number/font_size",
            page.font_size.value()
        )

        self.settings.setValue(
            "page_number/start_number",
            page.start_number.value()
        )

        self.settings.setValue(
            "page_number/horizontal_margin",
            page.h_margin.value()
        )

        self.settings.setValue(
            "page_number/vertical_margin",
            page.v_margin.value()
        )

        self.settings.setValue(
            "page_number/use_dash",
            page.use_dash.isChecked()
        )

    def load_page_number_settings(self):
        """저장된 페이지 번호 설정 불러오기"""

        page = self.page_number_page

        # 동일 위치 적용
        same_position = self.settings.value(
            "page_number/same_position",
            True,
            type=bool
        )

        # 짝수 / 홀수 위치
        even_position = self.settings.value(
            "page_number/even_position",
            5,
            type=int
        )

        odd_position = self.settings.value(
            "page_number/odd_position",
            5,
            type=int
        )

        # 글꼴 크기
        font_size = self.settings.value(
            "page_number/font_size",
            14,
            type=int
        )

        # 시작 번호
        start_number = self.settings.value(
            "page_number/start_number",
            1,
            type=int
        )

        # 여백
        horizontal_margin = self.settings.value(
            "page_number/horizontal_margin",
            15,
            type=int
        )

        vertical_margin = self.settings.value(
            "page_number/vertical_margin",
            15,
            type=int
        )

        # 하이픈
        use_dash = self.settings.value(
            "page_number/use_dash",
            False,
            type=bool
        )

        # -------------------------
        # 화면에 적용
        # -------------------------

        page.same_position.setChecked(
            same_position
        )

        page.even_selector.set_selected(
            even_position,
            emit_signal=False
        )

        page.odd_selector.set_selected(
            odd_position,
            emit_signal=False
        )

        page.font_size.setValue(
            font_size
        )

        page.start_number.setValue(
            start_number
        )

        page.h_margin.setValue(
            horizontal_margin
        )

        page.v_margin.setValue(
            vertical_margin
        )

        page.use_dash.setChecked(
            use_dash
        )

        # 미리보기 최종 갱신
        page.update_preview()

    def save_cover_settings(self, data):
        """표지 설정 저장"""

        # 설정을 불러오는 중에는 저장하지 않는다.
        if getattr(self, "_loading_cover_settings", False):
            return

        # 제목
        self.settings.setValue(
            "cover/title",
            data["title"]
        )

        self.settings.setValue(
            "cover/title_size",
            data["title_size"]
        )

        self.settings.setValue(
            "cover/title_align",
            data["title_align"]
        )

        self.settings.setValue(
            "cover/title_y",
            data["title_y"]
        )

        # 부제목
        self.settings.setValue(
            "cover/subtitle",
            data["subtitle"]
        )

        self.settings.setValue(
            "cover/subtitle_size",
            data["subtitle_size"]
        )

        self.settings.setValue(
            "cover/subtitle_align",
            data["subtitle_align"]
        )

        self.settings.setValue(
            "cover/subtitle_y",
            data["subtitle_y"]
        )

        # 하단 정보

        self.settings.setValue(
            "cover/info_size",
            data["info_size"]
        )

        self.settings.setValue(
            "cover/info_align",
            data["info_align"]
        )

        self.settings.setValue(
            "cover/info_y",
            data["info_y"]
        )

        self.settings.setValue(
            "cover/info_spacing",
            data["info_spacing"]
        )

        # -------------------------
        # 하단 정보 테이블 내용
        # -------------------------
        self.settings.beginWriteArray(
            "cover/items",
            len(data["items"])
        )

        for index, item in enumerate(data["items"]):

            self.settings.setArrayIndex(index)

            self.settings.setValue(
                "label",
                item["label"]
            )

            self.settings.setValue(
                "value",
                item["value"]
            )

        self.settings.endArray()

        # 그림
        self.settings.setValue(
            "cover/image_size",
            data["image_size"]
        )

        self.settings.setValue(
            "cover/image_align",
            data["image_align"]
        )

        self.settings.setValue(
            "cover/image_y",
            data["image_y"]
        )

    def load_cover_settings(self):
        """저장된 표지 설정 불러오기"""

        self._loading_cover_settings = True

        page = self.cover_page

        # -------------------------
        # 제목
        # -------------------------
        page.title_edit.setText(
            self.settings.value(
                "cover/title",
                "",
                type=str
            )
        )

        page.title_size.setValue(
            self.settings.value(
                "cover/title_size",
                22,
                type=int
            )
        )

        page.title_align.setCurrentText(
            self.settings.value(
                "cover/title_align",
                "왼쪽",
                type=str
            )
        )

        page.title_y.setValue(
            self.settings.value(
                "cover/title_y",
                165,
                type=int
            )
        )

        # -------------------------
        # 부제목
        # -------------------------
        page.subtitle_edit.setText(
            self.settings.value(
                "cover/subtitle",
                "",
                type=str
            )
        )

        page.subtitle_size.setValue(
            self.settings.value(
                "cover/subtitle_size",
                12,
                type=int
            )
        )

        page.subtitle_align.setCurrentText(
            self.settings.value(
                "cover/subtitle_align",
                "왼쪽",
                type=str
            )
        )

        page.subtitle_y.setValue(
            self.settings.value(
                "cover/subtitle_y",
                270,
                type=int
            )
        )

        # -------------------------
        # 하단 정보
        # -------------------------

        page.info_size.setValue(
            self.settings.value(
                "cover/info_size",
                11,
                type=int
            )
        )

        page.info_align.setCurrentText(
            self.settings.value(
                "cover/info_align",
                "왼쪽",
                type=str
            )
        )

        page.info_y.setValue(
            self.settings.value(
                "cover/info_y",
                500,
                type=int
            )
        )

        page.info_spacing.setValue(
            self.settings.value(
                "cover/info_spacing",
                28,
                type=int
            )
        )

        # -------------------------
        # 하단 정보 테이블 내용
        # -------------------------
        item_count = self.settings.beginReadArray(
            "cover/items"
        )

        # 저장된 하단 정보가 있을 때만 복원
        if item_count > 0:

            page.table.setRowCount(0)

            for index in range(item_count):

                self.settings.setArrayIndex(index)

                label = self.settings.value(
                    "label",
                    "",
                    type=str
                )

                value = self.settings.value(
                    "value",
                    "",
                    type=str
                )

                row = page.table.rowCount()
                page.table.insertRow(row)

                page.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(label)
                )

                page.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(value)
                )

        self.settings.endArray()

        # -------------------------
        # 그림
        # -------------------------
        page.image_size.setValue(
            self.settings.value(
                "cover/image_size",
                100,
                type=int
            )
        )

        page.image_align.setCurrentText(
            self.settings.value(
                "cover/image_align",
                "가운데",
                type=str
            )
        )

        page.image_y.setValue(
            self.settings.value(
                "cover/image_y",
                80,
                type=int
            )
        )

        # 설정 불러오기 완료
        self._loading_cover_settings = False

        # 미리보기 최종 갱신
        page.emit_cover_changed()