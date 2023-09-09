import streamlit as st
from bd import *
import pandas as pd

st.set_page_config(layout="wide")

# Interface da aplicação Streamlit
def main():
    st.title("Consulta Relacional Interativa")

    st.subheader("Selecionar Tabelas e Colunas")
    st.write("consultas feitas aqui deverão envolver pelo menos duas tabelas, para consultas envolvendo somente uma tabela, utilizar o select do CRUD")
    tabelas = st.multiselect("Selecione as tabelas", ["funcionario", "departamento", "dependente"])
    colunas = st.multiselect("Selecione as colunas", ["*"] + ["Pnome", "Minicial", "Unome", "Cpf", 
                                                              "Datanasc", "Endereco", "Sexo",
                                                              "Salario","Cpf_supervisor","Dnr",
                                                              "Fcpf","Nome_dependente","Datanasc","Parentesco",
                                                              "Dnome", "Dnumero", "Cpf_gerente", "Data_inicio_gerente"])

    if st.button("Executar Consulta"):
        consulta_sql = criar_consulta_relacional(tabelas, colunas)
        resultados = executar_consulta(consulta_sql)

        if not resultados.empty:  # Verifica se o DataFrame não está vazio
            st.write("Resultados da Consulta:")
            st.dataframe(resultados)
        else:
            st.write("Nenhum resultado encontrado.")

if __name__ == "__main__":
    main()