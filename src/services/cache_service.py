from src.infra.config import configCache
from typing import Any, Optional, Union
import redis
import json

from src.infra.db.interfaces.cache_repository_interface import ICacheRepository

class RedisCache(ICacheRepository):
    def __init__(self, dbc: int, host=configCache['host'], port=configCache['port'], password=configCache['password']):
        self.client = redis.Redis(host=host, port=port, password=password, db=dbc, decode_responses=True)
        
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        return self.client.set(key, value, ex=ttl)
        
    def get(self, key: str) ->Union[str, dict]:
        return self.client.get(key)
    
    def delete(self, key: str) -> None:
        self.client.delete(key)
        
    def hset(self, id_session: str, key_values: dict) -> bool:
        serialized_key_values = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in key_values.items()
        }
        return self.client.hset(
            id_session,
            mapping=serialized_key_values
        )
        
    def hgetall(self, id_session: str) -> bool:
        return self.client.hgetall(id_session)  
     
    
    def expire(self, id_session: str, timeout: int)-> None:
        return self.client.expire(id_session, timeout)