from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Perfil, Menu, Privilegio
from authentication.models import User
from .forms import PerfilForm, UserCreationFormWithEmail
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .decorador import RequiredUserAttribute


# Create your views here.

# view perfil
class PerfilListView(ListView):# ListView para usar una Lista de instancias de la clase Page
    model = Perfil
    template_name = 'perfil/perfil_list.html'
    context_object_name = 'perfil_list'
    paginate_by = 5

    def get_queryset(self):
      queryset_perfil = Perfil.objects.filter( Q(estado='001') | Q(estado='002'))
      return queryset_perfil

@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
# @RequiredUserAttribute(attribute = 'profesor', redirect_to_url = '/')
class PerfilDetailView(DetailView):# DetailView para usar instancia  de la clase Page, en la vista puedo usar object o el nombre del modelo page
    model = Perfil
    template_name = 'perfil/perfil_view.html'
    context_object_name = 'perfil_view'
    slug_field = 'nombre'

    def get_context_data(self,*args, **kwargs):
          context = super(PerfilDetailView, self).get_context_data(**kwargs)
          menu_list = Menu.objects.filter(estado='001')
          pagina = self.kwargs['pagina']
          context['menu_list'] = menu_list
          context['pagina'] = pagina
          return context

class PerfilCreateView(CreateView):
    model = Perfil
    template_name = 'perfil/perfil_create.html'
    form_class = PerfilForm

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilCreateView, self).get_context_data(**kwargs)
        menu_list = Menu.objects.filter(estado='001')
        context['menu_list'] = menu_list
        return context

    def post(self, request, *args, **kwargs):
        form = PerfilForm(request.POST)
        
        if form.is_valid():
            perfil = form.save()
            perfil.save()
            try:
                menu_list = Menu.objects.filter(estado='001')

                for menu in menu_list:
                    for menu_item in menu.menuitems.all():
                        view = self.request.POST.get('view_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                        create = self.request.POST.get('create_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                        update = self.request.POST.get('update_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                        delete = self.request.POST.get('delete_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                        privilegio = Privilegio.objects.create(perfil=perfil,menuitem=menu_item,view=view,create=create,delete=delete,update=update)
                        privilegio.save()
                
                messages.add_message(request, messages.SUCCESS, 'El Perfil se registro con exito.')
            except:
                messages.add_message(request, messages.ERROR, 'El Perfil no se registro.')
            
            return redirect(reverse_lazy('seguridad:perfilview', args=[perfil.id,1]))
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class PerfilUpdateView(UpdateView):
    model = Perfil
    template_name = 'perfil/perfil_update.html'
    form_class = PerfilForm

    def get_context_data(self, *args, **kwargs):
        context = super(PerfilUpdateView, self).get_context_data(**kwargs)
        menu_list = Menu.objects.filter(estado='001')
        privilegio_list = Privilegio.objects.filter(perfil__id = self.object.id)
        pagina = self.kwargs['pagina']
        context['pagina'] = pagina
        context['menu_list'] = menu_list
        context['privilegio_list'] = privilegio_list
        return context


    def post(self, request, *args, **kwargs):
      id_perfil = self.get_object().id
      form = PerfilForm(request.POST, instance=Perfil.objects.get(pk=id_perfil))
      pagina = self.kwargs['pagina']

      try:
        print(form.is_valid())
        if form.is_valid():
            perfil = Perfil.objects.get(pk=id_perfil)
            print(id_perfil)
            print(self.request.POST.get('nombre'))
            print(self.request.POST.get('descripcion'))
            print(self.request.POST.get('estado'))
            print(self.request.POST.get('is_admin') == 'on' if True else False)

            perfil.nombre = self.request.POST.get('nombre')
            perfil.descripcion = self.request.POST.get('descripcion')
            perfil.estado = self.request.POST.get('estado')
            perfil.is_admin = self.request.POST.get('is_admin') == 'on' if True else False
            perfil.save()
            
            #actualiza todos los hijos usuarios como administrador
            User.objects.filter(perfil__id = id_perfil).update(is_superuser=perfil.is_admin)

            menu_list = Menu.objects.filter(estado='001')

            for menu in menu_list:
                for menu_item in menu.menuitems.all():
                    view = self.request.POST.get('view_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                    create = self.request.POST.get('create_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                    update = self.request.POST.get('update_'+ str(menu.id)+'_'+ str(menu_item.id), '0')
                    delete = self.request.POST.get('delete_'+ str(menu.id)+'_'+ str(menu_item.id), '0')

                    privilegio = Privilegio.objects.filter(menuitem__id=menu_item.id,perfil__id=perfil.id).first()
                    privilegio.view = view
                    privilegio.create = create
                    privilegio.update = update
                    privilegio.delete = delete
                    privilegio.save()
          
            messages.add_message(request, messages.SUCCESS, 'El Perfil se actualizo con exito.')
        else:
            menu_list = Menu.objects.filter(estado='001')
            privilegio_list = Privilegio.objects.filter(perfil__id = id_perfil)
            context = {'form': form, 'menu_list': menu_list, 'privilegio_list': privilegio_list}
            return render(self.request, self.template_name, context)
      except Exception as e:
          print(e)
          messages.add_message(request, messages.ERROR, 'ERROR: El Perfil no se actualizo.')
      
      return redirect(reverse_lazy('seguridad:perfilview', args=[id_perfil,pagina]) )

class PerfilActivateUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        perfil = Perfil.objects.get(pk=kwargs['pk'])
        if perfil:
            perfil.estado = '001'
            perfil.save()
        return redirect(reverse_lazy('seguridad:perfileslist'))

class PerfilDesactivateUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        perfil = Perfil.objects.get(pk=kwargs['pk'])
        if perfil:

            if perfil.is_admin:
                if not Perfil.objects.filter(is_admin=True, estado='001').exclude(id=kwargs['pk']).exists():
                    messages.add_message(self.request, messages.ERROR, 'No puede desactivar, el unico perfil "Admin" del sistema..')
                    return redirect(reverse_lazy('seguridad:perfileslist'))

            perfil.estado = '002'
            perfil.save()
        return redirect(reverse_lazy('seguridad:perfileslist'))

class PerfilDeleteView(UpdateView):
    def post(self, request, *args, **kwargs):
        idDeletePerfil = self.request.POST.get('idDeletePerfil')
        pagina = self.request.POST.get('pagina')
        if idDeletePerfil:
          perfil = Perfil.objects.get(pk=int(idDeletePerfil))
          if perfil:

                if perfil.is_admin:
                    if not Perfil.objects.filter(is_admin=True).exclude(id=idDeletePerfil).exists():
                        messages.add_message(self.request, messages.ERROR, 'No puede eliminar, el unico perfil "Admin" del sistema..')
                        return redirect(reverse_lazy('seguridad:perfileslist') + '?page=' + pagina)

                Perfil.objects.get(pk=int(idDeletePerfil)).delete()
                messages.add_message(self.request, messages.SUCCESS, 'El Perfil se elimino con exito.')

        return redirect(reverse_lazy('seguridad:perfileslist') + '?page=' + pagina)

# view usuario
class UsuarioListView(ListView):# ListView para usar una Lista de instancias de la clase Page
    model = User
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuario_list'
    paginate_by = 5

    def get_queryset(self):
      queryset_usuario = User.objects.filter( Q(estado='001') | Q(estado='002'))
      return queryset_usuario

class UsuarioDetailView(DetailView):# DetailView para usar instancia  de la clase Page, en la vista puedo usar object o el nombre del modelo page
    model = User
    template_name = 'usuario/usuario_view.html'
    context_object_name = 'usuario_view'
    # slug_field = 'nombre'

    def get_context_data(self,*args, **kwargs):
          context = super(UsuarioDetailView, self).get_context_data(**kwargs)
          pagina = self.kwargs['pagina']
          context['pagina'] = pagina
          return context

class UsuarioActivateUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        usuario = User.objects.get(pk=kwargs['pk'])
        if usuario:
            usuario.estado = '001'
            usuario.save()
        return redirect(reverse_lazy('seguridad:usuarioslist'))

class UsuarioDesactivateUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        usuario = User.objects.get(pk=kwargs['pk'])
        if usuario:
            if usuario.is_superuser:
                if not User.objects.filter(is_superuser=True, estado='001').exclude(id=kwargs['pk']).exists():
                    messages.add_message(self.request, messages.ERROR, 'No puede desactivar, el unico usuario "Admin" del sistema..')
                    return redirect(reverse_lazy('seguridad:usuarioslist'))

            usuario.estado = '002'
            usuario.save()
        return redirect(reverse_lazy('seguridad:usuarioslist'))

class UsuarioDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        idDeleteUsuario = self.request.POST.get('idDeleteUsuario')
        pagina = self.request.POST.get('pagina')
        if idDeleteUsuario:
            usuario = User.objects.get(pk=int(idDeleteUsuario))
            if usuario:
                if usuario.is_superuser:
                    if not User.objects.filter(is_superuser=True).exclude(id=idDeleteUsuario).exists():
                        messages.add_message(self.request, messages.ERROR, 'El Usuario que desea eliminar es el unico administrador del sistema, siempre debe de existir uno como minimo.')
                        return redirect(reverse_lazy('seguridad:usuarioslist') + '?page=' + pagina)

                User.objects.get(pk=int(idDeleteUsuario)).delete()
                messages.add_message(self.request, messages.SUCCESS, 'El Usuario se elimino con exito.')

        return redirect(reverse_lazy('seguridad:usuarioslist') + '?page=' + pagina)

class UsuarioUpdateView(UpdateView):
    model = User
    form_class = UserCreationFormWithEmail
    template_name = 'usuario/usuario_edit.html'

    def get_success_url(self):
        id_usuario = self.get_object().id
        pagina = self.kwargs['pagina']
        messages.add_message(self.request, messages.SUCCESS, 'El Usuario se actualizo con exito.')
        return reverse_lazy('seguridad:usuarioview', args=[id_usuario,pagina])

class UsuarioCreateView(CreateView):
    model = User
    form_class = UserCreationFormWithEmail
    template_name = 'usuario/usuario_create.html'

    def get_success_url(self):
      id_usuario = self.object.id
      # pagina = self.kwargs['pagina']
      messages.add_message(self.request, messages.SUCCESS, 'El Usuario se creo con exito.')
      return reverse_lazy('seguridad:usuarioview', args=[id_usuario,1])
    
    
    # def get(self, request, *args, **kwargs):
    #       form = UsuarioForm()
    #       context = {'form': form}
    #       return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #       form = UsuarioForm(request.POST)
    #       print(form.is_valid())
    #       if form.is_valid():
    #           form.save()
    #       context = {'form': form}
    #       return render(request, self.template_name, context)
