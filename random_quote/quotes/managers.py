from django.db import models
from django.db.models import Count, Q

class AuthorManager(models.Manager):
    def with_published_quotes(self):
        return self.annotate(
                published_quotes_count = Count('quotes',
                                        filter=Q(quotes__status='Published'))).filter(published_quotes_count__gt=0)


class CategoryManager(models.Manager):
    def with_published_quotes(self):
        return self.annotate(
                published_quotes_count = Count('category', 
                                               filter=Q(category__status='Published'))).filter(published_quotes_count__gt=0)
    