from urllib.parse import urlparse


async def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)
