"""
Abstract interface for token service
"""

from abc import ABC, abstractmethod
from typing import Dict

from app.domain.value_objects.token import AccessToken, RefreshToken


class TokenService(ABC):
    """Abstract interface for token generation and validation"""
    
    @abstractmethod
    def generate_access_token(self, user_id: int) -> AccessToken:
        """
        Generate access token for user
        """
        pass
    
    @abstractmethod
    def generate_refresh_token(self, user_id: int) -> RefreshToken:
        """
        Generate refresh token for user
        """
        pass
    
    @abstractmethod
    def verify_access_token(self, token: str) -> Dict:
        """
        Verify and decode access token
        """
        pass
    
    @abstractmethod
    def verify_refresh_token(self, token: str) -> Dict:
        """
        Verify and decode refresh token
        """
        pass

