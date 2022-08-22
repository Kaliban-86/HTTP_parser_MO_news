class News:
    def __init__(self, title, date, url, cr_date):
        self.news_title = title
        self.news_url = url
        self.news_date = date
        self.news_get_date = cr_date

    def __str__(self):
        return f'{self.news_title}\n{self.news_date}\n{self.news_url}\n{self.news_get_date}'