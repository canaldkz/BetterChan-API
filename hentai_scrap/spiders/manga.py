import scrapy
from database.models import Manga, Error, Drop
from unicodedata import normalize as norm
from hentai_scrap.utils import date_convert, get_preview_url, mdb
from pyjsparser import parse


class MangasSpider(scrapy.Spider):
    name = "mangas"
    offset = 0
    base_url = "https://y.hentaichan.live"
    start_url = f"{base_url}/manga/new?offset={offset}"


    def start_requests(self):
        return [scrapy.FormRequest(self.start_url,
                                   formdata={
                                    'login': 'submit',
                                    'login_name': 'BetterBot',
                                    'login_password':"betterbotpass",
                                    'image': 'Вход'},
                                    callback=self.parse)]

    def parse(self, response):
        drop_count = 0
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
                if mdb.load_by_id(Id):
                    drop_count+=1
                    yield Drop(Id)
                else:
                    yield response.follow(
                        response.urljoin(url),
                        self.parse_manga_page,
                        cb_kwargs=dict(
                            item=Manga(
                                Id=Id,
                                url=url,
                                title=title,
                                series=series,
                                date=date_convert(date),
                                authors=authors,
                                translators=translators,
                                pages=pages,
                                tags=tag_list,
                                )))

        except Exception as e:
            yield Error(url=response.url, manga_url=url, message=f'{e}')
        next_page = response.xpath('//div[@id="pagination"]/a[(text() = ">")]/@href').extract_first()
        if next_page and drop_count < 20:
            yield scrapy.Request(response.urljoin(f"new{next_page}"))
        
    def parse_manga_page(self, response, item):
        # image = response.xpath('//div[@id="content"]//div[@id="manga_images"]/a/img/@src').extract_first()
        url = response.xpath('//div[@id="content"]//div[@id="manga_images"]/a/@href').extract_first()
        if "exhentai" not in url:
            item.private = False
            url = self.base_url+url
        else:
            item.private = True
        yield response.follow(url, self.parse_manga_images, cb_kwargs=dict(item=item))


    def parse_manga_images(self, response, item):
        script = norm("NFKD", response.xpath('//div[@id="content"]/script[not(@src)]/text()').extract_first())
        res = parse(script)
        item.page_urls = [a["value"] for a in res["body"][0]["declarations"][0]["init"]["properties"][2]["value"]["elements"]]
        item.preview_url = get_preview_url(item.page_urls[0]) 

        yield item