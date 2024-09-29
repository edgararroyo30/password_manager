import json
import keyring
import base64

class Keys():

    def __init__(self):
        pass

    def public_table_key(service_name):
        public_key_encoded = keyring.get_password(service_name, 'public_key')

        if public_key_encoded:
            public_key = public_key_encoded
            return public_key
        else:
            raise EnvironmentError("Keys not found in Windows Credential Manager.")


    def private_table_key(service_name):
        key_name = "private_key"
        key_parts = []
        i = 0

        while True:
            part = keyring.get_password(service_name, f'{key_name}_part_{i}')
            if part is None:
                break
            key_parts.append(base64.b64decode(part.encode('utf-8')))
            i += 1

        if not key_parts:
            raise EnvironmentError(f"No parts of the {key_name} key found in Windows Credential Manager.")
        
        return b''.join(key_parts)


#print(Keys.public_table_key("Password_keys"))