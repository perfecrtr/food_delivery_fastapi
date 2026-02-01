"""
Bcrypt implementation of PasswordHasher
"""

import bcrypt
import re

from app.domain.services.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Bcrypt implementation of password hashing service"""
    
    BCRYPT_PATTERN = r'^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{22}[./A-Za-z0-9]{31}$'
    
    def __init__(self, rounds: int = 12):
        """
        Initialize bcrypt password hasher
        """
        self.rounds = rounds
    
    def hash(self, password: str) -> str:
        """
        Hash a plain password using bcrypt
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if plain password matches hashed password
        """
        if not plain_password:
            return False
        
        if not hashed_password:
            raise ValueError("Hashed password cannot be empty")
        
        if not self._is_valid_bcrypt_hash(hashed_password):
            raise ValueError(
                "Invalid bcrypt hash format. Expected format: "
                "$2a$XX$[salt][hash] or $2b$XX$[salt][hash] or $2y$XX$[salt][hash]"
            )
        
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            raise ValueError(f"Error verifying password: {str(e)}")
    
    def _is_valid_bcrypt_hash(self, hashed_password: str) -> bool:
        """
        Validate bcrypt hash format
        """
        if not hashed_password or len(hashed_password) < 60:
            return False
        
        return bool(re.match(self.BCRYPT_PATTERN, hashed_password))

