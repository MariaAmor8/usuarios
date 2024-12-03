from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# Asegúrate de tener una clave secreta que se almacene de forma segura
def get_key():
    key = os.environ['Key']
    return base64.urlsafe_b64decode(key)  # Devolverla como bytes para usarla

# Cifra un valor de manera determinista
def encrypt(value):
    key = get_key()
    
    # Crear una clave derivada con PBKDF2 (determinista)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'selectedsaltvalue',  # El mismo salt fijo cada vez
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    # Crear el cipher AES
    cipher = Cipher(algorithms.AES(derived_key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Rellenar el valor (padding) para que tenga longitud múltiplo de 16
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(value.encode()) + padder.finalize()

    # Encriptar
    encrypted_value = encryptor.update(padded_data) + encryptor.finalize()

    return base64.urlsafe_b64encode(encrypted_value).decode('utf-8')

# Descifra el valor
def decrypt(value):
    key = get_key()

    # Crear una clave derivada con PBKDF2 (determinista)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'selectedsaltvalue',  # El mismo salt fijo cada vez
        iterations=100000,
        backend=default_backend()
    )
    derived_key = kdf.derive(key)

    # Crear el cipher AES
    cipher = Cipher(algorithms.AES(derived_key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decodificar el valor cifrado
    encrypted_value = base64.urlsafe_b64decode(value)
    
    # Desencriptar
    decrypted_data = decryptor.update(encrypted_value) + decryptor.finalize()

    # Quitar el padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_value = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_value.decode('utf-8')


'''
from cryptography.fernet import Fernet
import os
import base64

# Asegúrate de tener una clave secreta que se almacene de forma segura
def get_key():
    key = os.environ['Key']
    print(str(Fernet.generate_key()))
    try:
        # Verificar que la clave es válida y tiene 32 bytes
        decoded_key = base64.urlsafe_b64decode(key)
        if len(decoded_key) != 32:
            print(len(decoded_key))
            raise ValueError("La clave debe ser de 32 bytes.")
        return key.encode()  # Devolverla como bytes para usarla en Fernet
    except Exception as e:
        raise ValueError(f"Error al procesar la clave: {e}")

# Cifra un valor antes de guardarlo en la base de datos
def encrypt(value):
    cipher_suite = Fernet(get_key())
    encrypted_value = cipher_suite.encrypt(value.encode())
    return encrypted_value.decode('utf-8')  # Devuelve como string

# Descifra el valor cuando se recupera de la base de datos
def decrypt(value):
    cipher_suite = Fernet(get_key())
    decrypted_value = cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
    return decrypted_value
    '''