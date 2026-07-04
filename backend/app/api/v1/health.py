from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/platforms/status")
async def platform_status():
    return {
        "platforms": {
            "blinkit": {"status": "unknown", "message": "adapter not configured yet"},
            "zepto": {"status": "unknown", "message": "adapter not configured yet"},
        }
    }
