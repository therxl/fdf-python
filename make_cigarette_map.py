from pathlib import Path

from fdf.parser import parse_map

width = 25
height = 45
center_x = width // 2

# Create empty map
rows = [[0 for _ in range(width)] for _ in range(height)]


def draw_line(x0: int, y0: int, x1: int, y1: int, value: int, thickness: int = 1) -> None:
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    steps = max(dx, dy, 1)
    for step in range(steps + 1):
        t = step / steps if steps else 0
        x = round(x0 + (x1 - x0) * t)
        y = round(y0 + (y1 - y0) * t)
        for yy in range(max(0, y - thickness), min(height, y + thickness + 1)):
            for xx in range(max(0, x - thickness), min(width, x + thickness + 1)):
                rows[yy][xx] = max(rows[yy][xx], value)


# Keep only the central box outlined in the reference.
pack_left = center_x - 5
pack_right = center_x + 5
pack_top = 18
pack_bottom = 33

# Front face
for y in range(pack_top, pack_bottom + 1):
    for x in range(pack_left, pack_right + 1):
        rows[y][x] = max(rows[y][x], 8)

# Top band to better define the pack
for y in range(pack_top, pack_top + 3):
    for x in range(pack_left + 1, pack_right):
        rows[y][x] = max(rows[y][x], 10)

# Side depth / visible edges
for y in range(pack_top, pack_bottom + 1):
    rows[y][pack_left] = max(rows[y][pack_left], 7)
    rows[y][pack_right] = max(rows[y][pack_right], 7)

# Thin chains rise from the two upper corners of the pack.
for start, end in [
    ((pack_left, pack_top), (4, 2)),
    ((pack_right, pack_top), (20, 2)),
]:
    draw_line(start[0], start[1], end[0], end[1], 6, thickness=0)

# Remove the inner filled rectangle that caused the green block.
# The pack remains outlined only.

out = Path('maps/cigarette_pack.fdf')
out.parent.mkdir(exist_ok=True)
with out.open('w', encoding='utf-8') as f:
    for row in rows:
        f.write(' '.join(str(v) for v in row) + '\n')

m = parse_map(out)
print(f'created {out}  size={m.width}x{m.height}  sample={m.get(center_x, 18).z}')
