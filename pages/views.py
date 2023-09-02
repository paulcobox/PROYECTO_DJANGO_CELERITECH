from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Page
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import PageForm

from django.urls import reverse, reverse_lazy

# class StaffRequiredMixin(object):
#     """
#     Este mixin requerirá que el usuario sea miembro del staff
#     """
#     @method_decorator(staff_member_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class PageListView(ListView):# ListView para usar una Lista de instancias de la clase Page
    model = Page


class PageDetailView(DetailView):# DetailView para usar instancia  de la clase Page, en la vista puedo usar object o el nombre del modelo page
    model = Page

@method_decorator(staff_member_required, name='dispatch')
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    # fields = ['title', 'content', 'order']
    success_url = reverse_lazy('pages:pages')

@method_decorator(staff_member_required, name='dispatch')
class PageDeleteView(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')

@method_decorator(staff_member_required, name='dispatch')
class PageUpdateView(UpdateView):
    model = Page
    # fields = ['title', 'content', 'order']
    form_class = PageForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

# Funciones que las cambiaeremos por listview y detail view
# # Create your views here.
# def pages(request):
#     pages = get_list_or_404(Page)
#     return render(request, 'pages/pages.html', {'pages':pages})

# def page(request, page_id, page_slug):
#     page = get_object_or_404(Page, id=page_id)
#     return render(request, 'pages/page.html', {'page':page})