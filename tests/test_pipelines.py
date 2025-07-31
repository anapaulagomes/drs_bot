import pytest
from crawler.pipelines import DuplicatesPipeline
from scrapy.exceptions import DropItem
import pandas as pd


class TestDuplicatesPipeline:
    @pytest.fixture
    def pipeline(self):
        return DuplicatesPipeline()

    @pytest.fixture
    def sample_item(self):
        return {
            'title': 'Test Course',
            'course_url': 'https://www.drs.fu-berlin.de/en/node/123',
            'start': '01.01.2025 - 09:00',
            'end': '01.01.2025 - 17:00',
            'availability': 'available',
            'updated_at': None
        }

    def test_process_item_new_item(self, pipeline, sample_item):
        assert hasattr(pipeline, 'courses')
        assert isinstance(pipeline.courses, pd.DataFrame)

        result = pipeline.process_item(sample_item, None)

        assert result == sample_item

        contains_title = pipeline.courses.title == sample_item['title']
        contains_url = pipeline.courses.course_url == sample_item['course_url']
        courses_with_this_title_and_url = pipeline.courses[contains_title & contains_url]
        assert len(courses_with_this_title_and_url) == 1

    def test_process_item_similar_but_different_urls(self, pipeline, sample_item):
        item1 = sample_item.copy()
        item2 = sample_item.copy()
        item2['course_url'] = 'https://www.drs.fu-berlin.de/en/node/456'

        assert item1['course_url'] != item2['course_url']

        result1 = pipeline.process_item(item1, None)
        result2 = pipeline.process_item(item2, None)

        # both should be processed since they are similar but not duplicates
        assert result1 == item1
        assert result2 == item2

    def test_process_item_different_titles_same_url(self, pipeline, sample_item):
        item1 = sample_item.copy()
        item2 = sample_item.copy()
        item2['title'] = 'Different Course'

        assert item1['title'] != item2['title']

        result1 = pipeline.process_item(item1, None)
        result2 = pipeline.process_item(item2, None)
        
        # both should be processed since they are similar but not duplicates
        assert result1 == item1
        assert result2 == item2

    @pytest.mark.parametrize("item", [
        {'title': 'A title', 'course_url': None},
        {'title': 'Another title', 'course_url': ''},
        {'title': '', 'course_url': 'https://www.drs.fu-berlin.de/en/node/123'},
        {'title': None, 'course_url': 'https://www.drs.fu-berlin.de/en/node/123'},
        {'title': '', 'course_url': None},
        {'title': None, 'course_url': None},
        {'title': '', 'course_url': ''},
    ])
    def test_process_item_with_invalid_values(self, pipeline, item):
        with pytest.raises(DropItem):
            pipeline.process_item(item, None)

    def test_pipeline_reset(self, pipeline, sample_item):
        result1 = pipeline.process_item(sample_item, None)
        assert result1 == sample_item

        # simulating new run
        new_pipeline = DuplicatesPipeline()

        # process same item in new run
        result2 = new_pipeline.process_item(sample_item, None)
        assert result2 == sample_item
