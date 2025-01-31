from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView, CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from quotes.models import Quotes, Authors, Category
from quotes.forms import CreateQuoteNewAuthorForm, CategorySearchForm
from quotes.services.save_quote_service import SaveQuoteService
from random_quote.settings import DEFAULT_IMAGE


class RandomQuoteView(DetailView):
    template_name = 'quotes/home.html'
    context_object_name = 'quote'

    def get_object(self, queryset = None):
        return Quotes.objects.select_related('author').prefetch_related('category').filter(status='Published').order_by('?').first()


class AuthorsView(ListView):
    template_name = 'quotes/authors.html'
    context_object_name = 'authors'
    queryset = Authors.objects.with_published_quotes()
    extra_context = {'default_photo': DEFAULT_IMAGE}

class CategoriesView(ListView):
    template_name = 'quotes/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.with_published_quotes()
    extra_context = {'category_search_form':CategorySearchForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_field = self.request.GET.get('search_field', '')
        context['search_field'] = search_field
        if search_field:
            context['categories'] = Category.objects.with_published_quotes().filter(name__icontains=search_field)
        return context


class SearchView(TemplateView):
    template_name = 'quotes/search.html'
    extra_context = {'default_photo':DEFAULT_IMAGE}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_field = self.request.GET.get('search_field', '')
        context['search_field'] = search_field
        if search_field:
            context['quotes_result']  = Quotes.objects.select_related('author').prefetch_related('category').filter(quote__icontains=search_field, status='Published')
            context['authors_result'] =Authors.objects.with_published_quotes().filter(name__icontains=search_field)
            context['categories_result'] =Category.objects.with_published_quotes().filter(name__icontains=search_field)
        return context        


class AuthorQuotes(ListView):
    template_name = 'quotes/author_quotes.html'
    extra_context= {'default_photo': DEFAULT_IMAGE}
    context_object_name = 'quotes'

    def get_queryset(self):
        author_slug = self.kwargs['author']
        author = get_object_or_404(Authors, slug = author_slug)
        return Quotes.objects.prefetch_related('category').filter(author=author,status='Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(Authors, slug=self.kwargs['author'])

        return context

class CategoryQuotes(ListView):
    template_name = 'quotes/category_quotes.html'
    context_object_name = 'quotes'

    def get_queryset(self):
        category_slug = self.kwargs['category']
        category = get_object_or_404(Category, slug=category_slug)

        return Quotes.objects.select_related('author').prefetch_related('category').filter(category=category,status='Published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category']).name

        return context


class CreateQuoteView(LoginRequiredMixin, CreateView):
    template_name = 'quotes/create_quote.html'
    form_class = CreateQuoteNewAuthorForm

    def form_valid(self, form):
        quote = form.save()
        quote.user = self.request.user
        quote.save()
        return render(self.request,'quotes/success_form.html',{
            'title':'Форма успешно отправлена', 
            'message':'Ваша цитата будет рассмотрена модератором',
            } )
    

class SaveQuoteView(LoginRequiredMixin, UpdateView):
    template_name = 'quotes/home.html'
    model = get_user_model()
    fields = []
    success_url = reverse_lazy('home')

    def get_object(self, queryset = None):
        return get_user_model().objects.get(id=self.request.user.id)
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        success_save_quote = SaveQuoteService(self.kwargs['id'], user).save_quote()
        if success_save_quote:
            messages.success(self.request,success_save_quote)
        
        else:
            messages.error(self.request, 'Цитата не найдена!')
       
        return redirect('home')
