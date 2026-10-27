import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Author, Book, BookAuthor

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        help_text="Select one or more authors for this book",
    )

    class Meta:
        model = Book
        fields = ['title', 'authors', 'summary', 'isbn', 'genre', 'language']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['authors'].initial = self.instance.authors.all()

    def save(self, commit=True):
        book = super().save(commit=commit)
        if commit:
            self.save_authors(book)
        return book

    def save_authors(self, book):
        BookAuthor.objects.filter(book=book).delete()
        BookAuthor.objects.bulk_create(
            [
                BookAuthor(book=book, author=author, author_order=order)
                for order, author in enumerate(self.cleaned_data['authors'], start=1)
            ]
        )