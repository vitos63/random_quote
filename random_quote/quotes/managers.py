from django.db import models
from django.db.models import Count, Q


class QuoteManager(models.Manager):
    def random_quote(self):
        random_id = self.filter(status='Published').order_by('?').values_list('id', flat=True).first()
        return self.select_related('author').prefetch_related('category').get(id=random_id)


class AuthorManager(models.Manager):
    def with_published_quotes(self):
        return self.annotate(
                published_quotes_count = Count('author_quotes',
                                        filter=Q(author_quotes__status='Published'))).filter(published_quotes_count__gt=0)


class CategoryManager(models.Manager):
    def with_published_quotes(self):
        return self.annotate(
                published_quotes_count = Count('category_quotes', 
                                               filter=Q(category_quotes__status='Published'))).filter(published_quotes_count__gt=0)
    