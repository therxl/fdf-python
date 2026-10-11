from pathlib import Path

import pytest

from fdf.exceptions import MapFormatError
from fdf.parser import parse_map

ROOT = Path(__file__).resolve().parents[1]


def test_elem_map_parses() -> None:
    data = parse_map(ROOT / "maps" / "elem.fdf")
    assert data.height == 5
    assert data.width == 5
    assert len(data) == 25
    assert data.get(2, 2).z == 5


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("7", 7),
        ("-3", -3),
        ("2,0xFF8800", 2),
        ("1,0xff", 1),
    ],
)
def test_parse_values(value: str, expected: int) -> None:
    row = f"{value} 0"
    path = ROOT / "tmp_map.fdf"
    path.write_text(row, encoding="utf-8")
    try:
        data = parse_map(path)
        assert data.points[0][0].z == expected
    finally:
        path.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "bad_file",
    [
        ROOT / "maps" / "bad" / "non_integer.fdf",
        ROOT / "maps" / "bad" / "bad_color.fdf",
        ROOT / "maps" / "bad" / "row_length.fdf",
        ROOT / "maps" / "bad" / "empty.fdf",
    ],
)
def test_bad_maps_raise_map_format_error(bad_file: Path) -> None:
    with pytest.raises(MapFormatError):
        parse_map(bad_file)
