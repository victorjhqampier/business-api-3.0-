class AuthServerContainer:
    __instance = None
    __dependencies = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AuthServerContainer, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def register(cls, name: str, implementation: dict):
        cls.__dependencies[name] = implementation

    @classmethod
    def resolve(cls, name: str):
        return cls.__dependencies.get(name)

    @classmethod
    def update(cls, name: str, implementation: dict):
        if name in cls.__dependencies:
            cls.__dependencies[name] = implementation
        else:
            raise KeyError(f"No se encontró la variable {name} para actualizar.")

def register_vars(name: str, implementation: dict) -> None:
    AuthServerContainer.register(name, implementation)

def get_vars(name: str) -> dict:
    implementation = AuthServerContainer.resolve(name)
    if implementation is not None:
        return implementation
    else:
        raise KeyError(f"No se encontró variable para {name}")

def update_vars(name: str, implementation: dict) -> None:
    AuthServerContainer.update(name, implementation)
