from pydantic import BaseModel, EmailStr, validator
from bcrypt import hashpw, gensalt, checkpw
from typing import Union

class UserCliente(BaseModel):
    username        : str
    userpassword    : str
    cpf             : str
    cnpj            : Union[str, None]
    email           : EmailStr
    phone           : str

    @validator("cpf")
    def validate_cpf(cls, value) -> str:
        '''Valida se o cpf do usuario corrensponde aos requisitos'''
        if not value.isdigit() or len(value) != 11:
            raise ValueError("CPF deve conter 11 dígitos numéricos")
        return value

    @validator("userpassword")
    def validate_password(cls, value) -> str:
        '''Valida se a senha do usuario corrensponde aos requisitos'''
        if len(value) < 6:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        return hashpw(value.encode(), gensalt()).decode()

    def check_password(self, password: str) -> bool:
        '''Verifica se a senha do usuario esta correta'''
        return checkpw(password.encode(), self.userpassword.encode())
