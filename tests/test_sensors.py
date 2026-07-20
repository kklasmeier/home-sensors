from api.routes.sensors import _status_color


def test_status_color_green():
    assert _status_color(0) == "Green"
    assert _status_color(180) == "Green"


def test_status_color_yellow():
    assert _status_color(181) == "Yellow"
    assert _status_color(600) == "Yellow"


def test_status_color_red():
    assert _status_color(601) == "Red"
