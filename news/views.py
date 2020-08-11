from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
import json
import random


class NewsView(View):
    def get(self, request, link="0", *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r+") as news:
            news_json = json.load(news)
        show_article = {
            "created": "0000-00-00 00:00:00",
            "text": "Article not found",
            "title": "404 not found"
        }
        for article in news_json:
            if article["link"] == int(link):
                show_article = article
        return render(
            request, 'news/news_template.html', context={
                'title': show_article["title"],
                'create_date': show_article["created"],
                'text': show_article["text"]
            }
        )


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


class NewsPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as news:
            news_json = json.load(news)
        date_grouped = {}
        if 'q' in request.GET:
            for article in news_json:
                if article["title"].rfind(request.GET['q']) != -1:
                    day = datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    article["created"] = datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S").timestamp()
                    if day in date_grouped:
                        date_grouped[day].append(article)
                    else:
                        date_grouped[day] = [article]
            for key in date_grouped:
                date_grouped[key].sort(key=lambda article: article["created"], reverse=True)
            date_grouped_new = {}
            for key in sorted(date_grouped.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d").timestamp(),
                              reverse=True):
                date_grouped_new[key] = date_grouped[key]
            date_grouped = date_grouped_new
            return render(request, "news/news_list_template.html", context={
                "search": {
                    "show": True,
                    "request": request.GET.get("q"),
                },
                "date_grouped": date_grouped
            })
        else:
            for article in news_json:
                day = datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                article["created"] = datetime.strptime(article["created"], "%Y-%m-%d %H:%M:%S").timestamp()
                if day in date_grouped:
                    date_grouped[day].append(article)
                else:
                    date_grouped[day] = [article]
            for key in date_grouped:
                date_grouped[key].sort(key=lambda article: article["created"], reverse=True)
            date_grouped_new = {}
            for key in sorted(date_grouped.keys(), key=lambda date: datetime.strptime(date, "%Y-%m-%d").timestamp(),
                              reverse=True):
                date_grouped_new[key] = date_grouped[key]
            date_grouped = date_grouped_new
            return render(request, "news/news_list_template.html", context={
                "date_grouped": date_grouped,
                "search": {
                    "show": False
                }
            })


class CreatePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_template.html")

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as news:
            news_json = json.loads(news.read())
        new_article = {
            "created": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "text": request.POST.get("text"),
            "title": request.POST.get("title")
        }
        # Generating unique link
        link = random.randint(1000000, 9999999)
        for article in news_json:
            while link == article["link"]:
                link = random.randint(1000000, 9999999)
        new_article["link"] = link
        news_json.append(new_article)
        with open(settings.NEWS_JSON_PATH, "w+") as news:
            json.dump(news_json, news)
        return redirect("/news/")
