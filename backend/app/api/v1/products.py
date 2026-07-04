from fastapi import APIRouter

router = APIRouter()


@router.get("/{platform}/{product_id}")
async def get_product(platform: str, product_id: str):
    # TODO: fetch product details via adapter
    return {
        "platform": platform,
        "product_id": product_id,
        "detail": None,
        "message": "not implemented",
    }
