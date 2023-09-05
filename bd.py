import mysql.connector
import streamlit as st
import pandas as pd

connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='saltitao1',
        database='empresa_adaptado'
    )
cursor = connection.cursor()

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

def deletar_registro(tabela, chave_primaria, valor_chave):
    consulta_deletar = f"DELETE FROM {tabela} WHERE {chave_primaria} = '{valor_chave}'"
    conn = connection
    cursor = conn.cursor()
    
    try:
        cursor.execute(consulta_deletar)
        conn.commit()
        st.success(f"Registro com {chave_primaria} igual a '{valor_chave}' deletado com sucesso.")
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar registro: {err}")
        
def inserir_dados(tabela, campos):
    campos_formatados = ", ".join([f"'{valor}'" for valor in campos.values()])
    consulta_inserir = f"INSERT INTO {tabela} ({', '.join(campos.keys())}) VALUES ({campos_formatados})"
    executar_consulta_(consulta_inserir)

def deletar_linha_em_cascata(tabela, chave_primaria, valor_chave):
    consulta_deletar = f"DELETE FROM {tabela} WHERE {chave_primaria} = '{valor_chave}'"
    executar_consulta_(consulta_deletar)
    
def deletar_tabela(tabela):
    consulta_deletar = f"DROP TABLE IF EXISTS {tabela}"
    executar_consulta(consulta_deletar)