from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, Textarea

from .models import Author, Quote


class AuthorAddForm(ModelForm):
    fullname = CharField(
        max_length=50,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    born_date = CharField(
        max_length=50,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    born_location = CharField(
        max_length=150,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    description = CharField(
        required=True, widget=Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = Author
        fields = (
            "fullname",
            "born_date",
            "born_location",
            "description",
        )


class AuthorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class QuoteAddForm(ModelForm):
    quote = CharField(
        required=True,
        widget=Textarea(attrs={"class": "form-control"}),
    )
    author = AuthorChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Quote
        fields = (
            "quote",
            "author",
        )
