from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AuthorAddForm, QuoteAddForm
from .models import Quote, Tag, Author


def root(request, page=1):
    quotes = Quote.objects.all().order_by("-created_at")
    quotes_list = []

    for quote in quotes:
        tags = quote.tags.all()
        quote_dict = {
            "quote": quote.quote,
            "tags": tags,
            "author": quote.author,
            "created_at": quote.created_at,
        }
        quotes_list.append(quote_dict)

    per_page = 10
    paginator = Paginator(list(quotes_list), per_page)
    quotes_on_page = paginator.page(page)

    return render(
        request,
        "quotes_app/index.html",
        context={
            "quotes": quotes_on_page,
        },
    )


def author_info(request, author_id):
    author = Author.objects.get(id=author_id)
    print(author.fullname)

    return render(request, "quotes_app/author_info.html", {"author": author})


@login_required
def author_add(request):
    form = AuthorAddForm(instance=Author())

    if request.method == "POST":
        form = AuthorAddForm(request.POST, instance=Author())
        if form.is_valid():
            author_name = form.cleaned_data["fullname"]

            author_exist = Author.objects.filter(fullname=author_name)

            if not author_exist:
                form.save()
                return redirect(to="/")

            messages.warning(
                request,
                message=f"Author {author_name} is already in database.",
            )
            return redirect(to="quotes_app:author_add")

    return render(request, "quotes_app/author_add.html", context={"form": form})


@login_required
def quote_add(request):
    form = QuoteAddForm(instance=Quote())

    if request.method == "POST":
        form = QuoteAddForm(request.POST, instance=Quote())

        if form.is_valid():
            form.save()

            messages.success(
                request,
                message=f"Quote has been added to database.",
            )
            return redirect(to="/")

    return render(request, "quotes_app/quote_add.html", context={"form": form})


def quote_by_tag(request, tag_id):
    print(tag_id)

    tag = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag)

    return render(request, "quotes_app/quotes_tag.html", {"tag": tag, "quotes": quotes})


def top_tags(request):
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    return render(request, "quotes_app/top-tags.html", {"top_tags": top_tags})
