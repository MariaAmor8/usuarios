from django.urls import path
from . import views

urlpatterns = [
    path('students', views.students, name='students'),
    path('students/<str:student_id>', views.studentDetail, name='student_detail'),
    path('students/<str:student_id>/pagos', views.studentAddPago, name='student_add_pago'),
    path('estudiantes', views.estudiantes, name='estudiantes'),
    path('estudiantes/<str:student_id>', views.detalleEstudiante, name='estudiante_detail'),
    path('estudiantes/<str:student_id>/pagos', views.anadirPago, name='estudiante_add_pago'),
    #path('getPagos', views.check_pago, name='Pagos')
]