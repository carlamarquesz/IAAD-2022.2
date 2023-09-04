import mysql.connector
import streamlit as st
import pandas as pd

connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='saltitao1',
        database='empresa_iaad'
    )
cursor = connection.cursor()


def insert_operation(table, values, columns):
    try:
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        st.success(f"Os dados foram inseridos com sucesso na tabela {table}!")
        connection.commit()
    except mysql.connector.Error as err:
        st.error(f"Erro ao inserir dados na tabela {table}: {err}")
        connection.rollback()  


def update_operation(tabela, campos, valores_antigos, valores_novos):
    cursor = connection.cursor()

    comando_atualizacao = f"UPDATE {tabela} SET "
    atualizacoes = [f"{campo} = %s" for campo in campos]
    comando_atualizacao += ', '.join(atualizacoes)
    comando_atualizacao += " WHERE "
    condicoes = [f"{campo} = %s" for campo in campos]
    comando_atualizacao += ' AND '.join(condicoes)
    
    try:
        cursor.execute(comando_atualizacao, valores_novos + valores_antigos)
        connection.commit()
        num_linhas_afetadas = cursor.rowcount
        st.success(f"{num_linhas_afetadas} registro(s) atualizado(s) com sucesso.")

    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar registro: {err}")
        connection.rollback()


def delete_operation(tabela, dados, campos):
    if dados is not None:
        delete_query = f"DELETE FROM {tabela} WHERE "
        for campo, valor in zip(campos, dados):
            delete_query += f"{campo} = '{valor}' AND "
        
        delete_query = delete_query[:-5]  # Remove o "AND" final
        cursor.execute(delete_query)
        st.success(f"Os dados foram excluídos com sucesso: {delete_query}")
        connection.commit()


# ler
def read_operation(cursor, tabela):
    ler_tabela = tabela
    comando_ler = f'SELECT * FROM {ler_tabela};'
    cursor.execute(comando_ler)
    resultado = cursor.fetchall()
    return resultado
   
def table_names(tabela):
    cursor = connection.cursor()
    table_name = tabela
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    results = cursor.fetchall()
    return [tabela[0] for tabela in results]


def view_tables(cursor):
    consulta_sql = "SHOW TABLES"
    cursor.execute(consulta_sql)
    tabelas = cursor.fetchall()
    return [row[0] for row in tabelas]


def executar_consulta(consulta):
    conn = connection
    cursor = conn.cursor()

    cursor.execute(consulta)

    resultados = cursor.fetchall()
    colunas = [i[0] for i in cursor.description]

    if resultados:
        df = pd.DataFrame(resultados, columns=colunas)
        return df
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio quando não há resultados

def criar_consulta_relacional(tabelas, colunas):
    consulta = "SELECT "
    consulta += ", ".join(colunas)
    consulta += " FROM "
    consulta += ", ".join(tabelas)
    consulta += ";"

    return consulta

def criar_consulta(tabela, colunas):
    consulta = "SELECT "
    consulta += ", ".join(colunas)
    consulta += " FROM " + tabela

    return consulta

def executar_consulta_(consulta):
    conn = connection
    cursor = conn.cursor()

    cursor.execute(consulta)

    conn.commit()

    cursor.close()
    conn.close()