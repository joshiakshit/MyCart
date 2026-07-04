from app.adapters.base import PlatformAdapter
from app.adapters.blinkit.client import BlinkitAdapter
from app.adapters.zepto.client import ZeptoAdapter

_adapters: dict[str, PlatformAdapter] = {}


def _init_adapters():
    global _adapters
    if not _adapters:
        _adapters = {
            "blinkit": BlinkitAdapter(),
            "zepto": ZeptoAdapter(),
        }


def get_adapter(platform: str) -> PlatformAdapter:
    _init_adapters()
    adapter = _adapters.get(platform)
    if not adapter:
        raise ValueError(f"Unknown platform: {platform}")
    return adapter


def get_all_adapters() -> dict[str, PlatformAdapter]:
    _init_adapters()
    return _adapters
