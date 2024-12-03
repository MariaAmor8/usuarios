from django.db import models

# Create your models here.
class Estudiante():
    id = str()
    nombre = str()
    numId= str()
    telefono= str()
    colegio = str()
    carnet = str()
    grado = str()
    curso = str()
    emailPadreFamilia = str()
    pagos = list()
    saldo = str() 
    
    def __str__(self):
        return self.nombre + " - " + self.numId
    
    
    @staticmethod
    def from_mongo(dto):
        estudiante = Estudiante()
        estudiante.id = str(dto.get('_id', ''))
        estudiante.nombre = dto.get('nombre', '')
        estudiante.numId = str(dto.get('numId', ''))
        estudiante.telefono = str(dto.get('telefono', ''))
        estudiante.colegio = dto.get('colegio', '')
        estudiante.carnet = str(dto.get('carnet', ''))
        estudiante.grado = str(dto.get('grado', ''))
        estudiante.curso = dto.get('curso', '')
        estudiante.emailPadreFamilia = dto.get('emailPadreFamilia', '')
        estudiante.pagos = dto.get('pagos', [])
        estudiante.saldo = str(dto.get('saldo', 0.0))
        return estudiante


class Pago():
    id = str()
    valor = str()
    causacion= str()
    fechaLimite = str()
    estadoPago = str()
    mes = str()
    
    def __str__(self):
        return self.causacion+" - "+ self.valor
    
    @staticmethod
    def from_mongo(dto):
        pago =Pago()
        pago.id = str(dto.get('_id', ''))
        pago.valor = str(dto.get('valor', ''))
        pago.causacion = str(dto.get('causacion', ''))
        pago.fechaLimite = str(dto.get('fechaLimite', ''))
        pago.estadoPago = str(dto.get('estadoPago', 'False'))
        pago.mes = str(dto.get('mes', ''))
        return pago
