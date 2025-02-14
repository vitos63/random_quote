from quotes.models import Quote


class DeleteSavedQuotesService:

    def __init__(self, quote_id, user):
        self.quote_id = quote_id
        self.user = user

    def delete(self):
        try:
            quote = Quote.objects.get(id=self.quote_id)

            if quote in self.user.profile.saved_quotes.all():
                self.user.profile.saved_quotes.remove(quote)
                self.user.save()
                return True

        except Quote.DoesNotExist:
            return
