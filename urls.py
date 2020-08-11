"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news.views import NewsView
from news.views import MainPageView
from news.views import NewsPageView
from news.views import CreatePageView

urlpatterns = [
    path('news/create/', CreatePageView.as_view()),
    path('news/<str:link>/', NewsView.as_view()),
    path('', MainPageView.as_view()),
    path('news/', NewsPageView.as_view()),
]
