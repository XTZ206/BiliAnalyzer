from os import PathLike
from typing import Union, Any, TypeAlias, Optional, Collection

FilePath = Union[str, PathLike]

Member: TypeAlias = dict[str, Any]
Reply: TypeAlias = dict[str, Any]
Page: TypeAlias = dict[str, Any]
Analysis: TypeAlias = dict[str, Any]
Videoinfo: TypeAlias = dict[str, Any]

Cookies: TypeAlias = dict[str, str]
