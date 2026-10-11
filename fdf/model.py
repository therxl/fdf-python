from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int
    color: str | None = None

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y
        yield self.z


@dataclass
class Map:
    points: list[list[Point]] = field(default_factory=list)

    def __iter__(self) -> Iterator[Point]:
        for row in self.points:
            yield from row

    def __len__(self) -> int:
        return sum(len(row) for row in self.points)

    @property
    def width(self) -> int:
        return len(self.points[0]) if self.points else 0

    @property
    def height(self) -> int:
        return len(self.points)

    def get(self, x: int, y: int) -> Point | None:
        if 0 <= y < len(self.points) and 0 <= x < len(self.points[y]):
            return self.points[y][x]
        return None

    def neighbors(self, x: int, y: int) -> tuple[Point, ...]:
        result: list[Point] = []
        if x + 1 < self.width:
            result.append(self.points[y][x + 1])
        if y + 1 < self.height:
            result.append(self.points[y + 1][x])
        if x - 1 >= 0:
            result.append(self.points[y][x - 1])
        if y - 1 >= 0:
            result.append(self.points[y - 1][x])
        return tuple(result)
