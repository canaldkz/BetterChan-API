from datetime import date

from dataclasses import dataclass, field, fields
from typing import List, Optional, Union


@dataclass
class Manga:
    Id: str
    url: str
    title: str
    series: str
    date: Union[date, str, float]
    pages: int
    preview_url: Optional[str] = None
    authors: Optional[list] = field(default_factory=list)
    translators: Optional[list] = field(default_factory=list)
    tags: Optional[List[str]] = field(default_factory=list)
    page_urls: Optional[List[str]] = field(default_factory=list)

@dataclass
class Error:
    url: str
    manga_url: str
    message: str

@dataclass
class Drop:
    Id: str

@dataclass
class MangaSuggest:
    Id: str
    title: str
    series: str
    preview_url: str
    authors: field(default_factory=list)

@dataclass
class MangaResult:
    Id: str
    url: str
    title: str
    series: str
    date: Union[date, str, float]
    pages: int
    preview_url: Optional[str] = None
    authors: Optional[list] = field(default_factory=list)
    translators: Optional[list] = field(default_factory=list)
    tags: Optional[List[str]] = field(default_factory=list)
    private: bool = field(default=True)


@dataclass
class Filter:
    tags_filter:Optional[List[str]] = None
    author_filter:Optional[List[str]] = None
    translator_filter:Optional[List[str]] = None
    series_filter:Optional[str] = None
    date_filter:Optional[List[date]] = None
    page_filter:Optional[List[int]] = None