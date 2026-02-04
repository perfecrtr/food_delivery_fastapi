"""
Abstract interface for password hashing service
"""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Abstract interface for password hashing and verification"""
    
    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Hash a plain password
        """
        pass
    
    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if plain password matches hashed password
        """
        pass





