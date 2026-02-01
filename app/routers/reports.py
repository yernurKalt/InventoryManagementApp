from fastapi import APIRouter, Depends

from app.api.deps import require_admin
from app.models.user import UserModel
from app.schemas.reports import ReportGenerateRequest


router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.post("/generate")
async def generate_report(report: ReportGenerateRequest, admin_user: UserModel = Depends(require_admin)):
    pass