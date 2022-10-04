import scrapy
from database.models import Manga, Error
from unicodedata import normalize as norm
from hentai_scrap.utils import date_convert


class MangasSpider(scrapy.Spider):
    name = "mangas"
    offset = 0
    start_urls = [f"https://y.hentaichan.live/manga/new?offset={offset}"]

    def parse(self, response):
        try:
            for manga in response.xpath('//div[@id="content"]/div[@class="content_row"]'):
                title = manga.xpath('./div[@class="manga_row1"]//a[@class="title_link"]/text()').extract_first()
                url = manga.xpath('./div[@class="manga_row1"]//a[@class="title_link"]/@href').extract_first() .split("/")[-1]
                Id = url.replace(".html", '', 1)
                series = manga.xpath('./div[@class="manga_row2"]//h3[@class="original work"]/a/text()').extract_first()
                authors = manga.xpath('./div[@class="manga_row3"]//h3/a[1]/text()').extract()
                translators = manga.xpath('./div[@class="manga_row2"]//span/a/text()').extract()
                tag_list = manga.xpath('.//div[@class="genre"]/a/text()').extract()
                date = manga.xpath('./div[@class="manga_row4"]/div[@class="row4_right"]/b/text()').extract_first()
                pages = float(list(
                        filter(lambda i: len(i),
                        map(lambda i: norm("NFKD", i).strip().strip(","),
                        manga.xpath('./div[@class="manga_row4"]/div[@class="row4_left"]/text()').extract())))[0]
                        .split(",")[-1]
                        .split()[0]
                        )

                yield Manga(
                    Id=Id,
                    url=url,
                    title=title,
                    series=series,
                    date=date_convert(date),
                    authors=authors,
                    translators=translators,
                    pages=pages,
                    tags=tag_list,
                )
        except Exception as e:
            yield Error(url=response.url, manga_url=url, message=f'{e}')

        next_page = response.xpath('//div[@id="pagination"]/a[(text() = ">")]/@href').extract_first()
        # offset = int(next_page.split('=')[-1])
        # if next_page and offset <= (20*20)-20:
        if next_page:
            yield scrapy.Request(response.urljoin(f"new{next_page}"))
