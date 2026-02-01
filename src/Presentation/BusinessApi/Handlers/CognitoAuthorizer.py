from fastapi import Request, HTTPException, status
from fastapi.security import SecurityScopes
from jose import jwt, jwk
import requests
import os
from typing import Dict, Optional
import logging
from dotenv import load_dotenv

load_dotenv()

class CognitoAuthorizer:
    def __init__(self):        
        region = os.getenv("COGNITO_JWKS_REGION")
        pool_id = os.getenv("COGNITO_JWKS_POOL_ID")
        
        if not region or not pool_id:
            raise ValueError("Las variables de entorno COGNITO_JWKS_REGION y COGNITO_JWKS_POOL_ID son requeridas")
        
        self.jwks_url = f'https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json'
        self.issuer = f'https://cognito-idp.{region}.amazonaws.com/{pool_id}'
        self.jwks: Optional[Dict] = None
        self.logger = logging.getLogger(__name__)

    def _get_jwks(self) -> Dict:        
        if self.jwks is None:
            try:
                self.logger.warning(f"[WARNING] New HTTP request to {self.jwks_url}")
                response = requests.get(self.jwks_url, timeout=10)
                response.raise_for_status()
                self.jwks = response.json()
            except Exception as e:
                self.logger.error(f"Error al obtener JWKS: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al validar el token"
                )
        return self.jwks

    def _get_signing_key(self, token_header: Dict) -> str:        
        jwks = self._get_jwks()
        kid = token_header.get('kid')
        
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                return jwk.construct(key)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: llave de firma no encontrada"
        )

    def __call__(self, security_scopes: SecurityScopes, request: Request) -> dict:        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorización no proporcionado",
                headers={"WWW-Authenticate": "Bearer"}
            )

        try:
            # Extraer el token del header
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Esquema de autorización inválido",
                    headers={"WWW-Authenticate": "Bearer"}
                )

            # Decodificar el header del token sin verificar
            token_header = jwt.get_unverified_header(token)
            
            # Obtener la llave de firma
            signing_key: str = self._get_signing_key(token_header)
            
            # Decodificar y validar el token
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=['RS256'],
                audience=None,  # Se puede especificar el client_id si es necesario
                issuer=self.issuer,
                options={
                    'verify_aud': False,  # Desactivar verificación de audience
                    'verify_exp': True,   # Verificar expiración
                    'verify_iss': True,   # Verificar issuer
                }
            )

            # Verificar scopes
            token_scopes = set(payload.get('scope', '').split())
            required_scopes = set(security_scopes.scopes)
            missing_scopes = required_scopes - token_scopes
            
            if missing_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized"
                )

            return {
                "sub": payload.get('sub'),
                "username": payload.get('username'),
                "email": payload.get('email'),
                "granted_scopes": list(token_scopes),
                "token_use": payload.get('token_use'),
                "auth_time": payload.get('auth_time'),
                "exp": payload.get('exp')
            }

        except jwt.ExpiredSignatureError:
            raise HTTPArifyException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "Token expired"
                }
            )
        except jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as e:
            self.logger.error(f"Error al validar token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al validar el token"
            )

class HTTPArifyException(Exception):
    def __init__(self, status_code: int, content: dict):
        self.status_code = status_code
        self.content = content
        super().__init__()