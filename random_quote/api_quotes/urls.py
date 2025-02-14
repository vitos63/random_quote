from django.urls import path
from api_quotes.views import (
    RandomQuoteAPIView,
    AuthorsAPIView,
    CategoriesAPIView,
    AuthorQuotesAPIView,
    CategoryQuotesAPIView,
    SearchAPIView,
    RegisterAPIView,
    CreateQuoteAPIView,
    SuggestedQuotesAPIView,
    SavedQuotesAPIView,
    SaveQuoteAPIView,
    DeleteSavedQuotesAPIView,
)

app_name = "api_quotes"

urlpatterns = [
    path("random-quote/", RandomQuoteAPIView.as_view(), name="random_quote"),
    path("authors/", AuthorsAPIView.as_view(), name="authors"),
    path("categories/", CategoriesAPIView.as_view(), name="categories"),
    path(
        "author-quotes/<slug:author>/",
        AuthorQuotesAPIView.as_view(),
        name="author_quotes",
    ),
    path(
        "category-quotes/<slug:category>/",
        CategoryQuotesAPIView.as_view(),
        name="category_quotes",
    ),
    path("search/", SearchAPIView.as_view(), name="search"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("create-quote/", CreateQuoteAPIView.as_view(), name="create_quote"),
    path("save-quote/", SaveQuoteAPIView.as_view(), name="save_quote"),
    path(
        "suggested-quotes/", SuggestedQuotesAPIView.as_view(), name="suggested_quotes"
    ),
    path("saved-quotes/", SavedQuotesAPIView.as_view(), name="saved_quotes"),
    path(
        "delete-saved-quote/<int:pk>/",
        DeleteSavedQuotesAPIView.as_view(),
        name="delete_saved_quote",
    ),
]
