from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from quotes.models import Quote, Author, Category
from quotes.validators.author_validator import author_validate
from quotes.validators.category_validator import category_validate


class CreateQuoteNewAuthorForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        label="Автор",
        widget=ModelSelect2Widget(model=Author, search_fields=["name__icontains"]),
    )
    new_author = forms.CharField(
        max_length=150,
        required=False,
        label="Новый автор",
        validators=[author_validate],
        widget=forms.TextInput(
            attrs={"placeholder": "Введите автора, если его нет в списке"}
        ),
        strip=True,
    )
    biography = forms.CharField(
        required=False, label="Биография", widget=forms.Textarea()
    )
    photo = forms.ImageField(required=False, label="Фото автора")
    quote = forms.CharField(required=True, label="Цитата", widget=forms.Textarea())
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label="Выбрать категории",
        required=False,
        widget=ModelSelect2MultipleWidget(
            model=Category, search_fields=["name__icontains"]
        ),
    )

    new_categories = forms.CharField(
        max_length=150,
        required=False,
        label="Добавить свои категории",
        validators=[category_validate],
        widget=forms.Textarea(
            attrs={"placeholder": "Разделяйте запятой для нескольких категорий"}
        ),
        strip=True,
    )

    class Meta:
        model = Quote
        fields = ["quote"]

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data["categories"] and not self.cleaned_data.get(
            "new_categories", ""
        ):
            raise ValidationError(
                "Вы должны выбрать хотя бы одну категорию или написать свою."
            )

        if not self.cleaned_data["author"] and not self.cleaned_data.get(
            "new_author", ""
        ):
            raise ValidationError(
                "Вы должны выбрать автора из списка или написать своего."
            )

        return self.cleaned_data

    def save(self):

        author = (
            self.cleaned_data["author"]
            if self.cleaned_data["author"]
            else self.cleaned_data["new_author"].title()
        )
        biography = self.cleaned_data["biography"]
        photo = self.cleaned_data.get("photo")
        categories = list(self.cleaned_data["categories"])

        if Author.objects.filter(name=author).exists():
            author = Author.objects.get(name=author)
        else:
            author, _ = Author.objects.get_or_create(
                name=author, biography=biography, photo=photo
            )

        for cat in self.cleaned_data["new_categories"].split(","):
            if cat:
                cat = cat.strip().capitalize()
                category, _ = Category.objects.get_or_create(name=cat)
                categories.append(category)

        quote = Quote.objects.create(quote=self.cleaned_data["quote"], author=author)
        quote.category.set(categories)
        quote.save()

        return quote


class SearchForm(forms.Form):
    search_field = forms.CharField(
        label="Поиск по сайту",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Поиск по сайту"}),
    )


class CategorySearchForm(forms.Form):
    search_field = forms.CharField(
        label="Поиск по категориям",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Поиск по категориям"}),
    )
