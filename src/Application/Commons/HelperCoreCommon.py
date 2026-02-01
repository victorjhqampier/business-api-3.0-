import cryptocode
import bcrypt
import hashlib
import secrets

class HelperCoreCommon:
    def HashearCadena(self,cCadena:str) -> str:
        return bcrypt.hashpw(cCadena.encode("utf-8"), bcrypt.gensalt()).decode("utf8")
    
    def CompararHash(self,cCadena:str, cHashh:str) -> int:
        return bcrypt.checkpw(cCadena.encode("utf8"), cHashh.encode("utf8"))

    def EncriptarCadena(self, cCadena:str) -> str:
        return hashlib.sha384(cCadena.encode()).hexdigest()
        
    def CifrarCadena(self,cCadena:str, cKey:str) -> str:
        return cryptocode.encrypt(cCadena,cKey)

    def DescifrarCadena(self, cCadena:str, cKey:str) -> str:
        return cryptocode.decrypt(cCadena,cKey)
    
    def GenerateSecrests(self) -> str:
        return secrets.token_urlsafe(32)