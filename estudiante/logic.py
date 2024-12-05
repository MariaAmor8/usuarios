from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime
from estudiante.models import Estudiante, Pago
from usuarios.cifrado import encrypt, decrypt

def getStudents():
    """Obtiene todos los estudiantes de la base de datos"""
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos

    estudiantes_collection = db['estudiantes']
    estudiantes_db = estudiantes_collection.find({})

    estudiantes = []
    estudiantes += [Estudiante.from_mongo_decrypted(estudiante) for estudiante in estudiantes_db]
    
    client.close()
    return estudiantes

def getStudent(numId):
    """Obtiene un estudiante dado su numId"""
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos

    estudiantes_collection = db['estudiantes']
    numIdEncript = encrypt(numId)
    estudiante = estudiantes_collection.find_one({'numId': numIdEncript}) 

    client.close()

    if estudiante is None:
        raise ValueError('Estudiante no encontrado')
    

    return Estudiante.from_mongo_decrypted(estudiante)


def verifyEstData(data):
    if 'nombre' not in data:
        raise ValueError('name is required')
    
    estudiante = Estudiante()
    estudiante.nombre = data['nombre']
    estudiante.numId = data['numId']
    estudiante.telefono = data['telefono']
    estudiante.colegio = data['colegio']
    estudiante.carnet = data['carnet']
    estudiante.grado = data['grado']
    estudiante.curso = data['curso']
    estudiante.emailPadreFamilia = data['emailPadreFamilia']
    
    return estudiante


def createStudent(data):
    """Crea un nuevo estudiante en la base de datos"""
    
    estudiante = verifyEstData(data)
    estudiante.saldo = 0
    # Crear el estudiante en MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    
    estudiante.id = estudiantes_collection.insert(
        {
            'nombre': encrypt(estudiante.nombre),
            'numId': encrypt(estudiante.numId),
            'telefono': encrypt(estudiante.telefono), 
            'colegio': encrypt(estudiante.colegio),
            'carnet': encrypt(estudiante.carnet),
            'grado': encrypt(estudiante.grado),
            'curso': encrypt(estudiante.curso),
            'emailPadreFamilia': encrypt(estudiante.emailPadreFamilia),
            'saldo': encrypt(str(estudiante.saldo))
        }
        )
    
    client.close()
    return estudiante

def deleteEstudiante(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    result =  estudiantes_collection.delete_one({'_id': ObjectId(id)})
    client.close()
    return result

def verifyPagoData(data):
    pago = Pago()
    pago.valor = data['valor']
    pago.causacion = data['causacion']
    pago.fechaLimite = data['fechaLimite']
    #if not isinstance(data['estadoPago'], bool):
    #    raise ValueError("estadoPago debe ser un valor booleano (True o False)")
    pago.estadoPago = data['estadoPago']
    pago.mes = data['mes']
    
    return pago

def add_pago(est_numId, data):
    """Agrega un nuevo pago al estudiante especificado por su numId y actualiza el saldo si no está pagado."""
    
    # Verificar los datos del pago
    new_pago = verifyPagoData(data)
    
    # Conectar a la base de datos
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db
    estudiantes_collection = db['estudiantes']
    
    # Buscar el estudiante por numId
    estudiante = estudiantes_collection.find_one({'numId': encrypt(est_numId)})
    if estudiante is None:
        client.close()
        raise ValueError('Estudiante no encontrado')
    
    # Convertir el estudiante a un objeto
    estudiante = Estudiante.from_mongo(estudiante)
    
    # Verificar si el valor es un string y convertirlo a float
    try:
        valor_pago = float(new_pago.valor)
    except ValueError:
        client.close()
        raise ValueError(f"El valor del pago '{new_pago.valor}' no es válido como número.")
    
    # Agregar el nuevo pago a la lista de pagos
    new_pago_dict = {
        'valor': encrypt(str(valor_pago)),  # Guardamos como string
        'causacion': encrypt(new_pago.causacion),
        'fechaLimite': encrypt(new_pago.fechaLimite),
        'estadoPago': encrypt(new_pago.estadoPago),
        'mes': encrypt(new_pago.mes)
    }
    estudiante.pagos.append(new_pago_dict)
    
    # Convertir el saldo actual a float antes de hacer el cálculo
    try:
        saldo_actualizado = float(decrypt(estudiante.saldo))
    except ValueError:
        client.close()
        raise ValueError(f"El saldo del estudiante '{est_numId}' no es un número válido.")
    
    # Calcular el nuevo saldo solo si el pago no ha sido pagado
    if new_pago.estadoPago.lower() == 'false':  # Si el pago no está pagado
        saldo_actualizado += valor_pago
    
    # Convertir el saldo actualizado de vuelta a string para guardarlo
    saldo_actualizado_str = str(saldo_actualizado)
    
    # Actualizar el estudiante en la base de datos
    result = estudiantes_collection.update_one(
        {'numId': encrypt(est_numId)},
        {
            '$set': {
                'pagos': estudiante.pagos,
                'saldo': encrypt(saldo_actualizado_str)  # Guardar como string
            }
        }
    )
    
    client.close()
    return result.modified_count

#------------------------------ metodos sin ecnriptar y desencriptar---------------------------


def getEstudiantes():
    """Obtiene todos los estudiantes de la base de datos"""
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    estudiantes_db = estudiantes_collection.find({})
    estudiantes = []
    estudiantes += [Estudiante.from_mongo(estudiante) for estudiante in estudiantes_db]
    client.close()
    return estudiantes

def getEstudiante(numId):
    """Obtiene un estudiante dado su numId"""
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    estudiante = estudiantes_collection.find_one({'numId': numId}) 
    client.close()
    if estudiante is None:
        raise ValueError('Estudiante no encontrado')
    return Estudiante.from_mongo(estudiante)

def createEstiudiante(data):
    """Crea un nuevo estudiante en la base de datos"""
    
    estudiante = verifyEstData(data)
    estudiante.saldo = 0
    # Crear el estudiante en MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    
    estudiante.id = estudiantes_collection.insert(
        {
            'nombre': estudiante.nombre,
            'numId': estudiante.numId,
            'telefono': estudiante.telefono, 
            'colegio': estudiante.colegio,
            'carnet': estudiante.carnet,
            'grado': estudiante.grado,
            'curso': estudiante.curso,
            'emailPadreFamilia': estudiante.emailPadreFamilia,
            'saldo': str(estudiante.saldo)
        }
        )
    
    client.close()
    return estudiante


def agregar_pago(est_numId, data):
    """Agrega un nuevo pago al estudiante especificado por su numId y actualiza el saldo si no está pagado."""
    
    # Verificar los datos del pago
    new_pago = verifyPagoData(data)
    
    # Conectar a la base de datos
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db
    estudiantes_collection = db['estudiantes']
    
    # Buscar el estudiante por numId
    estudiante = estudiantes_collection.find_one({'numId': est_numId})
    if estudiante is None:
        client.close()
        raise ValueError('Estudiante no encontrado')
    
    # Convertir el estudiante a un objeto
    estudiante = Estudiante.from_mongo(estudiante)
    
    # Agregar el nuevo pago a la lista de pagos
    new_pago_dict = {
        'valor': new_pago.valor,
        'causacion': new_pago.causacion,
        'fechaLimite': new_pago.fechaLimite,
        'estadoPago': new_pago.estadoPago,
        'mes': new_pago.mes
    }
    estudiante.pagos.append(new_pago_dict)
    
    # Calcular el nuevo saldo solo si el pago no ha sido pagado
    saldo_actualizado = float(estudiante.saldo)
    if  new_pago.estadoPago.lower() == 'false':  # Si el pago no está pagado
        saldo_actualizado += float(new_pago.valor)
    
    # Actualizar el estudiante en la base de datos
    result = estudiantes_collection.update_one(
        {'numId': est_numId},
        {
            '$set': {
                'pagos': estudiante.pagos,
                'saldo': str(saldo_actualizado)
            }
        }
    )
    
    client.close()
    return result.modified_count

def deleteAll():
    client = MongoClient(settings.MONGO_CLI)
    db = client.usuarios_db  # Asegúrate de que 'usuarios_db' sea el nombre correcto de la base de datos
    estudiantes_collection = db['estudiantes']
    result = estudiantes_collection.delete_many({})
    client.close()
    return result.deleted_count