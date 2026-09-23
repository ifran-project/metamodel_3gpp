"""Basic utilities."""

from typing import Annotated, Any

from pydantic import (
    AnyUrl,
    UrlConstraints,
)

type URL = Annotated[AnyUrl, UrlConstraints(preserve_empty_path=True)]
"""
URL type without unwanted trailing slash at the end. See:
    - https://github.com/pydantic/pydantic/issues/7186
    - https://pydantic.dev/articles/pydantic-v2-12-release#preserve-empty-url-paths
"""


def parse_hex_int(value: str | Any) -> int | Any:
    """Convert an integer or hexadecimal string to an integer."""

    if isinstance(value, str):
        return int(value, 16)
    return value


def serialize_hex_int(value: int | None, width: int) -> str | None:
    """Serialize an integer to a zero-padded uppercase hexadecimal string."""

    if value is None:
        return None
    return f"{value:0{width}X}"
