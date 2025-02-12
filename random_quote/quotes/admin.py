from django.contrib import admin
from .models import Quote, Author, Category
from .models import Menu


@admin.register(Quote)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ['quote', 'author','author__biography', 'status']
    actions = ['set_published', 'set_rejected']
    list_filter = ['status']

    @admin.action(description='Опубликовать выбранные цитаты')
    def set_published(self,request,queryset):
        queryset.update(status = 'Published')
    
    @admin.action(description='Отклонить выбранные цитаты')
    def set_rejected(self,request,queryset):
        queryset.update(status = 'Rejected')


@admin.register(Author, Category)
class AuthorsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_name']
