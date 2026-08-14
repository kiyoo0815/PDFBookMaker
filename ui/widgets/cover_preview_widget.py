from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QFont, QColor, QPixmap
from PySide6.QtWidgets import QFrame


class CoverPreviewWidget(QFrame):

    positionChanged = Signal(str, int)

    def __init__(self):
        super().__init__()

        self.setMinimumSize(320, 450)

        self.title_align = "가운데"
        self.subtitle_align = "가운데"
        self.info_align = "왼쪽"

        self.title_y = 165
        self.subtitle_y = 205
        self.info_y = 340
        self.info_spacing = 28

        self.setStyleSheet("""
            background:white;
            border:1px solid #cccccc;
            border-radius:8px;
        """)

        # 미리보기 기본값
        self.title = "제목"
        self.subtitle = "부제목"

        # -------------------------
        # 글꼴 설정
        # -------------------------
        self.title_font = "맑은 고딕"
        self.title_size = 22

        self.subtitle_font = "맑은 고딕"
        self.subtitle_size = 12

        self.info_font = "맑은 고딕"
        self.info_size = 11

        self.items = [
            ("작성자", "깨비"),
            ("학교", "부산디지털대학교"),
            ("과목", "컴퓨터활용능력"),
            ("버전", "v1.0"),
        ]

        # -------------------------
        # 표지 그림
        # -------------------------
        self.image = None
        self.image_size = 100
        self.image_mode = "logo"
        self.image_align = "center"
        self.image_y = 80

        # -------------------------
        # 드래그 관련
        # -------------------------
        self.dragging = False
        self.drag_target = None
        self.drag_offset = 0


    def set_title(self, text):

        self.title = text

        self.update()

    def set_subtitle(self, text):

        self.subtitle = text

        self.update()

    def set_subtitle_y(self, y):

        self.subtitle_y = y

        self.update()

    def set_items(self, items):

        self.items = []

        for item in items:

            self.items.append(
                (
                    item["label"],
                    item["value"]
                )
            )

        self.update()

    def set_image(self, path, size=100):

        if path:
            self.image = QPixmap(path)
        else:
            self.image = None

        self.image_size = size

        self.update()

    def set_image_mode(self, mode):

        self.image_mode = mode

        self.update()

    def set_image_position(self, y):

        self.image_y = y

        self.update()

    def set_image_align(self, align):

        self.image_align = align

        self.update()

    def set_title_style(self, font, size):

        self.title_font = font
        self.title_size = size

        self.update()

    def set_title_align(self, align):

        self.title_align = align

        self.update()

    def set_title_y(self, y):

        self.title_y = y

        self.update()


    def set_subtitle_style(self, font, size):

        self.subtitle_font = font
        self.subtitle_size = size

        self.update()


    def set_subtitle_align(self, align):

        self.subtitle_align = align

        self.update()


    def set_info_style(self, font, size):

        self.info_font = font
        self.info_size = size

        self.update()

    def set_info_align(self, align):

        self.info_align = align

        self.update()

    def set_info_y(self, y):

        self.info_y = y

        self.update()

    def set_info_spacing(self, spacing):

        self.info_spacing = spacing

        self.update()

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        # -------------------------
        # 그림
        # -------------------------

        print("paintEvent :", self.image_align)
        
        if self.image and not self.image.isNull():

            painter.setOpacity(0.25)

            if self.image_mode == "logo":

                base = 120
                size = int(base * self.image_size / 100)

                pix = self.image.scaled(
                    size,
                    size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                # -------------------------
                # X 위치
                # -------------------------
                margin = 20

                if self.image_align == "왼쪽":
                    x = margin

                elif self.image_align == "가운데":
                    x = (self.width() - pix.width()) // 2

                elif self.image_align == "오른쪽":
                    x = self.width() - pix.width() - margin

                else:
                    x = (self.width() - pix.width()) // 2

                painter.drawPixmap(
                    x,
                    self.image_y,
                    pix
                )

            else:

                pix = self.image.scaled(
                    self.width() - 20,
                    self.height() - 20,
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )

                painter.drawPixmap(
                    10,
                    self.image_y,
                    pix
                )

            painter.setOpacity(1.0)

        # -------------------------
        # 제목
        # -------------------------
        painter.setPen(QColor("#222222"))

        painter.setFont(
            QFont(
                self.title_font,
                self.title_size,
                QFont.Bold
            )
        )

        if self.title_align == "왼쪽":
            align = Qt.AlignLeft

        elif self.title_align == "오른쪽":
            align = Qt.AlignRight

        else:
            align = Qt.AlignCenter

        painter.drawText(
            20,
            self.title_y,
            self.width() - 40,
            40,
            align,
            self.title
        )

        # -------------------------
        # 부제목
        # -------------------------
        painter.setFont(
            QFont(
                self.subtitle_font,
                self.subtitle_size
            )
        )

        if self.subtitle_align == "왼쪽":
            align = Qt.AlignLeft

        elif self.subtitle_align == "오른쪽":
            align = Qt.AlignRight

        else:
            align = Qt.AlignCenter

        painter.drawText(
            20,
            self.subtitle_y,
            self.width() - 40,
            30,
            align,
            self.subtitle
        )

        # -------------------------
        # 하단 정보
        # -------------------------
        painter.setPen(QColor("#222222"))

        painter.setFont(
            QFont(
                self.info_font,
                self.info_size
            )
        )

        if self.info_align == "왼쪽":
            flags = Qt.AlignLeft | Qt.AlignVCenter

        elif self.info_align == "오른쪽":
            flags = Qt.AlignRight | Qt.AlignVCenter

        else:
            flags = Qt.AlignHCenter | Qt.AlignVCenter

        y = self.info_y

        for label, value in self.items:

            label = label.strip()
            value = value.strip()

            # 항목과 내용이 모두 비어 있으면
            # 아무것도 그리지 않고 빈 줄로 사용
            if not label and not value:
                y += self.info_spacing
                continue

            painter.drawText(
                20,
                y,
                self.width() - 40,
                30,
                flags,
                f"{label} : {value}"
            )

            y += self.info_spacing

    def mousePressEvent(self, event):

        # 제목 영역을 클릭했는지 확인
        title_top = self.title_y
        title_bottom = self.title_y + 40

        if title_top <= event.position().y() <= title_bottom:

            self.dragging = True
            self.drag_target = "title"

            self.drag_offset = (
                event.position().y()
                - self.title_y
            )

        # 부제목 영역을 클릭했는지 확인
        subtitle_top = self.subtitle_y
        subtitle_bottom = self.subtitle_y + 30

        if subtitle_top <= event.position().y() <= subtitle_bottom:

            self.dragging = True
            self.drag_target = "subtitle"

            self.drag_offset = (
                event.position().y()
                - self.subtitle_y
            )

        # 하단 정보 영역을 클릭했는지 확인
        if self.items:

            info_top = self.info_y
            info_bottom = (
                self.info_y
                + (len(self.items) - 1) * self.info_spacing
                + 30
            )

            if info_top <= event.position().y() <= info_bottom:

                self.dragging = True
                self.drag_target = "info"

                self.drag_offset = (
                    event.position().y()
                    - self.info_y
                )

        # 그림 영역을 클릭했는지 확인
        if self.image and not self.image.isNull():

            if self.image_mode == "logo":

                base = 120
                size = int(base * self.image_size / 100)

                pix = self.image.scaled(
                    size,
                    size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                margin = 20

                if self.image_align == "왼쪽":
                    image_x = margin

                elif self.image_align == "가운데":
                    image_x = (self.width() - pix.width()) // 2

                elif self.image_align == "오른쪽":
                    image_x = self.width() - pix.width() - margin

                else:
                    image_x = (self.width() - pix.width()) // 2

                mouse_x = event.position().x()
                mouse_y = event.position().y()

                if (
                    image_x <= mouse_x <= image_x + pix.width()
                    and
                    self.image_y <= mouse_y <= self.image_y + pix.height()
                ):
                    self.dragging = True
                    self.drag_target = "image"

                    self.drag_offset = (
                        mouse_y - self.image_y
                    )

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self.dragging and self.drag_target == "title":

            self.title_y = int(
                event.position().y() - self.drag_offset
            )

            self.update()

            self.positionChanged.emit(
                "title",
                self.title_y
            )

        elif self.dragging and self.drag_target == "subtitle":

            self.subtitle_y = int(
                event.position().y() - self.drag_offset
            )

            self.update()

            self.positionChanged.emit(
                "subtitle",
                self.subtitle_y
            )

        elif self.dragging and self.drag_target == "info":

            self.info_y = int(
                event.position().y() - self.drag_offset
            )

            self.update()

            self.positionChanged.emit(
                "info",
                self.info_y
            )

        elif self.dragging and self.drag_target == "image":

            self.image_y = int(
                event.position().y() - self.drag_offset
            )

            self.update()

            self.positionChanged.emit(
                "image",
                self.image_y
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        self.dragging = False
        self.drag_target = None

        super().mouseReleaseEvent(event)