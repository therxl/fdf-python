from __future__ import annotations

import os
from pathlib import Path

import pygame

from fdf.app import App

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


ROOT = Path(__file__).resolve().parent
SCREENSHOT_SIZE = (800, 600)
MAP_SCREENSHOTS = (
    ("maps/elem.fdf", "docs/screenshot.png"),
    ("maps/cigarette_pack.fdf", "docs/cigarette_pack.png"),
)


def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode(SCREENSHOT_SIZE)
    for map_path, image_path in MAP_SCREENSHOTS:
        App(str(ROOT / map_path), *SCREENSHOT_SIZE).draw(surface)
        output_path = ROOT / image_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pygame.image.save(surface, output_path)
        print(f"created {output_path.relative_to(ROOT)}")
    pygame.quit()


if __name__ == "__main__":
    main()
