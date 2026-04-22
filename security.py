from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

class CyberVault:
    @staticmethod
    def gerar_chave(senha: str, salt: bytes):
        """Deriva uma chave de 32 bytes (256 bits) a partir da senha e do salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(senha.encode())

    @staticmethod
    def criptografar(dados: str, senha: str):
        """Criptografa o texto usando AES-256 no modo CFB."""
        salt = os.urandom(16)
        iv = os.urandom(16)
        chave = CyberVault.gerar_chave(senha, salt)
        
        cipher = Cipher(algorithms.AES(chave), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        dados_criptografados = encryptor.update(dados.encode()) + encryptor.finalize()
        
        # Retorna o pacote binário completo: salt (16 bytes) + IV (16 bytes) + dados
        return salt + iv + dados_criptografados

    @staticmethod
    def descriptografar(dados_brutos: bytes, senha: str):
        """Extrai os componentes e descriptografa os dados para texto plano."""
        salt = dados_brutos[:16]
        iv = dados_brutos[16:32]
        conteudo = dados_brutos[32:]
        
        chave = CyberVault.gerar_chave(senha, salt)
        
        cipher = Cipher(algorithms.AES(chave), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        texto_claro = decryptor.update(conteudo) + decryptor.finalize()
        return texto_claro.decode('utf-8')