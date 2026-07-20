"""Shared pytest fixtures."""

from contextlib import contextmanager
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

ROUTE_MODULES = (
    "api.routes.sensors",
    "api.routes.garage",
    "api.routes.sump_pump",
    "api.routes.hvac",
)


@pytest.fixture
def client():
    with patch("api.main.check_database_connection", return_value=True):
        from api.main import app

        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture
def mock_db_connection():
    """Patch get_connection in all route modules."""
    active_patches: list = []

    def configure(
        fetchall=None,
        fetchone=None,
        fetchone_sequence=None,
        callproc_results=None,
    ):
        nonlocal active_patches
        for p in active_patches:
            p.stop()
        active_patches = []

        cursor = MagicMock()
        if fetchall is not None:
            cursor.fetchall.return_value = fetchall
        if fetchone is not None:
            cursor.fetchone.return_value = fetchone
        if fetchone_sequence is not None:
            cursor.fetchone.side_effect = fetchone_sequence
        if callproc_results is not None:
            result_cursor = MagicMock()
            result_cursor.fetchall.return_value = callproc_results
            cursor.stored_results.return_value = [result_cursor]

        conn = MagicMock()
        conn.cursor.return_value = cursor

        @contextmanager
        def get_connection():
            yield conn

        for module in ROUTE_MODULES:
            p = patch(f"{module}.get_connection", get_connection)
            p.start()
            active_patches.append(p)

        return cursor

    yield configure

    for p in active_patches:
        p.stop()


@pytest.fixture
def garage_db_rows():
    now = datetime(2026, 7, 19, 21, 0, 0)
    earlier = datetime(2026, 7, 19, 18, 0, 0)
    return [
        {"2Door": "UP", "reading_dttm": now},
        {"reading_dttm": earlier},
        {"1Door": "DOWN", "reading_dttm": now},
        {"reading_dttm": earlier},
    ]
