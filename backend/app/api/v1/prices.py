from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/history")
async def price_history(
    platform: str = Query(...),
    product_id: str = Query(...),
    days: int = Query(30, ge=1, le=365),
):
    # TODO: query price_snapshots table
    return {
        "platform": platform,
        "product_id": product_id,
        "days": days,
        "history": [],
    }
