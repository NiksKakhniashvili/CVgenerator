from rest_framework.exceptions import ValidationError


def emailvalidator(email):
    if not email.endswith("@makingscience.com"):
        raise ValidationError("invalid email, you can only register with makingscience")