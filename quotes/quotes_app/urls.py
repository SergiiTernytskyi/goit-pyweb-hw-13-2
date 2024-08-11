from django.urls import path

from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.root, name="root"),
    path("<int:page>", views.root, name="root_paginate"),
    path("author-info/<str:author_id>/", views.author_info, name="author_info"),
    path("author-add/", views.author_add, name="author_add"),
    path("quote_add/", views.quote_add, name="quote_add"),
    path("quote-by-tag/<str:tag_id>/", views.quote_by_tag, name="quote_by_tag"),
    path("top-tags/", views.top_tags, name="top_tags"),
]
