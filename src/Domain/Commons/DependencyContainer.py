from typing import Any
from typing import Callable
from typing import Union
from typing import Type
from functools import wraps

class _dependencyContainer:
    __instance = None
    __dependencies = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def register(cls, interface: Type, implementation: Union[Type, Callable[[], Any]]) -> None:
        """Registra una implementación para una interfaz dada."""
        cls.__dependencies[interface] = implementation 

    @classmethod
    def resolve(cls, interface: Type):
        """Resuelve una implementación para una interfaz dada."""
        return cls.__dependencies.get(interface)

# def register_dependency(interface: Type, implementation: Type):    
#     """Función para registrar una implementación como una dependencia."""
#     _dependencyContainer.register(interface, implementation)

# def get_dependency(interface: Type):
#     """Obtiene la implementación de una interfaz dada."""
#     implementation = _dependencyContainer.resolve(interface)
#     if implementation:
#         return implementation()
#     else:
#         raise Exception(f"No se encontró implementación para la interfaz {interface}")
