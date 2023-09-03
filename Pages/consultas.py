import streamlit as st
from bd import *
import pandas as pd

st.set_page_config(layout="wide")

# Função para executar consultas SQL e retornar os resultados
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

# Função para criar a consulta SQL com base nas tabelas e colunas selecionadas
def criar_consulta(tabelas, colunas):
    consulta = "SELECT "
    consulta += ", ".join(colunas)
    consulta += " FROM "
    consulta += ", ".join(tabelas)
    consulta += ";"

    return consulta

# Interface da aplicação Streamlit
def main():
    st.title("Consulta Relacional Interativa")

    st.subheader("Selecionar Tabelas e Colunas")
    tabelas = st.multiselect("Selecione as tabelas", ["funcionario", "departamento", "dependente"])
    colunas = st.multiselect("Selecione as colunas", ["*"] + ["Pnome", "Minicial", "Unome", "Cpf", 
                                                              "Datanasc", "Endereco", "Sexo",
                                                              "Salario","Cpf_supervisor","Dnr",
                                                              "Fcpf","Nome_dependente","Datanasc","Parentesco",
                                                              "Dnome", "Dnumero", "Cpf_gerente", "Data_inicio_gerente"])

    if st.button("Executar Consulta"):
        consulta_sql = criar_consulta(tabelas, colunas)
        resultados = executar_consulta(consulta_sql)

        if not resultados.empty:  # Verifica se o DataFrame não está vazio
            st.write("Resultados da Consulta:")
            st.dataframe(resultados)
        else:
            st.write("Nenhum resultado encontrado.")

if __name__ == "__main__":
    main()