from werkzeug.security import generate_password_hash, check_password_hash


def set_password(password):
    pw_hash = generate_password_hash(password)
    return pw_hash


def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)
