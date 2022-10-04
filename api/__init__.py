import fastapi
from database import MDB

RAVEN_URI = 'http://127.0.0.1:9999'
RAVEN_DB = 'MangaDB'

app = fastapi.FastAPI()
mdb = MDB(RAVEN_URI, RAVEN_DB)

from api import routes
