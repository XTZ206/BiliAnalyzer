from os import PathLike
from typing import Union, Any, Optional, Collection

FilePath = Union[str, PathLike]

Member = dict[str, Any]
Reply = dict[str, Any]
Page = dict[str, Any]

Cookies = dict[str, str]
