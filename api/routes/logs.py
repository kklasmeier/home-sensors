from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from api.config import settings

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/collect", response_class=PlainTextResponse)
def collect_log():
    log_path = Path(settings.collector_log_path)
    if not log_path.is_file():
        raise HTTPException(status_code=404, detail="Log file not found")
    return log_path.read_text(encoding="utf-8", errors="replace")
