from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
)

from ui.pages.page_number_page import PageNumberPage
from ui.pages.cover_page import CoverPage
from ui.widgets.cover_preview_widget import CoverPreviewWidget


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.preview = CoverPreviewWidget()

        self.cover_page.coverChanged.connect(
            self.update_cover_preview
        )

        self.preview.positionChanged.connect(
            self.update_preview_position
        )

        # ==========================================
        # 레이아웃
        # ==========================================
        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.stack)
        main_layout.addWidget(self.preview)

        # ==========================================
        # 메뉴 연결
        # ==========================================
        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)

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

        print(data["title_y"])

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