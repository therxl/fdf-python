from __future__ import annotations

from collections.abc import Iterable

import pygame

from .model import Map, Point
from .parser import parse_map
from .projection import Camera, height_color, lerp_color

ZOOM_FACTOR = 1.1


class App:
    def __init__(self, map_data: Map | str, width: int = 800, height: int = 600) -> None:
        self.map = parse_map(map_data) if isinstance(map_data, str) else map_data
        self.width = width
        self.height = height
        self.camera = Camera()
        self.camera.fit(self.map, width, height)

    def _iter_edges(self) -> Iterable[tuple[Point, Point]]:
        for y, row in enumerate(self.map.points):
            for x, point in enumerate(row):
                if x + 1 < len(row):
                    yield point, row[x + 1]
                if y + 1 < len(self.map.points):
                    yield point, self.map.points[y + 1][x]

    def _color_for_point(self, point: Point) -> str:
        if point.color:
            return point.color
        z_values = [p.z for p in self.map]
        if not z_values:
            return "#FFFFFF"
        z_min = min(z_values)
        z_max = max(z_values)
        return height_color(point.z, z_min, z_max)

    def _draw_line(self, screen: pygame.Surface, start: tuple[float, float], end: tuple[float, float], color_a: str, color_b: str) -> None:
        distance = max(int(((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5), 1)
        steps = max(2, min(20, distance // 4))
        for step in range(steps + 1):
            t = step / steps if steps else 0.0
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            shade = lerp_color(color_a, color_b, t)
            pygame.draw.circle(screen, pygame.Color(shade), (round(x), round(y)), 1)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((12, 18, 28))
        for start, end in self._iter_edges():
            start_pos = self.camera.project(start)
            end_pos = self.camera.project(end)
            start_color = self._color_for_point(start)
            end_color = self._color_for_point(end)
            self._draw_line(screen, start_pos, end_pos, start_color, end_color)
        pygame.display.flip()

    def _handle_control(
        self,
        event: pygame.event.Event,
        mouse_pos: tuple[int, int],
    ) -> None:
        if event.type == pygame.MOUSEWHEEL:
            wheel_y = -event.y if getattr(event, "flipped", False) else event.y
            if wheel_y:
                self.camera.zoom(ZOOM_FACTOR**wheel_y, *mouse_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                self.camera.z_scale += 0.5
                self.camera.fit(self.map, self.width, self.height)
            elif event.key == pygame.K_MINUS:
                self.camera.z_scale = max(0.1, self.camera.z_scale - 0.5)
                self.camera.fit(self.map, self.width, self.height)
            elif event.key == pygame.K_LEFT:
                self.camera.angle -= 5.0
                self.camera.fit(self.map, self.width, self.height)
            elif event.key == pygame.K_RIGHT:
                self.camera.angle += 5.0
                self.camera.fit(self.map, self.width, self.height)
            elif event.key == pygame.K_v:
                self.camera.top_view = not self.camera.top_view
                self.camera.fit(self.map, self.width, self.height)

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("FdF")
        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.camera.fit(self.map, self.width, self.height)
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.camera.fit(self.map, self.width, self.height)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    self._handle_control(event, pygame.mouse.get_pos())

            self.draw(screen)
            clock.tick(60)

        pygame.quit()
