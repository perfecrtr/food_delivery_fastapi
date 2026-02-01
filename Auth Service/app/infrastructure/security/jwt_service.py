"""
JWT implementation of TokenService
"""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

from app.core.config import settings
from app.domain.services.token_service import TokenService
from app.domain.value_objects.token import AccessToken, RefreshToken


class JWTService(TokenService):
    """JWT implementation of token service"""
    
    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        access_token_expire_minutes: Optional[int] = None,
        refresh_token_expire_days: Optional[int] = None
    ):
        self.secret_key = secret_key or settings.jwt_secret_key
        self.algorithm = algorithm or settings.jwt_algorithm
        self.access_token_expire_minutes = (
            access_token_expire_minutes or settings.access_token_expire_minutes
        )
        self.refresh_token_expire_days = (
            refresh_token_expire_days or settings.refresh_token_expire_days
        )
    
    def generate_access_token(self, user_id: int) -> AccessToken:
        """
        Generate access token for user

        """
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        
        expires_at = datetime.utcnow() + timedelta(
            minutes=self.access_token_expire_minutes
        )
        now = datetime.utcnow()
        
        payload = {
            'sub': str(user_id),  
            'user_id': user_id,
            'type': 'access',
            'exp': int(expires_at.timestamp()),  
            'iat': int(now.timestamp())  
        }
        
        token_value = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return AccessToken(
            value=token_value,
            user_id=user_id,
            expires_at=expires_at
        )
    
    def generate_refresh_token(self, user_id: int) -> RefreshToken:
        """
        Generate refresh token for user
        """
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        
        expires_at = datetime.utcnow() + timedelta(
            days=self.refresh_token_expire_days
        )
        now = datetime.utcnow()
        
        payload = {
            'sub': str(user_id),  
            'user_id': user_id,
            'type': 'refresh',
            'exp': int(expires_at.timestamp()), 
            'iat': int(now.timestamp()) 
        }
        
        token_value = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return RefreshToken(
            value=token_value,
            user_id=user_id,
            expires_at=expires_at
        )
    
    def verify_access_token(self, token: str) -> Dict:
        """
        Verify and decode access token
        """
        return self._verify_token(token, expected_type='access')
    
    def verify_refresh_token(self, token: str) -> Dict:
        """
        Verify and decode refresh token
        """
        return self._verify_token(token, expected_type='refresh')
    
    def _verify_token(self, token: str, expected_type: str) -> Dict:
        """
        Internal method to verify and decode JWT token
        """
        if not token:
            raise ValueError("Token cannot be empty")
        
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            token_type = payload.get('type')
            if token_type != expected_type:
                raise ValueError(
                    f"Invalid token type. Expected '{expected_type}', got '{token_type}'"
                )
            
            user_id = payload.get('user_id')
            if not user_id or user_id <= 0:
                raise ValueError("Invalid user_id in token payload")
            
            if 'exp' in payload and isinstance(payload['exp'], (int, float)):
                payload['exp'] = datetime.utcfromtimestamp(payload['exp'])
            
            if 'iat' in payload and isinstance(payload['iat'], (int, float)):
                payload['iat'] = datetime.utcfromtimestamp(payload['iat'])
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error verifying token: {str(e)}")

