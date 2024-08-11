import os
import django
from pymongo import MongoClient
import configparser
import pathlib


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()


from quotes_app.models import Author, Tag, Quote


file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")


client = MongoClient(
    f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
)

db = client[db_name]

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        tag_text, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(tag_text)

    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))

    if not exist_quote:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(quote=quote["quote"], author=a)
        for tag in tags:
            q.tags.add(tag)
