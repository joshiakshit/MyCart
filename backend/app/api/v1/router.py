from fastapi import APIRouter

from app.api.v1 import auth, health, search, accounts, products, prices

v1_router = APIRouter()

v1_router.include_router(health.router, tags=["health"])
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
v1_router.include_router(search.router, prefix="/search", tags=["search"])
v1_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
v1_router.include_router(products.router, prefix="/products", tags=["products"])
v1_router.include_router(prices.router, prefix="/prices", tags=["prices"])
