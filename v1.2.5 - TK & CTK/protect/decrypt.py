from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import bcrypt
from protect.key import Keys

def decrypt(user_password):

        private_key_string = Keys.private_table_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None)
        

        decrypted_data = loaded_private_key.decrypt(
            user_password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_data.decode("utf-8")

def encrypt(user_password):

    public_key_string = Keys.public_table_key()
    public_key_bytes = public_key_string.encode('utf-8')
    loaded_public_key = serialization.load_pem_public_key(public_key_bytes)
    user_password_bytes = user_password.encode('utf-8')


    encrypted_password = loaded_public_key.encrypt(
        user_password_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_password

def hash_code(user_code):
    codgio_bytes = user_code.encode('utf-8')
    codigo_hashed = bcrypt.hashpw(codgio_bytes, bcrypt.gensalt())

    return  codigo_hashed

def check_hash(db_code, input_code):
    hashed_password = db_code[0]
    codigo_bytes = input_code.encode('utf-8')


    return bcrypt.checkpw(codigo_bytes, hashed_password)
