import re
from datetime import datetime

import scrapy
from scrapy import Request


class DahlemResearchSchoolSpider(scrapy.Spider):
    name = "drs"
    allowed_domains = ["www.drs.fu-berlin.de"]
    start_urls = ["https://www.drs.fu-berlin.de/course_list"]
    base_url = "https://www.drs.fu-berlin.de"

    # TODO read courses csv and add there only the new ones

    def parse(self, response):
        english_code = "2"
        semester_option_labels_values = extract_option_and_values(response, "select#edit-semester")
        semesters = filter_semester(semester_option_labels_values)
        url = (
            "https://www.drs.fu-berlin.de/en/course_list?"
            "semester={}&"
            "title=&"
            f"field_language_value={english_code}"
        )

        return [
            Request(
                url.format(semester_value),
                callback=self.parse_page,
            )
            for semester_value in semesters
        ]

    def parse_page(self, response):
        next_page = response.css("div.view-course-list ul.pagination li.next a ::attr(href)").extract_first()

        for row in response.css("div.table-responsive tr"):
            title = row.css("td.views-field-title a ::text").extract_first()
            if not title:
                continue
            course_url = row.css("td.views-field-title a ::attr(href)").extract_first().strip()
            start = row.css("td.views-field-course-start-time::text").extract_first()
            end = row.css("td.views-field-course-end-time::text").extract_first()
            capacity_bookings = row.css("td.views-field-oc-course-size::text").extract_first().strip()
            availability = "unavailable"
            if capacity_bookings:
                if capacity_bookings == "0":
                    availability = "unknown"
                try:
                    # e.g. 15 / 5
                    capacity, bookings = capacity_bookings.split("/")
                    if int(bookings) < int(capacity):
                        availability = "available"
                except ValueError:
                    pass

            yield dict(
                title=title.strip(),
                course_url=f"{self.base_url}{course_url}",
                start=start.strip(),
                end=end.strip(),
                availability=availability,
                sent_at=None
            )

        yield response.follow(f"{self.base_url}{next_page}", callback=self.parse)


def filter_semester(semester_option_labels_values):
    filtered_semesters = []
    for label, value in semester_option_labels_values.items():
        found = re.search(r"(\d{4})(\/)?(\d{2})?", label)
        if found:
            past_year = found.group(1)
            current_year = found.group(3)
            last_year = datetime.now().year - 1
            if current_year and int(current_year) >= last_year:
                filtered_semesters.append(value)
            elif past_year and int(past_year) >= last_year:
                filtered_semesters.append(value)
    return filtered_semesters


def extract_option_and_values(response, select_id):
    semester_options = response.css(select_id)
    semester_option_labels = semester_options.css(" ::text").extract()
    semester_option_values = semester_options.css(" ::attr(value)").extract()
    return {key: value for key, value in zip(semester_option_labels, semester_option_values)}
