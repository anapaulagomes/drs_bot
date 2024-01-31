import scrapy
from scrapy import FormRequest


class DahlemResearchSchoolSpider(scrapy.Spider):
    name = "drs"
    allowed_domains = ["www.drs.fu-berlin.de"]
    start_urls = ["https://www.drs.fu-berlin.de/course_list"]

    def start_requests(self, response):
        semester_option_labels_values = extract_option_and_values("select#edit-semester")
        category_option_labels_values = extract_option_and_values("select#edit-parent-container")
        language_option_labels_values = extract_option_and_values("select#edit-field-language-value")
        title = ""  # TODO get as param

        # https://www.drs.fu-berlin.de/en/course_list?semester=20&title=&field_language_value=All
        # https://www.drs.fu-berlin.de/en/course_list?
        #   semester=20&
        #   title=&
        #   parent_container%5B%5D=52648&
        #   field_language_value=All
        return [FormRequest(
            url="http://www.example.com/post/action",
            formdata={"title": title, "age": "27"},
            callback=self.after_post,
        )]


# TODO filter by semesters in the future
# TODO crawl all pages after the filter

def extract_option_and_values(response, select_id):
    semester_options = response.css(select_id)
    semester_option_labels = semester_options.css(" ::text").extract()
    semester_option_values = semester_options.css(" ::attr(value)").extract()
    return {key: value for key, value in zip(semester_option_labels, semester_option_values)}
