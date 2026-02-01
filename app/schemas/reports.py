from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReportGenerateRequest(BaseModel):
    period_start: datetime
    period_end: datetime
    format: Optional[str] = None
    report_type: Optional[str] = None


class ReportOut(ReportGenerateRequest):
    id: int
    status: str
    file_path: Optional[str] = None
    created_at: datetime
    generated_at: Optional[datetime] = None
    error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)