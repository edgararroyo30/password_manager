import json


class Keys():

    def __init__(self):
        pass

    def public_table_key():
        with open("C:/Users/edgar/OneDrive/Escritorio/Current Projects/Password Manager/Version 1.2.5 - TK & CTK/keys/keys.json", "r") as file:
            config = json.load(file)
        key = config["PUBLIC_TABLE_KEY"]

        return key

    def private_db_key():
        with open("C:/Users/edgar/OneDrive/Escritorio/Current Projects/Password Manager/Version 1.2.5 - TK & CTK/keys/keys.json", "r") as file:
            config = json.load(file)
        key = config["PRIVATE_DB_KEY"]

        return key

    def public_db_key():
        with open("C:/Users/edgar/OneDrive/Escritorio/Current Projects/Password Manager/Version 1.2.5 - TK & CTK/keys/keys.json", "r") as file:
            config = json.load(file)
        key = config["PUBLIC_DB_KEY"]

        return key

    def private_table_key():
        with open("C:/Users/edgar/OneDrive/Escritorio/Current Projects/Password Manager/Version 1.2.5 - TK & CTK/keys/keys.json", "r") as file:
            config = json.load(file)
        key = config["PRIVATE_TABLE_KEY"]

        return key
