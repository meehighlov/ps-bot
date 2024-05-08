from cryptography.fernet import Fernet


class CryptographyPasswordUtils:
    def __init__(self, fernet: Fernet):
        self.fernet = fernet

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()

