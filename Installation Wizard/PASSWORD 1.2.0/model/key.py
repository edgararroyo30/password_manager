import os


def public_table_key():
    key = os.environ.get("Public_table_key")

    return key


def private_db_key():
    key = os.environ.get("Private_db_key")

    return key

def public_db_key():
    key = os.environ.get("Public_db_key")

    return key

def private_table_key():
    key = os.environ.get("private_table_key")

    return key


    