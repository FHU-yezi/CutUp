from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class SplitRequest:
    library: str
    variant: str
    text: str


@dataclass
class SplitResponse:
    text: Tuple[str]


@dataclass
class GetWordFreqRequest:
    library: str
    variant: str
    text: str


@dataclass
class GetWordFreqResponse:
    text: Dict[str, int]
