import scrapy

from crawler.spiders.adapters import extract_status_from_capacity_bookings


class DahlemResearchSchoolSpider(scrapy.Spider):
    name = "drs"
    allowed_domains = ["www.drs.fu-berlin.de"]
    start_urls = ["https://www.drs.fu-berlin.de/en/course_list"]
    base_url = "https://www.drs.fu-berlin.de"

    def parse(self, response):
        for row in response.css("table tbody tr"):
            title_element = row.css("td:first-child a")
            title = title_element.css("::text").extract_first()
            if not title:
                continue

            course_url = title_element.css("::attr(href)").extract_first()
            if course_url:
                course_url = course_url.strip()
                if not course_url.startswith('http'):
                    course_url = f"{self.base_url}{course_url}"

            start = row.css("td:nth-child(3)::text").extract_first()
            end = row.css("td:nth-child(4)::text").extract_first()

            capacity_bookings = row.css("td:nth-child(8)::text").extract_first()
            if capacity_bookings:
                capacity_bookings = capacity_bookings.strip()
                availability = extract_status_from_capacity_bookings(capacity_bookings)
            else:
                availability = "unavailable"

            yield dict(
                title=title.strip() if title else "",
                course_url=course_url if course_url else "",
                start=start.strip() if start else "",
                end=end.strip() if end else "",
                availability=availability,
                updated_at=None
            )

        next_page = response.css("ul.pagination li.next a::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
