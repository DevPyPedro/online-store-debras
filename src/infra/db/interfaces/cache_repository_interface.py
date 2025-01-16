from typing import Any, Optional, Union
from abc import ABC, abstractmethod

class ICacheRepository(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        '''adiciona valores no cache no modelo key value, e adiciona um tempo de timeout'''

    @abstractmethod
    def get(self, key: str) -> Union[str, dict]:
        '''busca valores atraves da chave(key)'''

    @abstractmethod
    def delete(self, key: str) -> bool:
        '''deleta valores atraves da chave(key)'''
        
    @abstractmethod
    def hset(self, id_session: str ,key_values: str) -> bool:
        '''adciona valores no cache na forma de dicionario'''
        
    @abstractmethod
    def hgetall(self, id_session: str) -> bool:
        '''Busca valores no cache atraves do user id'''
    
    def expire(self, id_session: str, timeout: int)-> None:
        '''adcionando tempo aos valores'''