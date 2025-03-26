import os
max_send_attempts = os.getenv("MAX_SEND_ATTEMPTS", 3)
code_expiration_minutes = os.getenv("CODE_EXPIRATION_MINUTES", 5)
subjects = {
    "login_notification": "Notificación de inicio de sesión",
    "password_reset": "Restablecimiento de contraseña",
    "email_verification": "Verificación de email"
}