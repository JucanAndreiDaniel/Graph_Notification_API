import django
import os
import traceback
from newsapi import NewsApiClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "login_api.settings")

django.setup()


def correcttime(timestamp: str):
    if timestamp == "":
        correct = "2000-01-01"
        return correct
    return timestamp


try:
    import requests
    from oldAPI.models import News

    token = os.environ.get('TOKEN_NEWS')

    api = NewsApiClient(api_key=token)

    for i in range(1,80):
        values = api.get_everything(q="crypto",page_size=99,page=i)

        for article in values["articles"]:
            news = News(
                source_name=article["source"]["name"],
                author=article["author"],
                title=article["title"],
                description=article["description"],
                url=article["url"],
                image_url=article["urlToImage"],
                published_at=article["publishedAt"],
                content=article["content"],
            )
            news.save()

except:
    traceback.print_exc()
