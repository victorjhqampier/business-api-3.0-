from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Interfaces.IHttpClientInfrastructure import IHttpClientInfrastructure
from Infrastructure.HttpClientHelper.HttpClientConnector import HttpClientConnector
from Infrastructure.HttpClientHelper.HttpClientInfrastructure import HttpClientInfrastructure

# ********************************************************************************************************          
# * Copyright © 2025 Arify Labs - All rights reserved.   
# * 
# * Info                  : HttpClientSetting injection Handler.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 20/10/2024
# * 
# **********************************************************************************************************

class HttpClientSetting:

    @classmethod
    def add_services(self) -> None:
        Services.add_singleton_dependency(IHttpClientInfrastructure, HttpClientInfrastructure)

        # Added instance on singleton
        Services.add_singleton_instance(HttpClientConnector(timeout_sec=15))