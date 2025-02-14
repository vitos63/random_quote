from quotes.models import Quote


class SaveQuoteService:
    def __init__(self, quote_id, user):
        self.quote_id = quote_id
        self.user = user

    def save_quote(self):

        try:
            quote = Quote.objects.get(id=self.quote_id)
            if quote in self.user.profile.saved_quotes.all():
                return "Цитата уже сохранена"
            else:
                self.user.profile.saved_quotes.add(quote)
                self.user.save()
                return "Цитата успешно сохранена"

        except Quote.DoesNotExist:
            return
