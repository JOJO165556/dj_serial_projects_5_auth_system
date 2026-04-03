# Protéger API dès l'entrée

import re
from rest_framework.exceptions import ValidationError

def validate_email(email: str):
    pattern = r"[^@]+@[^@]+\.[^@]+"

    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")

    return email

def validate_password(password: str):
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters")

    return password