from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import keyring
import base64

class KeyGeneration():

    def __init__(self):
        self.store()

    def create_keys(self):

        private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend)
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                    )

        public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)

        return private_key_pem.decode('utf-8'), public_key_pem.decode('utf-8')

    def split_key(self, data, chunk_size):
        return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    def store_large_encryption_key(self, service_name, key_name, key_data, chunk_size=500):
        key_parts = self.split_key(key_data.encode('utf-8'), chunk_size)

        for i, part in enumerate(key_parts):
            keyring.set_password(service_name, f'{key_name}_part_{i}', base64.b64encode(part).decode('utf-8'))

        #print(f"{len(key_parts)} parts of the {key_name} key have been securely stored in Windows Credential Manager.")

    def check_keys_exist(self,service_name):
        private_key = keyring.get_password(service_name, "private_key")
        public_key = keyring.get_password(service_name, "public_key")

        if private_key and public_key:
            return True
        else:
            return False

    def store_encryption_keys(self,service_name, private_key, public_key):

        if not self.check_keys_exist(service_name):
            self.store_large_encryption_key (service_name, "private_key", private_key)
            keyring.set_password(service_name, "public_key", public_key)
            #print("Keys have been securely stored.")
            #print(keyring.get_password(service_name, "private_key"))
        else: 
            print("Keys already exist. Skipping storage.")

    def store(self):

        private_key_passwords, public_key_passwords = self.create_keys()

        self.store_encryption_keys("Password_keys", private_key_passwords, public_key_passwords)



