from __future__ import annotations

from pathlib import Path

from .exceptions import MapFormatError
from .model import Map, Point


def _parse_color(raw_color: str) -> str:
    if not raw_color:
        raise ValueError("пустой цвет")
    if not raw_color.startswith("0x") and not raw_color.startswith("0X"):
        raise ValueError("цвет должен начинаться с 0x")
    value = raw_color[2:]
    if not value or len(value) > 6:
        raise ValueError("цвет должен содержать от 1 до 6 шестнадцатеричных цифр")
    try:
        parsed = int(value, 16)
    except ValueError as exc:  # pragma: no cover - defensive path
        raise ValueError("некорректный цвет") from exc
    return f"#{parsed:06X}"


def parse_map(path: str | Path) -> Map:
    file_path = Path(path)
    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл не найден: {file_path}") from exc

    lines = content.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise MapFormatError("строка 1, колонка 1: пустой файл")

    rows: list[list[Point]] = []
    expected_width: int | None = None

    for row_index, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        cells = raw_line.split()
        if expected_width is None:
            expected_width = len(cells)
        elif len(cells) != expected_width:
            raise MapFormatError(
                f"строка {row_index}, колонка {len(cells) + 1}: "
                "строки имеют разную длину"
            )

        parsed_row: list[Point] = []
        for column_index, token in enumerate(cells, start=1):
            value_part = token
            color_part: str | None = None
            normalized_color: str | None = None
            if "," in token:
                parts = token.split(",", 1)
                if len(parts) != 2 or not parts[0] or not parts[1]:
                    raise MapFormatError(
                        f"строка {row_index}, колонка {column_index}: '{token}' — некорректный цвет"
                    )
                value_part, color_part = parts
                try:
                    normalized_color = _parse_color(color_part)
                except ValueError:
                    raise MapFormatError(
                        f"строка {row_index}, колонка {column_index}: '{token}' — некорректный цвет"
                    ) from None
            try:
                value = int(value_part)
            except ValueError:
                raise MapFormatError(
                    f"строка {row_index}, колонка {column_index}: '{token}' — не целое число"
                ) from None
            parsed_row.append(
                Point(
                    x=column_index - 1,
                    y=row_index - 1,
                    z=value,
                    color=normalized_color if color_part is not None else None,
                )
            )
        rows.append(parsed_row)

    if not rows:
        raise MapFormatError("строка 1, колонка 1: пустой файл")

    return Map(rows)
