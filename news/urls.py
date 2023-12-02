from django.urls import path, re_path, include
from news.views import ListPostView

news_urls = [
    path("posts", ListPostView.as_view(), name="list posts"),
]

urlpatterns = [
    re_path(r'^v1/', include(news_urls)),
]