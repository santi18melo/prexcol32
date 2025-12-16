import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    """Validate that the password meets custom character rules.

    Rules enforced:
    - Minimum length of 8 characters (already enforced by MinimumLengthValidator).
    - Must contain at least one uppercase letter.
    - Must contain at least one lowercase letter.
    - Must contain at least one digit.
    - Must contain at least one special character (e.g., @#$%).
    """

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra minúscula."),
                code='password_no_lower',
            )
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_digit',
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial."
        )
