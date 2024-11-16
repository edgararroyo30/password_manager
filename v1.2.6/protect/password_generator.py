import secrets

def generate_password():
    """
    Creates a save password
    """
    password_lenght = 12
    password = secrets.token_urlsafe(password_lenght)
    return password