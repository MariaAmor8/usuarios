from django.db import models
from usuarios.cifrado import decrypt

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
        estudiante.nombre = str(dto.get('nombre', ''))
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
    
    @staticmethod
    def from_mongo_decrypted(dto):
        estudiante = Estudiante()
        estudiante.id = str(dto.get('_id', ''))
        estudiante.nombre = decrypt(str(dto.get('nombre', '')))
        estudiante.numId = decrypt(str(dto.get('numId', '')))
        estudiante.telefono = decrypt(str(dto.get('telefono', '')))
        estudiante.colegio = decrypt(dto.get('colegio', ''))
        estudiante.carnet = decrypt(str(dto.get('carnet', '')))
        estudiante.grado = decrypt(str(dto.get('grado', '')))
        estudiante.curso = decrypt(dto.get('curso', ''))
        estudiante.emailPadreFamilia = decrypt(dto.get('emailPadreFamilia', ''))
        #estudiante.pagos = dto.get('pagos', []),
        # Desencriptar los pagos
        estudiante.pagos = [
            Pago.from_mongo_decrypted(pago) for pago in dto.get('pagos', [])
        ]
        estudiante.saldo = decrypt(str(dto.get('saldo', 0.0)))
        return estudiante
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'numId': self.numId,
            'telefono': self.telefono,
            'colegio': self.colegio,
            'carnet': self.carnet,
            'grado': self.grado,
            'curso': self.curso,
            'emailPadreFamilia': self.emailPadreFamilia,
            'pagos': [pago.to_dict() for pago in self.pagos],  # Convertir cada pago a dict
            'saldo': self.saldo,
        }


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
    
    @staticmethod
    def from_mongo_decrypted(dto):
        pago =Pago()
        pago.id = str(dto.get('_id', ''))
        pago.valor = decrypt(str(dto.get('valor', '')))
        pago.causacion = decrypt(str(dto.get('causacion', '')))
        pago.fechaLimite = decrypt(str(dto.get('fechaLimite', '')))
        pago.estadoPago = decrypt(str(dto.get('estadoPago', 'False')))
        pago.mes = decrypt(str(dto.get('mes', '')))
        return pago
    
    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'causacion': self.causacion,
            'fechaLimite': self.fechaLimite,
            'estadoPago': self.estadoPago,
            'mes': self.mes,
        }
