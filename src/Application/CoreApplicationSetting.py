from Infrastructure.ExampleFakeApiInfra.ExampleFakeApiSetting import ExampleFakeApiSetting
from Infrastructure.HttpClientHelper.HttpClientSetting import HttpClientSetting
# from Infrastructure.KafkaProducerInfrastructure.KafkaProducerSetting import KafkaProducerSetting

# ********************************************************************************************************          
# * Copyright © 2025 Arify Labs - All rights reserved.   
# * 
# * Info                  : Dependency injection Handler.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991*14
# *
# * Creation date         : 20/10/2025
# * 
# **********************************************************************************************************

class CoreApplicationSetting:
    def __init__(self) -> None:
        self.__add_infrastructure()

    def __add_infrastructure(self) -> None:
        HttpClientSetting.add_services()
        ExampleFakeApiSetting.add_services()
        # KafkaProducerSetting.add_services()
    
    # ********************************************************************************************************          
    # * Please not use or added sigleton instance in this layer, only in the infrastructure layer.
    # ********************************************************************************************************          
