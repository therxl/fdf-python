from pathlib import Path

from fdf.exceptions import MapFormatError
from fdf.model import Map, Point
from fdf.parser import parse_map
from fdf.projection import Camera


def test_public_parser_and_model() -> None:
    root = Path(__file__).resolve().parents[1]
    parsed = parse_map(root / "maps" / "elem.fdf")
    assert isinstance(parsed, Map)
    assert len(parsed) == 25
    assert parsed.get(0, 0).z == 0
    assert parsed.get(2, 2).z == 5


def test_public_projection() -> None:
    camera = Camera()
    point = Point(0, 0, 0)
    assert camera.project(point) == (0.0, 0.0)
    camera.fit(Map([[Point(0, 0, 0), Point(1, 0, 0)]]), 200, 200)
    assert camera.scale > 0


def test_public_error() -> None:
    root = Path(__file__).resolve().parents[1]
    try:
        parse_map(root / "maps" / "bad" / "non_integer.fdf")
    except MapFormatError:
        return
    raise AssertionError("MapFormatError was not raised")
