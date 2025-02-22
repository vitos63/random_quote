from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from quotes.models import Quote, Author, Category
from api_quotes.serializers import (
    QuoteSerializer,
    AuthorSerializer,
    CategorySerializer,
    RegisterSerializer,
    CreateQuoteSerializer,
    SuggestedQuotesSerializer,
    SaveQuoteSerializer,
)


class RandomQuoteAPIView(RetrieveAPIView):
    serializer_class = QuoteSerializer

    def get(self, request, *args, **kwargs):
        random_quote = Quote.objects.random_quote()
        serializer_data = self.serializer_class(random_quote).data
        return Response(serializer_data)


class AuthorsAPIView(ListAPIView):
    queryset = Author.objects.with_published_quotes()
    serializer_class = AuthorSerializer


class CategoriesAPIView(ListAPIView):
    queryset = Category.objects.with_published_quotes()
    serializer_class = CategorySerializer


class AuthorQuotesAPIView(ListAPIView):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        author = get_object_or_404(Author, slug=self.kwargs["author"])
        return Quote.objects.prefetch_related("category").filter(
            author=author, status="Published"
        )


class CategoryQuotesAPIView(ListAPIView):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category"])
        return (
            Quote.objects.select_related("author")
            .prefetch_related("category")
            .filter(category=category, status="Published")
        )


class SearchAPIView(APIView):

    def get(self, request, *args, **kwargs):
        search_field = self.request.GET.get("search_field", "")
        serializer_data = {}
        if search_field:
            serializer_data["quotes_result"] = QuoteSerializer(
                Quote.objects.select_related("author")
                .prefetch_related("category")
                .filter(quote__icontains=search_field, status="Published"),
                many=True,
            ).data
            serializer_data["authors_result"] = AuthorSerializer(
                Author.objects.with_published_quotes().filter(
                    name__icontains=search_field
                ),
                many=True,
            ).data
            serializer_data["categories_result"] = CategorySerializer(
                Category.objects.with_published_quotes().filter(
                    name__icontains=search_field
                ),
                many=True,
            ).data

        if not any(serializer_data.values()):
            return Response(
                {"detail": "Результаты не найдены."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer_data)


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Пользователь успешно зарегистрирован",
                    "user": {"username": user.username, "email": user.email},
                }
            )
        return Response(serializer.errors)


class CreateQuoteAPIView(CreateAPIView):
    serializer_class = CreateQuoteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quote = serializer.save()
        data = QuoteSerializer(quote).data

        return Response(data, status=status.HTTP_201_CREATED)


class SaveQuoteAPIView(CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = SaveQuoteSerializer

    def perform_create(self, serializer):
        quote = serializer.save()

        return Response(
            {
                "message": "Цитата успешно добавлена в сохраненные.",
                "quote": {
                    "id": quote.id,
                    "quote": quote.quote,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class SuggestedQuotesAPIView(ListAPIView):
    serializer_class = SuggestedQuotesSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return (
            Quote.objects.select_related("author")
            .prefetch_related("category")
            .filter(user=self.request.user)
        )


class SavedQuotesAPIView(ListAPIView):
    serializer_class = QuoteSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return self.request.user.profile.saved_quotes.all()


class DeleteSavedQuoteAPIView(DestroyAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return self.request.user.profile.saved_quotes.all()

    def perform_destroy(self, instance):
        if instance not in self.request.user.profile.saved_quotes.all():
            raise PermissionDenied("Цитата не найдена")

        instance.delete()
        return Response(
            {"detail": "Цитата успешно удалена."}, status=status.HTTP_204_NO_CONTENT
        )
