class MyCartError(Exception):
    pass


class PlatformUnavailableError(MyCartError):
    def __init__(self, platform: str, detail: str = ""):
        self.platform = platform
        self.detail = detail
        super().__init__(f"{platform} is unavailable: {detail}")


class TokenExpiredError(MyCartError):
    def __init__(self, platform: str):
        self.platform = platform
        super().__init__(f"Auth token for {platform} has expired")


class AdapterNotImplementedError(MyCartError):
    def __init__(self, platform: str, method: str):
        super().__init__(f"{platform}.{method} not yet implemented")
