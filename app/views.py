from django.shortcuts import render, redirect
from .models import Alumnoclase, Curso, Calificacion
from authentication.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .forms import CalificacionForm
from django.http import HttpResponseRedirect
from .helper import query_list_calificacion, query_list_asistencia,query_list_curso

# @method_decorator(staff_member_required, name='dispatch')
class CalificacionListView(ListView):
    
     template_name = 'app/alumnocurso_calificacion.html'
     context_object_name = 'alumnocurso_list'
     paginate_by = 20

     def get_context_data(self, *args, **kwargs):
          context = super(CalificacionListView, self).get_context_data(**kwargs)
          cursos = query_list_curso(self.request.user)
          curso_select = self.request.GET.get("curso_select", None)
          context['cursos'] = query_list_curso(self.request.user)
          if curso_select:
               context['curso_select'] = int(curso_select)
          return context

     def get_queryset(self):
          curso_select = self.request.GET.get("curso_select", None)
          # print('CURSO SELECT ======', curso_select)
          return query_list_calificacion(curso_select,self.request.user)

def asistencia(request,alumnoclase_id=-1, asistencia=-1,curso_select=None, asistencia_select=None, date=None):

     alumnoclase = get_object_or_404(Alumnoclase, id=alumnoclase_id)
     alumnoclase.asistio=asistencia
     alumnoclase.save()
     alumnoclase_list = query_list_asistencia(curso_select, asistencia_select, date, request.user)
     cursos = query_list_curso(request.user)
     return render(request, "app/asistencia_list.html", {'curso_select':curso_select,'date':date,'asistencia_select':asistencia_select,'cursos':cursos, 'asistencia_list':alumnoclase_list})

# @method_decorator(staff_member_required, name='dispatch')
class AlumnoclaseListView(ListView):
    
     template_name = 'app/asistencia_list.html'
     context_object_name = 'asistencia_list'
     paginate_by = 20

     def get_context_data(self, **kwargs):
          cursos = query_list_curso(self.request.user)
          context = super(AlumnoclaseListView, self).get_context_data(**kwargs)
          context['cursos'] = cursos

          curso_select = self.request.GET.get("curso_select", None)
          if curso_select:
               context['curso_select'] = int(curso_select)

          asistencia_select = self.request.GET.get("asistencia_select", None)
          if asistencia_select:
               context['asistencia_select'] = int(asistencia_select)

          date = self.request.GET.get("date", None)
          if date:
               context['date'] = date

          return context
     def get_queryset(self):
          queryset_alumno_clase = Alumnoclase.objects.filter(status=1)
          curso_select = self.request.GET.get("curso_select", None)
          asistencia_select = self.request.GET.get("asistencia_select", None)
          date = self.request.GET.get("date", None)
          return query_list_asistencia(curso_select, asistencia_select, date, self.request.user)

@method_decorator(staff_member_required, name='dispatch')
class CalificacionCreateView(CreateView):
     model = Calificacion
     form_class = CalificacionForm

     def get_context_data(self, *args, **kwargs):
          context = super(CalificacionCreateView, self).get_context_data(**kwargs)
          id = self.kwargs['id']
          curso_id = self.kwargs['curso_id']
          curso = Curso.objects.get(pk=curso_id)
          user = User.objects.get(pk=id)
          alumno_clase_result = Alumnoclase.objects.filter(user__id=id,clase__curso__id=curso_id)
          alumno_clase_list = list(alumno_clase_result)
          context['alumno_clase_list'] = alumno_clase_list
          context['user'] = user
          context['curso'] = curso
          return context

     def post(self, request, *args, **kwargs):
          form = CalificacionForm(request.POST)
          #id_alumnoclase
          alumno_clase = request.POST['alumnoclase']
          alumno_clase_object = Alumnoclase.objects.get(pk=alumno_clase)
          evaluacion = request.POST['evaluacion']
          note = request.POST['note']
  
          if form.is_valid():
               calificacion_object = Calificacion.objects.filter(alumnoclase__user__id=alumno_clase_object.user.id, evaluacion=evaluacion).first()
               print(calificacion_object)
               if calificacion_object:
                    print('entro 1')
                    calificacion_object.alumnoclase = alumno_clase_object
                    calificacion_object.note = note
                    calificacion_object.save()
               else:
                    print('entro 2')
                    calificacion = form.save()
                    calificacion.save()
               cursos = query_list_curso(self.request.user)
               return redirect(reverse_lazy('apps:calificacionlist')+ '?ok')

          return redirect(request.META.get('HTTP_REFERER'))

     success_url = reverse_lazy('apps:calificacionlist')
