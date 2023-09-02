from .models import Alumnoclase, Curso

def query_list_calificacion(curso_select, user = None):
    query_1 = f'''SELECT usuario.id, curso.id as curso_id, curso.profesor_id, usuario.username, curso.title, calificacion.evaluacion, calificacion.note FROM app_alumnoclase alumnoclase
               inner join (
                    SELECT * from app_clase
               ) clase on (alumnoclase.clase_id = clase.id)
               inner join (
                    SELECT * from authentication_user
               ) usuario on (alumnoclase.user_id = usuario.id)
               inner join (
                    SELECT * from app_curso
               ) curso on (clase.curso_id = curso.id)
               left join (
                    SELECT * from app_calificacion
               ) calificacion on (alumnoclase.id = calificacion.alumnoclase_id)
               where 1 = 1 '''

    query_2 = f'''SELECT usuario.id, curso.id as curso_id, curso.profesor_id, usuario.username,usuario.first_name,usuario.last_name, curso.title FROM app_alumnoclase alumnoclase
               inner join (
                    SELECT * from app_clase
               ) clase on (alumnoclase.clase_id = clase.id)
               inner join (
                    SELECT * from authentication_user
               ) usuario on (alumnoclase.user_id = usuario.id)
               inner join (
                    SELECT * from app_curso
               ) curso on (clase.curso_id = curso.id)
               left join (
                    SELECT * from app_calificacion
               ) calificacion on (alumnoclase.id = calificacion.alumnoclase_id)
               where 1 = 1 '''

    if curso_select:
      query_1 = query_1 + f''' and  curso.id = {curso_select}'''
      query_2 = query_2 + f''' and  curso.id = {curso_select}'''
    
    if user:
      if not user.is_staff and not user.is_superuser:  # es un alumno
        query_1 = query_1 + f''' and  usuario.id = {user.id}'''
        query_2 = query_2 + f''' and  usuario.id = {user.id}'''
      if user.is_staff and not user.is_superuser:  # es un profesor
        query_1 = query_1 + f''' and  curso.profesor_id = {user.id}'''
        query_2 = query_2 + f''' and  curso.profesor_id = {user.id}'''

    query_1 = query_1 + f''' ORDER BY title, username ASC;'''
    query_2 = query_2 + f''' group by usuario.id, curso.id , curso.profesor_id, usuario.username, usuario.first_name, usuario.last_name , curso.title;'''
    
    alumnocurso_list=Alumnoclase.objects.raw(query_1)
    alumnocurso_list2=Alumnoclase.objects.raw(query_2)

    notas_curso_list = []
    for registro in alumnocurso_list2:
          notas_curso = {
                              'alumno' : registro.username,
                              'titulo' : registro.title,
                              'first_name' : registro.first_name,
                              'last_name' : registro.last_name,
                              'id' : registro.id,
                              'curso_id' : registro.curso_id,
                                  'P1': -1,
                                  'P2': -1,
                                  'P3': -1,
                                  'P4': -1,
                                  'EP': -1,
                                  'EF': -1,
                                  'ES': -1,
                                  'PC': -1
                                                  }

          for registro2 in alumnocurso_list:
              if (registro.username == registro2.username and registro.title ==registro2.title):
              
                    if (registro2.evaluacion == 'P1'):
                        notas_curso['P1'] = registro2.note
                    if (registro2.evaluacion == 'P2'):
                        notas_curso['P2'] = registro2.note
                    if (registro2.evaluacion == 'P3'):
                        notas_curso['P3'] = registro2.note
                    if (registro2.evaluacion == 'P4'):
                        notas_curso['P4'] = registro2.note
                    if (registro2.evaluacion == 'EP'):
                        notas_curso['EP'] = registro2.note
                    if (registro2.evaluacion == 'EF'):
                        notas_curso['EF'] = registro2.note
                    if (registro2.evaluacion == 'ES'):
                        notas_curso['ES'] = registro2.note
                    if (registro2.evaluacion == 'PC'):
                        notas_curso['PC'] = registro2.note

          
          notas_curso_list.append(notas_curso)
    return notas_curso_list


def query_list_asistencia(curso_select, asistencia_select, date, user = None):

    alumnoclase_list = Alumnoclase.objects.filter(status=1)

    if curso_select:
         alumnoclase_list = alumnoclase_list.filter(clase__curso__id=curso_select)
        
    if  date:
         alumnoclase_list = alumnoclase_list.filter(clase__date_class = date)
    # else:
    #     date='-'
    if  asistencia_select:
         alumnoclase_list = alumnoclase_list.filter(asistio = asistencia_select)
    
    if user:
      if not user.is_staff and not user.is_superuser:  # es un alumno
        alumnoclase_list = alumnoclase_list.filter(user__id = user.id)
      if user.is_staff and not user.is_superuser:  # es un profesor
        alumnoclase_list = alumnoclase_list.filter(clase__curso__profesor__id=user.id)

    return alumnoclase_list

def query_list_curso(user):
  cursos = Curso.objects.filter(status=1)

  query_curso = f'''SELECT curso.id, curso.title, curso.status FROM app_alumnoclase alumnoclase
	   inner join (
			SELECT * from app_clase
	   ) clase on (alumnoclase.clase_id = clase.id)
	   inner join (
			SELECT * from authentication_user
	   ) usuario on (alumnoclase.user_id = usuario.id)
	   inner join (
			SELECT * from app_curso
	   ) curso on (clase.curso_id = curso.id)
		where 1 = 1 
    '''

  query_curso = query_curso + f''' and  usuario.id = {user.id}'''
  query_curso = query_curso + f''' group by curso.id, curso.title, curso.status '''

  if user:
    
    if not user.is_staff and not user.is_superuser:  # es un alumno
      cursos=Curso.objects.raw(query_curso)

    if user.is_staff and not user.is_superuser:  # es un profesor
      cursos = cursos.filter(profesor = user.id)

  return cursos