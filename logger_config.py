import logging
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (que já aparece na sua imagem!)
load_dotenv()

def setup_logger(name):
    logger = logging.getLogger(name)
    
    # Lendo se o ambiente é DEV ou PROD
    env = os.getenv("APP_ENV", "PROD")
    
    if not logger.handlers:
        file_handler = logging.FileHandler('blackwallet_system.log')
        
        if env == "DEV":
            formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
            logger.setLevel(logging.DEBUG)
        else:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            logger.setLevel(logging.INFO)
            
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger