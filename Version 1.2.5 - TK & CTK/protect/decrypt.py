from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import bcrypt
from protect.key import Keys

def decrypt(user_data):

        private_key_string = Keys.private_db_key()
        private_key_bytes = private_key_string.encode('utf-8')
        loaded_private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None)

        get_password = user_data.password

        decrypted_data = loaded_private_key.decrypt(
            get_password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_data

def encrypt(user_data):

	decrypted_password = decrypt(user_data)

	public_key_string = Keys.public_table_key()
    public_key_bytes = public_key_string.encode('utf-8')
    loaded_public_key = serialization.load_pem_public_key(public_key_bytes)

    encrypted_password = loaded_public_key.encrypt(
        decrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )