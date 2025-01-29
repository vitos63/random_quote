"""
URL configuration for random_quote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from .views import AuthorQuotes, CategoryQuotes, CreateQuoteView, RandomQuoteView, SaveQuoteView, AuthorsView, CategoriesView, SearchView

urlpatterns = [
    path('', RandomQuoteView.as_view(), name='home'),
    path('authors/',AuthorsView.as_view(), name='authors'),
    path('categories/',CategoriesView.as_view(), name='categories'),
    path('create-quote/',CreateQuoteView.as_view(), name='create_quote'),
    path('author-quotes/<slug:author>', AuthorQuotes.as_view(), name='author_quotes'),
    path('category-quotes/<slug:category>', CategoryQuotes.as_view(), name='category_quotes'),
    path('save-quote/<int:id>/', SaveQuoteView.as_view(), name='save_quote'),
    path('search/', SearchView.as_view(), name='search'),
]
