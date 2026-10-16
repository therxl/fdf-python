from __future__ import annotations

import math

from .model import Map, Point


def lerp_color(color_a: str, color_b: str, t: float) -> str:
    if not (0.0 <= t <= 1.0):
        raise ValueError("t must be between 0 and 1")

    def channel(a: str, b: str) -> int:
        return int((1.0 - t) * int(a, 16) + t * int(b, 16))

    a_rgb = [color_a[i : i + 2] for i in range(1, 7, 2)]
    b_rgb = [color_b[i : i + 2] for i in range(1, 7, 2)]
    result = "#" + "".join(f"{channel(x, y):02X}" for x, y in zip(a_rgb, b_rgb))
    return result


def height_color(z: int, z_min: int, z_max: int) -> str:
    if z_max == z_min:
        return "#00BFFF"

    t = (z - z_min) / (z_max - z_min)
    palette = [
        (0x1B, 0x6D, 0xFF),
        (0x00, 0xD5, 0x6C),
        (0xFF, 0xD6, 0x00),
        (0xFF, 0x4D, 0x4D),
    ]
    if t <= 0:
        return "#1B6DFF"
    if t >= 1:
        return "#FF4D4D"

    scaled = t * (len(palette) - 1)
    index = int(scaled)
    next_index = min(index + 1, len(palette) - 1)
    local_t = scaled - index
    left = palette[index]
    right = palette[next_index]
    channels = []
    for left_channel, right_channel in zip(left, right):
        channels.append(round(left_channel + (right_channel - left_channel) * local_t))
    return "#" + "".join(f"{channel:02X}" for channel in channels)


class Camera:
    def __init__(self, angle: float = 0.0, z_scale: float = 1.0) -> None:
        self.angle = angle
        self.z_scale = z_scale
        self.top_view = False
        self.scale = 1.0
        self._fit_scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

    def _project_raw(self, point: Point) -> tuple[float, float]:
        theta = math.radians(self.angle)
        rotated_x = point.x * math.cos(theta) - point.y * math.sin(theta)
        rotated_y = point.x * math.sin(theta) + point.y * math.cos(theta)

        if self.top_view:
            return rotated_x, rotated_y

        x_offset = (rotated_x - rotated_y) * math.cos(math.radians(30.0))
        y_offset = (rotated_x + rotated_y) * math.sin(math.radians(30.0)) - point.z * self.z_scale
        return x_offset, y_offset

    def project(self, point: Point) -> tuple[float, float]:
        x_value, y_value = self._project_raw(point)
        return x_value * self.scale + self.offset_x, y_value * self.scale + self.offset_y

    def pan(self, dx: float, dy: float) -> None:
        self.offset_x += dx
        self.offset_y += dy

    def zoom(self, factor: float, anchor_x: float, anchor_y: float) -> None:
        if factor <= 0:
            raise ValueError("zoom factor must be positive")

        new_scale = min(max(self.scale * factor, self._fit_scale * 0.1), self._fit_scale * 10.0)
        applied_factor = new_scale / self.scale
        self.offset_x = anchor_x - (anchor_x - self.offset_x) * applied_factor
        self.offset_y = anchor_y - (anchor_y - self.offset_y) * applied_factor
        self.scale = new_scale

    def fit(self, map_data: Map, width: float, height: float) -> tuple[float, float, float]:
        if not map_data.points:
            self.scale = 1.0
            self._fit_scale = self.scale
            self.offset_x = 0.0
            self.offset_y = 0.0
            return self.scale, self.offset_x, self.offset_y

        raw_points = [self._project_raw(point) for point in map_data]
        xs = [value[0] for value in raw_points]
        ys = [value[1] for value in raw_points]
        width_span = max(xs) - min(xs)
        height_span = max(ys) - min(ys)
        width_span = max(width_span, 1.0)
        height_span = max(height_span, 1.0)

        self.scale = min(width / width_span, height / height_span) * 0.9
        self._fit_scale = self.scale
        center_x = (min(xs) + max(xs)) / 2.0
        center_y = (min(ys) + max(ys)) / 2.0
        self.offset_x = width / 2.0 - center_x * self.scale
        self.offset_y = height / 2.0 - center_y * self.scale
        return self.scale, self.offset_x, self.offset_y
