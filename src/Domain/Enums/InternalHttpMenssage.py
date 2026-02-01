from enum import Enum
class InternalHttpMenssage(str, Enum):
    Success:str = 'La petición se completó exitosamente'    
    SuccessEmpty:str = 'La solicitud se completó exitosamente, pero su respuesta no tiene ningún contenido'
    InternalError:str = 'La solicitud no pudo ser procesada debido a un problema interno'
    RequestError:str = 'La petición no pudo completarse debido a que la solicitud no fue válida'