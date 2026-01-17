"""
Sistema de logging profesional para el bot
"""

import logging
from datetime import datetime
from pathlib import Path
from config import Config


class Logger:
    """Sistema de logging del bot"""
    
    _instances = {}
    
    def __new__(cls, name="bot"):
        """Singleton pattern para cada nombre de logger"""
        if name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[name] = instance
        return cls._instances[name]
    
    def __init__(self, name="bot"):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Evitar duplicados
        if self.logger.handlers:
            return
        
        # Formato de logs
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola
        if Config.LOG_TO_CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Handler para archivo
        if Config.LOG_TO_FILE:
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = Config.LOGS_DIR / f"{name}_{today}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Log de nivel DEBUG"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log de nivel INFO"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log de nivel WARNING"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de nivel ERROR"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log de nivel CRITICAL"""
        self.logger.critical(message)