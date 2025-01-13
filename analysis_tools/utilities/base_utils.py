import os
from typing import Union, AnyStr
from pathlib import Path

__all__ = [
    "PathType",
]


PathType = Union[str, AnyStr, os.PathLike, Path]
