from decimal import Decimal

from api.serialize import php_json_row, php_json_value


def test_php_json_value_decimal():
    assert php_json_value(Decimal("88.10")) == "88.10"
    assert php_json_value(Decimal("72")) == "72"


def test_php_json_value_passthrough():
    assert php_json_value("hello") == "hello"
    assert php_json_value(42) == 42


def test_php_json_row():
    row = {"temperature_f": Decimal("75.50"), "location": "Inside"}
    assert php_json_row(row) == {"temperature_f": "75.50", "location": "Inside"}
