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