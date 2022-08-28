class News:
    def __init__(self, title, categ_inf, url, cr_date):
        self.news_title = title
        self.news_url = url
        self.news_categ = categ_inf
        self.news_get_date = cr_date

    def __str__(self):
        return f'{self.news_title}\n{self.news_categ.lstrip().rstrip()}\n{self.news_url.lstrip()}\n{self.news_get_date}'