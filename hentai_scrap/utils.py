from datetime import date
from database import MDB
from scrapy.utils.project import get_project_settings


MONTH_DICT = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


settings = get_project_settings()
mdb = MDB(settings.get("RAVEN_URI"), settings.get("RAVEN_DB"))

def date_convert(date_str: str):
    date_list = date_str.split(" ")
    return date(int(date_list[2]), MONTH_DICT[date_list[1]], int(date_list[0])).isoformat()

def get_preview_url(url:str) -> str:
    args = url.split('/')[-3:]
    args[-1] = args[-1].replace('webp', 'jpg')
    preview_url = settings.get("IMGSCHAN") + settings.get("RETINA_PATH") + "/".join(args)
    return preview_url

if __name__ == "__main__":
    print(date_convert("15 ноября 2022"))
    print(mdb.manga_exists('35789-ol-kurosto-kaga-san'))
