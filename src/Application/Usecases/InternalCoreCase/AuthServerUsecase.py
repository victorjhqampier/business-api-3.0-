from typing import Any
import base64
from datetime import datetime, timedelta
from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Commons.AuthServerContainer import get_vars, update_vars
from Domain.Entities.HttpResponseEntity import HttpResponseEntity
from Domain.Interfaces.IAuthServerInfrastructure import IAuthServerInfrastructure
from Domain.Messages.InternalCoreMessage import InternalCoreMessage

# ********************************************************************************************************          
# * Copyright © 2025 Arify Labs - All rights reserved.   
# * 
# * Info                  : Build a http request Handler.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991*14
# *
# * Creation date         : 20/10/2024
# * 
# **********************************************************************************************************

class AuthServerUsecase:
    def __init__(self) -> None:
        self.__auth_server:dict = get_vars(InternalCoreMessage.COGNITO_NAME_APPCLIENTE_SYSTEM.value)
        self.__infra:IAuthServerInfrastructure = Services.get_dependency(IAuthServerInfrastructure)
    
    async def get_cognito_token(self)->str:
        # Si el token ya expiró
        
        expire_date:datetime   = datetime.fromisoformat(self.__auth_server["expire"])
        if expire_date <= datetime.now():
            
            credentials:str = f"{self.__auth_server['user']}:{self.__auth_server['passwd']}"
            credentials_bytes: bytes = credentials.encode('utf-8')  # Convertimos la cadena a bytes
            encoded_credentials: str = base64.b64encode(credentials_bytes).decode('utf-8')
            param: dict[str, str] = {
                "grant_type": "client_credentials",
                "scope": self.__auth_server['scope']
            }
            header: dict[str, str] = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + encoded_credentials
            }
            
            result:HttpResponseEntity = await self.__infra.post_async(self.__auth_server["host"], data=None, params=param, headers=header)
            
            if result.Content is not None and result.StatusCode == 200:
                self.__auth_server.update({
                    "token": result.Content["access_token"],
                    "expire": (datetime.now() + timedelta(seconds=result.Content["expires_in"]) - timedelta(minutes=2)).isoformat()
                })

                update_vars(InternalCoreMessage.COGNITO_NAME_APPCLIENTE_SYSTEM.value, self.__auth_server)
                return result.Content["access_token"]
        
        return self.__auth_server["token"]

