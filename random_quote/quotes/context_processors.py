from .models import Menu
from .forms import SearchForm
def menu_context(request):
    menu = []
    for title in Menu.objects.all():
        menu.append({'title':title.title , 'url_name': title.url_name})
    
    return {'menu':menu, 'search_form':SearchForm}

