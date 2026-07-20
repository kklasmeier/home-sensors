from decimal import Decimal
from typing import Any


def php_json_value(value: Any) -> Any:
    """Match PHP mysqli/json_encode scalar formatting where possible."""
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, bytes):
        return value.decode()
    return value


def php_json_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: php_json_value(val) for key, val in row.items()}


def php_json_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [php_json_row(row) for row in rows]
