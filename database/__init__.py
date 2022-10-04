from copy import copy
import ravendb as rdb
from typing import Union, Optional, List
from database.models import *
from database.utils import clamp

RAVEN_URI = "http://127.0.0.1:9999"
RAVEN_DB = "MangaDB"

MIN_PAGE_SIZE = 10
MAX_PAGE_SIZE = 25
DEFAULT_PAGE_SIZE = 10

class MDB(rdb.DocumentStore):
    def __init__(self, urls: Optional[Union[str, List[str]]] = None, database: Optional[str] = None):
        super().__init__(urls, database)
        self.initialize()

    def save(self, obj):
        with self.open_session() as session:
            session.store(obj)
            session.save_changes()
    
    def build_query(self, f:Filter=None) -> rdb.DocumentQuery:
        with self.open_session() as session:
            q = session.advanced.document_query(collection_name="Mangas").select_fields(MangaResult, *[f.name for f in fields(MangaResult)])
            if f:
                if f.tags_filter: q = q.contains_all("tags", f.tags_filter)
                if f.author_filter: q = q.contains_all("authors", [f.author_filter])
                if f.translator_filter: q = q.contains_all("translators", [f.translator_filter])
                if f.date_filter: q = q.where_between("date", f.date_filter[0].isoformat(), f.date_filter[1].isoformat())
                if f.page_filter: q = q.where_between("pages", f.page_filter[0], f.page_filter[1])
                if f.series_filter: q = q.where_equals("series", f.series_filter)
        return q

    def discovery(self):
        query = """
        from 'Mangas'
        group by {0}
        order by {0} as alphanumeric 
        """
        with self.open_session() as session:
            all_tags = list(map(lambda x: x['tags[]'], session.advanced.raw_query(query.format("tags[]")).get_query_result().results))
            all_series = list(map(lambda x: x['series'], session.advanced.raw_query(query.format("series")).get_query_result().results))
            all_authors = list(map(lambda x: x['authors[]'], session.advanced.raw_query(query.format("authors[]")).get_query_result().results))
        return dict(tags=all_tags, series=all_series, authors=all_authors)

    def load_by_id(self, manga_id):
        with self.open_session() as session:
            response = session.load(manga_id, Manga)
            return response

    def search_by_query(self, query:str) -> List[Manga]:
        with self.open_session() as session:
            response = list(
                session.advanced.document_query(collection_name="Mangas")
                .select_fields(MangaSuggest, "Id", "title", "series", "preview_url", "authors")
                .search("title", query, rdb.SearchOperator.AND)
                .take(10))
        return response

    def paginate(self, query:rdb.DocumentQuery, offset:int=0, page_size:int=DEFAULT_PAGE_SIZE):
        page_size = clamp(page_size, MIN_PAGE_SIZE, MAX_PAGE_SIZE)
        count = copy(query).count()
        response = list(
            query
            .order_by_descending("Id", rdb.OrderingType.ALPHA_NUMERIC)
            .skip(offset)
            .take(page_size)
        )
        return response, count


if __name__ == "__main__":
    mdb = MDB(RAVEN_URI, RAVEN_DB)
    # r = mdb.discovery()
    # print(r)
    filtr = Filter(author_filter=['Kouda Tomohiro'])
    res = mdb.build_query(filtr)
    print(mdb.paginate(res, 0))