from api import app, mdb
from database.models import Filter
from fastapi import Response, Request


@app.get('/')
def index(response:Response):
    discovery_data = mdb.discovery()
    response.headers["Access-Control-Allow-Origin"] = "*"
    return discovery_data

@app.api_route('/mangas', methods=["GET", "POST", "OPTIONS"])
async def mangas(response:Response, request:Request, offset:int=0, page_size:int=20):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "X-PINGOTHER, Content-Type"
    match request.method:
        case "GET":
            query = mdb.build_query()
            mangas, manga_count = mdb.paginate(query, offset, page_size)
        case "POST":
            body:dict = await request.json()
            filter_data = Filter(
                tags_filter=body.get("tags", None),
                author_filter=body.get("author", None),
                series_filter=body.get("series", None)
                )
            query = mdb.build_query(filter_data)
            mangas, manga_count = mdb.paginate(query, offset, page_size)
        case "OPTIONS":
            return "ok"
    
    return {"items": mangas, "offset": offset, "manga_count": manga_count}

@app.get('/manga')
def manga(response:Response, id:str):
    manga = mdb.load_by_id(id)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"item": manga}

@app.get('/search')
def manga(response:Response, query:str):
    mangas = mdb.search_by_query(query)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"items":mangas}
