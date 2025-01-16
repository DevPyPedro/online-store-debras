from unidecode import unidecode #type: ignore
import re

from src.infra.models.types_queries import *

# Definindo uma regex para caracteres inválidos
regex = r"""[^A-Za-z0-9, "'.();:_=*<>!-]"""

def sanitize_query(query: str) -> str:
    """Remove caracteres indesejados e normaliza o espaço."""
    return (
        re.sub(regex, "", unidecode(query))
        .strip()
        .replace("   ", "")
        .replace("  ", " ")
    )

def create_table(params: CreateTableParams) -> List[str]:
    """Cria uma query para a criação de tabela."""
    table_name = f'"{params["Nome"].upper()}"'
    columns = ",\n   ".join([f'"{col["Nome"].upper()}" {col["Type"]}' for col in params["Columns"]])
    query = f"""CREATE TABLE IF NOT EXISTS {table_name}(\n   {columns}\n);"""
    return [sanitize_query(query)]

def insert_values(values: InsertValuesParams, table_template: CreateTableParams, returning=None) -> List[str]:
    """Cria uma query para inserir valores na tabela."""
    columns = {col["Nome"]: col["Type"] for col in table_template["Columns"]}
    querys_put = []

    for value in values:
        str_columns, str_values = [], []
        for key, val in value.items():
            if key not in columns:
                continue

            col = key.upper()
            type_ = columns[key]

            if val is None:
                val = "NULL"
            elif "TEXT" in type_ or "VARCHAR" in type_:
                val = f"'{str(val)}'"
            elif "REAL" in type_:
                val = f"{float(val)}"
            elif "INTEGER" in type_:
                val = f"{int(val)}"

            str_columns.append(f'"{col}"')
            str_values.append(f"{val}")

        if str_columns and str_values:
            query = f"""INSERT INTO "{table_template['Nome']}" ({", ".join(str_columns)}) VALUES ({", ".join(str_values)})"""
            if returning:
                query += f' RETURNING "{returning}";'
            else:
                query += ";"
            querys_put.append(sanitize_query(query))

    return querys_put

def update_values(values: UpdateValuesParams, table_template: CreateTableParams) -> List[str]:
    """Cria uma query para atualizar valores na tabela."""
    column_types = {col["Nome"]: col["Type"] for col in table_template["Columns"]}
    querys_put = []

    for value in values:
        sets = []
        wheres = []
        for key, val in value.items():
            if key in column_types:
                col = key.upper()
                type_ = column_types[key]
                if val is None:
                    val = "NULL"
                elif "TEXT" in type_ or "VARCHAR" in type_:
                    val = f"'{str(val)}'"
                elif "REAL" in type_:
                    val = f"{float(val)}"
                elif "INTEGER" in type_:
                    val = f"{int(val)}"
                sets.append(f'"{col}" = {val}')

        for key in table_template["PrimaryKey"]:
            key_val = value[key]
            key_type = column_types[key]
            key = key.upper()
            if key_val is None:
                key_val = "NULL"
            elif "TEXT" in key_type or "VARCHAR" in key_type:
                key_val = f"'{str(key_val)}'"
            elif "REAL" in key_type:
                key_val = f"{float(key_val)}"
            elif "INTEGER" in key_type:
                key_val = f"{int(key_val)}"
            wheres.append(f'"{key}" = {key_val}')

        query = f'UPDATE "{table_template["Nome"]}" SET {", ".join(sets)} WHERE {" AND ".join(wheres)};'
        querys_put.append(sanitize_query(query))
    return querys_put

def select_values(values: SelectValues, table_template: SelectParams, limit: int =None) -> List[str]:
    """Cria uma query para selecionar valores da tabela."""
    columns = ", ".join(table_template["Columns"])
    query = f'SELECT {columns} FROM "{table_template["Nome"]}"'
    
    if "Join" in table_template:
        for join in table_template["Join"]:
            query += f' {join["Tipo"]} JOIN {join["Tabela"]} ON {join["Condicao"]}'

    if "Where" in table_template:
        where_clauses = []
        for info in table_template["Where"]:
            col = info["Nome"]
            type_ = info["Type"]
            operator = info.get("Operator", "=")
            value = values.get(col)
            if value is not None:
                if "TEXT" in type_ or "VARCHAR" in type_:
                    value = f"'{str(value)}'"
                elif "REAL" in type_:
                    value = f"{float(value)}"
                elif "INTEGER" in type_:
                    value = f"{int(value)}"
                if operator == "BETWEEN":
                    value_re = re.sub(r"""[^0-9,_]""", "", value)
                    start_date, end_date = value_re.split(",")
                    where_clauses.append(f'"{col}" BETWEEN \'{start_date}\' AND \'{end_date}\'')
                else:
                    where_clauses.append(f'"{col}" {operator} {value}')
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

    if "Order" in table_template:
        order_clauses = []
        
        for order in table_template["Order"]:
            order_clauses.append(f'"{order["Coluna"]}" {order["Ordem"]}')
        
        if order_clauses:
            query += " ORDER BY " + ", ".join(order_clauses)
        
    if limit:
        query += f' LIMIT {limit}'

    return [sanitize_query(query)]

def delete_values(values: DeleteValuesParams, table_template: SelectParams) -> List[str]:
    """Cria uma query para deletar valores da tabela."""
    querys_put = []
    for value in values:
        query = f'DELETE FROM "{table_template["Nome"]}"'
        if "Where" in table_template:
            where_clauses = []
            for info in table_template["Where"]:
                col = info["Nome"]
                type_ = info["Type"]
                operator = info.get("Operator", "=")
                val = value.get(col)
                if val is not None:
                    if "TEXT" in type_ or "VARCHAR" in type_:
                        val = f"'{str(val)}'"
                    elif "REAL" in type_:
                        val = f"{float(val)}"
                    elif "INTEGER" in type_:
                        val = f"{int(val)}"
                    if operator == "BETWEEN":
                        start_date, end_date = val.split(",")
                        where_clauses.append(f'"{col}" BETWEEN {start_date} AND {end_date}')
                    else:
                        where_clauses.append(f'"{col}" {operator} {val}')
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
        querys_put.append(sanitize_query(query))

    return querys_put
