import os
import tempfile
import fitz
from pathlib import Path
from datetime import datetime
from ui.utils.page_number_helper import calculate_position

today = datetime.now().strftime("%Y.%m.%d")

# ==========================
# PDF 설정
# ==========================

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_RIGHT_MARGIN = 40

# 목차 한 페이지에 표시할 항목 수
TOC_ENTRIES_PER_PAGE = 20

TOC_TITLE_Y = 90 

TOC_START_Y = 110
TOC_LINE_HEIGHT = 28
TOC_TITLE_MAX_WIDTH = 270
TOC_TITLE_SIZE = 14

# 목차 좌우 여백
PAGE_SIDE_MARGIN = 60

# ==========================
# 페이지 번호 설정
# ==========================

PAGE_NUMBER_START = 1
PAGE_NUMBER_SIZE = 10
PAGE_NUMBER_MARGIN = 20
PAGE_NUMBER_POSITION = "center"   # left / center / right

def draw_text(page, text, y, fontname, fontsize, align=1):
    """
    텍스트 출력

    align
        0 : 왼쪽
        1 : 가운데
        2 : 오른쪽
    """
    print(f"text={text}, align={align}")

    rect = fitz.Rect(
        LEFT_RIGHT_MARGIN,
        y,
        page.rect.width - LEFT_RIGHT_MARGIN,
        y + 50
    )

    page.insert_textbox(
        rect,
        text,
        fontname=fontname,
        fontsize=fontsize,
        align=align
    )

def get_align_value(text):
    if text == "왼쪽":
        return 0
    elif text == "오른쪽":
        return 2
    return 1

def create_cover_page(page, cover_settings):
    """표지 생성"""

    page_width = page.rect.width
    page_height = page.rect.height

    # Windows 맑은 고딕 폰트
    font_path = Path(__file__).parent / "assets" / "fonts" / "malgun.ttf"

    # 폰트 등록
    page.insert_font(
        fontname="malgun",
        fontfile=font_path
    )

    print("===== COVER SETTINGS =====")
    print(cover_settings)

    # -------------------------
    # 그림 출력
    # -------------------------
    image_path = cover_settings.get("image_path", "")

    if image_path:

        image_size = cover_settings.get("image_size", 100)
        image_y = cover_settings.get("image_y", 20)

        base = 120
        size = base * image_size / 100

        margin = 40

        image_align = cover_settings.get("image_align", "가운데")

        if image_align == "왼쪽":
            x = margin

        elif image_align == "가운데":
            x = (page_width - size) / 2

        elif image_align == "오른쪽":
            x = page_width - size - margin

        else:
            x = (page_width - size) / 2

        rect = fitz.Rect(
            x,
            image_y,
            x + size,
            image_y + size
        )

        page.insert_image(
            rect,
            filename=image_path
        )

    # 제목 출력
    align = get_align_value(
        cover_settings.get("title_align", "가운데")
    )

    draw_text(
        page,
        cover_settings["title"],
        cover_settings.get("title_y", 220),
        "malgun",
        cover_settings["title_size"],
        align
    )

    align = get_align_value(
        cover_settings.get("subtitle_align", "가운데")
    )

    draw_text(
        page,
        cover_settings["subtitle"],
        cover_settings.get("subtitle_y", 270),
        "malgun",
        cover_settings["subtitle_size"],
        align
    )

    # -------------------------
    # 하단 정보 출력
    # -------------------------

    info_align = get_align_value(
        cover_settings.get("info_align", "왼쪽")
    )

    y = cover_settings.get("info_y", 500)

    for item in cover_settings["items"]:

        text = f'{item["label"]} : {item["value"]}'

        draw_text(
            page,
            text,
            y,
            "malgun",
            cover_settings["info_size"],
            info_align
        )

        y += cover_settings.get("info_spacing", 28)

def shorten_toc_title(title, font, max_width):
    """긴 목차 제목을 줄임표가 붙은 한 줄로 줄인다."""

    if font.text_length(title, fontsize=TOC_TITLE_SIZE) <= max_width:
        return title

    ellipsis = "..."
    shortened_title = title

    while shortened_title:
        candidate = shortened_title.rstrip() + ellipsis

        if font.text_length(
            candidate,
            fontsize=TOC_TITLE_SIZE
        ) <= max_width:
            return candidate

        shortened_title = shortened_title[:-1]

    return ellipsis


def create_toc_pages(
    document,
    toc_items,
    body_start_pages,
    start_number
):
    """목차 페이지 생성"""

    font_path = Path(__file__).parent / "assets" / "fonts" / "malgun.ttf"

    toc_font = fitz.Font(fontfile=str(font_path))

    # 목차에 출력할 행 수(section + pdf)
    total_rows = len(toc_items)

    toc_page_count = max(
        1,
        (total_rows + TOC_ENTRIES_PER_PAGE - 1)
        // TOC_ENTRIES_PER_PAGE
    )

    pdf_index = 0

    for toc_page_index in range(toc_page_count):

        page = document.new_page(
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        page.insert_font(
            fontname="malgun",
            fontfile=font_path
        )

        # 첫 번째 목차 페이지에만 "목차" 출력
        if toc_page_index == 0:

            draw_text(
                page,
                "목 차",
                TOC_TITLE_Y,
                "malgun",
                28
            )

        first = toc_page_index * TOC_ENTRIES_PER_PAGE
        last = first + TOC_ENTRIES_PER_PAGE

        page_items = toc_items[first:last]

        if toc_page_index == 0:
            y = TOC_START_Y + TOC_LINE_HEIGHT
        else:
            y = TOC_START_Y

        for item in page_items:

            # ----------------------------
            # 큰 제목
            # ----------------------------
            if item["type"] == "section":

                # 첫 번째 장이 아니라면 위쪽에 여백 추가
                if y != TOC_START_Y:
                    y += TOC_LINE_HEIGHT * 0.7

                page.insert_text(
                    (PAGE_SIDE_MARGIN, y),
                    item["title"],
                    fontname="malgun",
                    fontsize=16
                )

                y += TOC_LINE_HEIGHT
                continue

            # ----------------------------
            # PDF 제목
            # ----------------------------

            title = shorten_toc_title(
                item["title"],
                toc_font,
                TOC_TITLE_MAX_WIDTH - 20
            )

            title_x = PAGE_SIDE_MARGIN + 20

            title_width = toc_font.text_length(
                title,
                TOC_TITLE_SIZE
            )

            display_page = (
                start_number
                + body_start_pages[pdf_index]
                - 1
            )

            page_text = str(display_page)

            page_width = fitz.get_text_length(
                page_text,
                fontname="helv",
                fontsize=14
            )

            page_right = PAGE_WIDTH - PAGE_SIDE_MARGIN
            page_left = page_right - page_width

            page.insert_text(
                (title_x, y),
                title,
                fontname="malgun",
                fontsize=TOC_TITLE_SIZE
            )

            dot_start = title_x + title_width + 10
            dot_end = page_left - 12

            dot_width = fitz.get_text_length(
                ".",
                fontname="helv",
                fontsize=12
            )

            dot_count = max(
                0,
                int((dot_end - dot_start) / dot_width)
            )

            page.insert_text(
                (dot_start, y),
                "." * dot_count,
                fontname="helv",
                fontsize=12
            )

            page.insert_text(
                (page_left, y),
                page_text,
                fontname="helv",
                fontsize=14
            )

            pdf_index += 1
            y += TOC_LINE_HEIGHT

    return toc_page_count

def add_page_number(
    page,
    page_no,
    page_number_settings,
    pdf_page_index
):

    print(page_number_settings)
    
    """페이지 번호 출력"""

    if page_number_settings["use_dash"]:
        text = f"-{page_no}-"
    else:
        text = str(page_no)

    fontsize = page_number_settings["font_size"]

    # 대략적인 글자 폭 계산
    text_width = len(text) * fontsize * 0.55

    h_margin = page_number_settings["horizontal_margin"]
    v_margin = page_number_settings["vertical_margin"]

    # 사용할 위치 결정
    if page_number_settings["same_position"]:
        position = page_number_settings["odd_position"]
    else:
        if pdf_page_index % 2 == 0:
            position = page_number_settings["even_position"]
        else:
            position = page_number_settings["odd_position"]

    # X 위치
    if position in (0, 3):          # 좌
        x = h_margin

    elif position in (1, 4):        # 가운데
        x = (PAGE_WIDTH - text_width) / 2

    else:                           # 우
        x = PAGE_WIDTH - h_margin - text_width

    # Y 위치
    if position in (0, 1, 2):       # 위
        y = v_margin + fontsize

    else:                           # 아래
        y = PAGE_HEIGHT - v_margin

    # 선택한 글꼴 등록
    font_path = (
        Path(__file__).parent
        / "assets"
        / "fonts"
        / "malgun.ttf"
    )

    page.insert_font(
        fontname="malgun",
        fontfile=str(font_path)
    )

    page.insert_text(
        fitz.Point(x, y),
        text,
        fontname="malgun",
        fontsize=fontsize,
    )

def get_pdf_page_counts(pdf_list):
    """각 PDF의 페이지 수를 확인한다."""

    page_counts = []

    for pdf_path in pdf_list:
        with fitz.open(pdf_path) as document:
            page_counts.append(document.page_count)

    return page_counts


def calculate_body_start_pages(page_counts):

    """각 PDF가 시작되는 본문 페이지 번호를 계산한다."""

    start_pages = []
    next_page = PAGE_NUMBER_START

    for page_count in page_counts:
        start_pages.append(next_page)
        next_page += page_count

    return start_pages


def report_progress(progress_callback, value):
    """진행률 콜백이 있으면 현재 값을 전달한다."""

    if progress_callback:
        progress_callback(value)


def report_log(log_callback, message):
    """로그 콜백이 있으면 현재 작업 내용을 전달한다."""

    if log_callback:
        log_callback(message)


def append_pdf_files(
    merged,
    pdf_list,
    first_body_page_index,
    total_body_pages,
    page_number_settings,
    progress_callback=None,
    log_callback=None
):
    """PDF를 순서대로 추가하고 연속 페이지 번호를 표시한다."""

    current_page_index = first_body_page_index
    book_page_number = page_number_settings["start_number"]
    completed_pages = 0

    for file_index, pdf_path in enumerate(pdf_list, start=1):
        filename = Path(pdf_path).name
        report_log(
            log_callback,
            f"PDF 병합 중 ({file_index}/{len(pdf_list)}) : {filename}"
        )

        with fitz.open(pdf_path) as document:
            merged.insert_pdf(document)

            for page_offset in range(document.page_count):
                page = merged[current_page_index + page_offset]
                add_page_number(
                    page,
                    book_page_number,
                    page_number_settings,
                    current_page_index + page_offset
                )
                book_page_number += 1
                completed_pages += 1

                # 본문 병합 구간은 전체 진행률의 20%부터 90%까지 사용한다.
                progress = 20 + int(
                    completed_pages / total_body_pages * 70
                )
                report_progress(progress_callback, progress)

            current_page_index += document.page_count


def create_bookmarks(titles, body_start_pages, first_body_page_index):
    """본문의 실제 위치를 가리키는 PDF 북마크를 만든다."""

    bookmarks = []

    for title, body_page in zip(titles, body_start_pages):
        pdf_page = first_body_page_index + body_page
        bookmarks.append([1, title, pdf_page])

    return bookmarks


def validate_merge_inputs(pdf_list, toc_items):
    """병합 전에 파일 목록과 목차 정보를 확인한다."""

    if not pdf_list:
        raise ValueError("병합할 PDF 파일이 없습니다.")

    # PDF 항목만 센다.
    pdf_count = sum(
        1
        for item in toc_items
        if item["type"] == "pdf"
    )

    if len(pdf_list) != pdf_count:
        raise ValueError("PDF 파일 수와 목차 정보가 일치하지 않습니다.")

    for pdf_path in pdf_list:
        path = Path(pdf_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"PDF 파일을 찾을 수 없습니다: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"PDF 파일만 병합할 수 있습니다: {path.name}"
            )

def validate_output_file(output_file, pdf_list):
    """출력 파일과 저장 폴더를 확인한다."""

    output_path = Path(output_file)
    output_folder = output_path.parent

    if output_path.suffix.lower() != ".pdf":
        raise ValueError("출력 파일의 확장자는 .pdf여야 합니다.")

    if not output_folder.is_dir():
        raise FileNotFoundError(
            f"출력 폴더를 찾을 수 없습니다: {output_folder}"
        )

    input_paths = {
        Path(pdf_path).resolve()
        for pdf_path in pdf_list
    }

    if output_path.resolve() in input_paths:
        raise ValueError("입력 PDF와 같은 경로에는 저장할 수 없습니다.")


def save_pdf_safely(document, output_file):
    """임시 파일에 먼저 저장한 뒤 완성된 PDF로 교체한다."""

    output_path = Path(output_file)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.stem}_",
        suffix=".pdf",
        dir=output_path.parent
    )
    os.close(file_descriptor)

    temporary_path = Path(temporary_name)
    temporary_path.unlink()

    try:
        document.save(temporary_path)
        os.replace(temporary_path, output_path)
    finally:
        # 저장 실패로 임시 파일이 남은 경우에만 정리한다.
        if temporary_path.exists():
            temporary_path.unlink()


def merge_pdf(
    toc_items,
    book_title,
    output_file,
    page_number_settings,
    cover_settings,
    progress_callback=None,
    log_callback=None
):
    """표지, 목차, 본문과 북마크를 하나의 PDF로 만든다."""

    print("PDF 병합 시작")
    report_log(log_callback, "PDF 병합을 시작합니다.")
    report_progress(progress_callback, 0)

    pdf_list = [
        item["path"]
        for item in toc_items
        if item["type"] == "pdf"
    ]

    titles = [
        item["title"]
        for item in toc_items
        if item["type"] == "pdf"
    ]

    merged = None

    try:
        validate_merge_inputs(pdf_list, toc_items)
        validate_output_file(output_file, pdf_list)

        report_log(log_callback, "PDF 페이지 정보를 확인합니다.")
        page_counts = get_pdf_page_counts(pdf_list)
        body_start_pages = calculate_body_start_pages(page_counts)
        total_body_pages = max(1, sum(page_counts))
        report_progress(progress_callback, 10)

        merged = fitz.open()

        # 첫 페이지에 표지를 만든다.
        report_log(log_callback, "표지를 생성합니다.")
        cover_page = merged.new_page(
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )
        create_cover_page(
            cover_page,
            cover_settings
        )

        # 제목 개수에 맞춰 목차 페이지를 만든다.
        toc_page_count = create_toc_pages(
            merged,
            toc_items,
            body_start_pages,
            page_number_settings["start_number"]
        )
        report_log(
            log_callback,
            f"목차 {toc_page_count}페이지를 생성했습니다."
        )
        report_progress(progress_callback, 20)

        first_body_page_index = 1 + toc_page_count

        append_pdf_files(
            merged,
            pdf_list,
            first_body_page_index,
            total_body_pages,
            page_number_settings,
            progress_callback,
            log_callback
        )

        report_log(log_callback, "PDF 북마크를 생성합니다.")
        bookmarks = create_bookmarks(
            titles,
            body_start_pages,
            first_body_page_index
        )
        merged.set_toc(bookmarks)
        report_progress(progress_callback, 95)

        report_log(log_callback, "완성된 PDF를 저장합니다.")
        save_pdf_safely(merged, output_file)
    except Exception as error:
        report_log(log_callback, f"오류가 발생했습니다: {error}")
        raise
    finally:
        if merged:
            merged.close()

    report_progress(progress_callback, 100)
    report_log(log_callback, "PDF 병합이 완료되었습니다.")
    print("PDF 병합 완료")
