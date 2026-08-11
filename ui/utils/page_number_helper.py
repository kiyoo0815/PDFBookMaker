from PySide6.QtGui import QFontMetrics


def calculate_position(
    width,
    height,
    position,
    text,
    font,
    horizontal_margin,
    vertical_margin,
):
    """
    페이지 번호 위치 계산

    position
        0 : 좌상
        1 : 상단 가운데
        2 : 우상
        3 : 좌하
        4 : 하단 가운데
        5 : 우하
    """

    fm = QFontMetrics(font)

    text_width = fm.horizontalAdvance(str(text))
    ascent = fm.ascent()

    # 기준점
    if position == 0:
        x = horizontal_margin
        y = vertical_margin + ascent

    elif position == 1:
        x = (width - text_width) / 2
        y = vertical_margin + ascent

    elif position == 2:
        x = width - horizontal_margin - text_width
        y = vertical_margin + ascent

    elif position == 3:
        x = horizontal_margin
        y = height - vertical_margin

    elif position == 4:
        x = (width - text_width) / 2
        y = height - vertical_margin

    else:
        x = width - horizontal_margin - text_width
        y = height - vertical_margin

    return int(x), int(y)