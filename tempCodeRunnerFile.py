SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)