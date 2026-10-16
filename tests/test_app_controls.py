import pygame

from fdf.app import App
from fdf.parser import parse_map


def create_app() -> App:
    return App(parse_map("maps/elem.fdf"))


def test_v_toggles_top_view() -> None:
    app = create_app()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_v)

    app._handle_control(event, (0, 0))
    assert app.camera.top_view
    app._handle_control(event, (0, 0))
    assert not app.camera.top_view


def test_left_and_right_rotate_around_centered_map() -> None:
    app = create_app()
    start_angle = app.camera.angle

    app._handle_control(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT), (0, 0))
    assert app.camera.angle == start_angle - 5.0
    app._handle_control(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), (0, 0))
    assert app.camera.angle == start_angle

    projected = [app.camera.project(point) for point in app.map]
    xs = [point[0] for point in projected]
    ys = [point[1] for point in projected]
    assert (min(xs) + max(xs)) / 2 == app.width / 2
    assert (min(ys) + max(ys)) / 2 == app.height / 2


def test_up_and_down_do_not_pan_or_rotate() -> None:
    app = create_app()
    start_angle = app.camera.angle
    start_offset = (app.camera.offset_x, app.camera.offset_y)

    app._handle_control(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP), (0, 0))
    app._handle_control(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN), (0, 0))

    assert app.camera.angle == start_angle
    assert (app.camera.offset_x, app.camera.offset_y) == start_offset


def test_mouse_wheel_zoom_anchors_at_pointer() -> None:
    app = create_app()
    point = app.map.points[2][2]
    pointer = app.camera.project(point)
    start_scale = app.camera.scale

    app._handle_control(
        pygame.event.Event(pygame.MOUSEWHEEL, y=1, flipped=False),
        (round(pointer[0]), round(pointer[1])),
    )

    assert app.camera.scale > start_scale
    projected = app.camera.project(point)
    assert abs(projected[0] - pointer[0]) < 1.0
    assert abs(projected[1] - pointer[1]) < 1.0