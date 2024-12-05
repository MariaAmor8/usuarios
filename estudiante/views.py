from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId
import estudiante.logic as estudiante_logic
import requests

# Create your views here.
@api_view(["GET", "POST"])
def students(request):
    """Mostrar todos los estudiantes DESCIFRADOS"""
    
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
            return JsonResponse(student.to_dict(), safe=False)
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
            # Parsear los datos recibidos en el request
            data = JSONParser().parse(request)
            idPago = data.get("idPago")
            if not idPago:
                raise ValueError("El campo 'idPago' es obligatorio")
            
            # Obtener los datos del pago de la otra máquina
            pago = check_pago(idPago)
            if not pago:
                raise ValueError(f"Pago con id {idPago} no encontrado")
            
            # Formatear los datos del pago como strings
            pago_formateado = {
                "id": str(pago["id"]),
                "valor": pago["valor"],
                "causacion": str(pago["causacion"]),
                "fechaLimite": str(pago["fechaLimite"]),
                "estadoPago": str(pago["estado"]).lower(),  # Convertir estado a string
                "mes": str(pago["mes"])
            }

            # Agregar el pago al estudiante
            add_result = estudiante_logic.add_pago(student_id, pago_formateado)
            
            response = {
                "result": str(add_result),
                "message": f"Pago agregado al estudiante con ID {student_id}"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
#------------------------------ metodos sin ecnriptar y desencriptar---------------------------

@api_view(["GET", "POST"])
def estudiantes(request):
    """Maneja las solicitudes para obtener y crear estudiantes SIN cifrar"""
    
    if request.method == "GET":
        # Obtener todos los estudiantes
        students = estudiante_logic.getEstudiantes()
        return JsonResponse([student.__dict__ for student in students], safe=False)
    if request.method == "POST":
        try:
            # Crear un nuevo estudiante
            data = JSONParser().parse(request)
            student = estudiante_logic.createEstiudiante(data)
            response = {
                "objectId": str(student.id),
                "message": f"Estudiante {student.nombre} creado en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
@api_view(["GET", "DELETE"])
def detalleEstudiante(request, student_id):
    """Maneja las solicitudes para un estudiante específico: obtener o eliminar SIN cifrar"""
    
    if request.method == "GET":
        try:
            # Obtener detalles de un estudiante por su numId
            student = estudiante_logic.getEstudiante(student_id)
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
def anadirPago(request, student_id):
    """Maneja la solicitud para agregar un pago a un estudiante SIN cifrar"""
    
    if request.method == "POST":
        try:
            # Agregar un pago al estudiante
            data = JSONParser().parse(request)
            add_result = estudiante_logic.agregar_pago(student_id, data)
            response = {
                "result": str(add_result),
                "message": f"Pago agregado al estudiante con ID {student_id}"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
# =====================================================================

def check_pago(idPago):
    """Obtiene el pago de la otra máquina usando el idPago"""
    try:
        r = requests.get(settings.PATH_CRONOGRAMAS, headers={"Accept": "application/json"})
        r.raise_for_status()  # Lanza una excepción si la respuesta es un error
        pagos = r.json()
        for pago in pagos:
            if pago["id"] == idPago:
                return pago
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error al obtener el pago: {str(e)}")
    
    return None


@api_view(["POST"])
def anadirPago(request, student_id):
    """Maneja la solicitud para agregar un pago a un estudiante SIN cifrar"""
    
    if request.method == "POST":
        try:
            # Parsear los datos recibidos en el request
            data = JSONParser().parse(request)
            idPago = data.get("idPago")
            if not idPago:
                raise ValueError("El campo 'idPago' es obligatorio")
            
            # Obtener los datos del pago de la otra máquina
            pago = check_pago(idPago)
            if not pago:
                raise ValueError(f"Pago con id {idPago} no encontrado")
            
            # Formatear los datos del pago como strings
            pago_formateado = {
                "id": str(pago["id"]),
                "valor": pago["valor"],
                "causacion": str(pago["causacion"]),
                "fechaLimite": str(pago["fechaLimite"]),
                "estadoPago": str(pago["estado"]).lower(),  # Convertir estado a string
                "mes": str(pago["mes"])
            }

            # Agregar el pago al estudiante
            add_result = estudiante_logic.agregar_pago(student_id, pago_formateado)
            
            response = {
                "result": str(add_result),
                "message": f"Pago agregado al estudiante con ID {student_id}"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
@api_view(["GET"])
def deleteAll(request):
    """Elimina todos los estudiantes de la base de datos"""
    try:
        # Llamar a la función para eliminar todos los estudiantes
        deleted_count = estudiante_logic.deleteAll()
        response = {
            "message": f"Se eliminaron {deleted_count} estudiantes de la base de datos"
        }
        return JsonResponse(response, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)