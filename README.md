# DRS bot

[![Search and Notify](https://github.com/anapaulagomes/drs_bot/actions/workflows/schedule.yml/badge.svg)](https://github.com/anapaulagomes/drs_bot/actions/workflows/schedule.yml)

> How did you know about this course? Well, a little bot told me...

A bot to let me know about courses available on [Dahlem Research School courses](https://www.drs.fu-berlin.de/en/course_list).

## Development

Have [Poetry](https://python-poetry.org/) installed and then run:

```
poetry install
poetry shell
```

Running it locally:

```
scrapy crawl drs
```

The pipeline will take care of updating the file `courses.csv`.
