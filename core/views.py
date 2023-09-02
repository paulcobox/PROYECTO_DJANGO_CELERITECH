from django.shortcuts import render
from django.views.generic.base import TemplateView



class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Sistema de Paul'})


    # Forma 1 un poco larga porque para sobreecribir el diccionario de contexto
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Estudio de Danza "Muevete al Estilo Cubano"'
    #     return context

class SamplePageView(TemplateView):
    template_name = "core/sample.html"

# def home(request):
#     return render(request, "core/home.html")

# def sample(request):
#     return render(request, "core/sample.html")

