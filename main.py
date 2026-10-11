from __future__ import annotations

import sys
from pathlib import Path

from fdf.app import App
from fdf.exceptions import FdfError, MapFormatError
from fdf.parser import parse_map

USAGE = "Usage: python main.py <file.fdf>"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    file_path = Path(args[0])
    try:
        parse_map(file_path)
        app = App(str(file_path))
        app.run()
        return 0
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {file_path}", file=sys.stderr)
        return 1
    except (MapFormatError, FdfError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - final safety net for UI errors
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
