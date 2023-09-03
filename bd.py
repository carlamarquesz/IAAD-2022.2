import mysql.connector
import streamlit as st
connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='saltitao1',
        database='empresa_iaad'
    )
cursor = connection.cursor()

def insert(table, values, columns): 
    placeholders = ', '.join(['%s'] * len(values)) 
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})" 
    cursor.execute(query, values) 
    st.success(f"Os dados foram inseridos com sucesso na tabela {table}!")
    connection.commit()

# def update(table, values, columns, id): 
#     query = f"UPDATE {table} SET {', '.join(map(lambda col: f'{col} = %s', columns))} WHERE id = {id}"
#     cursor.execute(query, values)
#     st.success(f"Os dados foram atualizados com sucesso na tabela {table}!")
#     connection.commit()

# def delete(table, id):
#     query = f"DELETE FROM {table} WHERE id = {id}"
#     cursor.execute(query)
#     st.success(f"Os dados foram deletados com sucesso na tabela {table}!")
#     connection.commit()



################################## Antony

def inserir_dados(cursor, tabela, **kwargs):
    # Montar a consulta SQL dinamicamente
    campos = ', '.join(kwargs.keys())
    valores = ', '.join(['%s' for _ in kwargs])
    consulta = f'INSERT INTO {tabela} ({campos}) VALUES ({valores})'

    cursor.execute(consulta, tuple(kwargs.values()))
    connection.commit()

# ler
def leitura(cursor, tabela):
    ler_tabela = tabela
    comando_ler = f'SELECT * FROM {ler_tabela};'
    cursor.execute(comando_ler)
    resultado = cursor.fetchall()
    return resultado
   
def nomes_tabelas(tabela):
    cursor = connection.cursor()
    table_name = tabela
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    results = cursor.fetchall()
    return [tabela[0] for tabela in results]


def todas_tabelas(cursor):
    consulta_sql = "SHOW TABLES"
    cursor.execute(consulta_sql)
    tabelas = cursor.fetchall()
    return [row[0] for row in tabelas]
