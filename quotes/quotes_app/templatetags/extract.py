from bson.objectid import ObjectId
from django.shortcuts import get_object_or_404
from django import template

from ..models import Author, Tag

register = template.Library()


def get_author(author_quote):
    author = get_object_or_404(Author, id=author_quote.id)

    return author.fullname


register.filter("author", get_author)


def get_tags(tag_quote):
    return tag_quote.name


register.filter("tag_name", get_tags)
