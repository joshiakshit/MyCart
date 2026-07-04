from fastapi import APIRouter, Query

router = APIRouter()


@router.get("")
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    platforms: str = Query("blinkit,zepto", description="Comma-separated platform names"),
):
    platform_list = [p.strip() for p in platforms.split(",")]

    # TODO: wire up SearchService.search_all()
    return {
        "query": q,
        "platforms_queried": platform_list,
        "results": [],
        "platform_status": {p: {"status": "not_implemented"} for p in platform_list},
    }
