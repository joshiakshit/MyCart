import asyncio
import time

from app.adapters import get_adapter, get_all_adapters
from app.schemas.common import (
    ComparedProduct,
    PlatformPrice,
    PlatformProduct,
    PlatformStatus,
    SearchResponse,
)


class SearchService:
    async def search_all(
        self,
        query: str,
        platforms: list[str],
        auth_tokens: dict[str, str],
        lat: float,
        lng: float,
    ) -> SearchResponse:
        tasks = {}
        for platform in platforms:
            token = auth_tokens.get(platform)
            if not token:
                continue
            adapter = get_adapter(platform)
            tasks[platform] = self._timed_search(adapter, query, token, lat, lng)

        results_by_platform: dict[str, list[PlatformProduct]] = {}
        status_by_platform: dict[str, PlatformStatus] = {}

        gathered = await asyncio.gather(
            *[tasks[p] for p in tasks],
            return_exceptions=True,
        )

        for platform, result in zip(tasks.keys(), gathered):
            if isinstance(result, Exception):
                status_by_platform[platform] = PlatformStatus(
                    status="error", message=str(result)
                )
                results_by_platform[platform] = []
            else:
                products, elapsed_ms = result
                status_by_platform[platform] = PlatformStatus(
                    status="ok", response_time_ms=elapsed_ms
                )
                results_by_platform[platform] = products

        for p in platforms:
            if p not in status_by_platform:
                status_by_platform[p] = PlatformStatus(
                    status="skipped", message="no auth token"
                )

        compared = self._merge_results(results_by_platform)

        return SearchResponse(
            query=query,
            results=compared,
            platform_status=status_by_platform,
        )

    async def _timed_search(self, adapter, query, token, lat, lng):
        start = time.monotonic()
        products = await adapter.search(query, token, lat, lng)
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return products, elapsed_ms

    def _merge_results(
        self, results_by_platform: dict[str, list[PlatformProduct]]
    ) -> list[ComparedProduct]:
        all_products: list[ComparedProduct] = []

        for platform, products in results_by_platform.items():
            for p in products:
                price_entry = PlatformPrice(
                    platform=p.platform,
                    price=p.price,
                    mrp=p.mrp,
                    discount_pct=p.discount_pct,
                    in_stock=p.in_stock,
                    delivery_eta_minutes=p.delivery_eta_minutes,
                    platform_product_id=p.platform_product_id,
                )

                matched = self._find_match(all_products, p)
                if matched:
                    matched.prices.append(price_entry)
                    matched.best_price = min(matched.prices, key=lambda x: x.price)
                else:
                    all_products.append(
                        ComparedProduct(
                            name=p.name,
                            brand=p.brand,
                            unit_quantity=p.unit_quantity,
                            image_url=p.image_url,
                            prices=[price_entry],
                            best_price=price_entry,
                        )
                    )

        return all_products

    def _find_match(
        self, existing: list[ComparedProduct], product: PlatformProduct
    ) -> ComparedProduct | None:
        for item in existing:
            if (
                item.name.lower() == product.name.lower()
                and item.brand == product.brand
                and item.unit_quantity == product.unit_quantity
            ):
                return item
        return None
