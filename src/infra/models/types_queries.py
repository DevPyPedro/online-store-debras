from typing import TypedDict, List

class SelectValues(TypedDict):
    Values: List[dict]

class DeleteValuesParams(TypedDict):
    Values: List[dict]
    
class InsertValuesParams(TypedDict):
    Values: List[dict]

class UpdateValuesParams(TypedDict):
    Values: List[dict]
    
class CreateTableParams(TypedDict):
    Nome: str
    PrimaryKey: str
    Columns: List[dict]
    
class SelectParams(TypedDict):
    Nome: str
    Columns: List[str]
    Where: List[dict]
    Join: List[dict]
    Order: List[str]
    
class DeleteParams(TypedDict):
    Nome: str
    Columns: List[str]
    Where: List[dict]