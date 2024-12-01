from django.urls import path
from . import views

urlpatterns = [
    path('students', views.students, name='students'),
    path('students/<str:student_id>', views.studentDetail, name='student_detail'),
    path('students/<str:student_id>/pagos', views.studentAddPago, name='student_add_pago'),
]