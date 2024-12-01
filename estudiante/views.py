from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId
import estudiante.logic as estudiante_logic

# Create your views here.
@api_view(["GET", "POST"])
def students(request):
    """Maneja las solicitudes para obtener y crear estudiantes."""
    
    if request.method == "GET":
        # Obtener todos los estudiantes
        students = estudiante_logic.getStudents()
        return JsonResponse([student.__dict__ for student in students], safe=False)

    if request.method == "POST":
        try:
            # Crear un nuevo estudiante
            data = JSONParser().parse(request)
            student = estudiante_logic.createStudent(data)
            response = {
                "objectId": str(student.id),
                "message": f"Estudiante {student.nombre} creado en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET", "DELETE"])
def studentDetail(request, student_id):
    """Maneja las solicitudes para un estudiante específico: obtener o eliminar."""
    
    if request.method == "GET":
        try:
            # Obtener detalles de un estudiante por su numId
            student = estudiante_logic.getStudent(student_id)
            return JsonResponse(student.__dict__, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

    if request.method == "DELETE":
        # Eliminar un estudiante por su numId
        result = estudiante_logic.deleteEstudiante(student_id)
        response = {
            "objectID": str(result),
            "message": "Estudiante eliminado de la base de datos"
        }
        return JsonResponse(response, safe=False)


@api_view(["POST"])
def studentAddPago(request, student_id):
    """Maneja la solicitud para agregar un pago a un estudiante."""
    
    if request.method == "POST":
        try:
            # Agregar un pago al estudiante
            data = JSONParser().parse(request)
            add_result = estudiante_logic.add_pago(student_id, data)
            response = {
                "result": str(add_result),
                "message": f"Pago agregado al estudiante con ID {student_id}"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)