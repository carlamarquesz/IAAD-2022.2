import streamlit as st
from bd import *

st.set_page_config(layout="wide")
st.title("Consultas")

def execute_query(query, args=None):
    try:
        cursor = connection.cursor()

        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)

        results = cursor.fetchall()

        connection.commit()
        return results
    except Exception as e:
        st.error(f"Erro na consulta: {str(e)}")


# Título do aplicativo Streamlit
st.title("Consultas Relacionais em MySQL")

# Widget de seleção do tipo de consulta
consulta = st.selectbox("Selecione o tipo de consulta:", ["Funcionários por Departamento", 
                                                          "Dependentes por Funcionário", 
                                                          'Funcionários por departamento por dependente'])

if consulta == "Funcionários por Departamento":
    # Consulta SQL: Funcionários por Departamento
    query = """
        SELECT F.Pnome, F.Unome, D.Dnome
        FROM FUNCIONARIO F
        JOIN DEPARTAMENTO D ON F.Dnr = D.Dnumero;
    """

elif consulta == "Dependentes por Funcionário":
    # Consulta SQL: Dependentes por Funcionário
    query = """
        SELECT F.Pnome, F.Unome, DD.Nome_dependente
        FROM FUNCIONARIO F
        LEFT JOIN DEPENDENTE DD ON F.Cpf = DD.Fcpf;
    """

elif consulta == 'Funcionários por departamento por dependente':
    query = """
    SELECT F.Pnome, F.Unome, D.Dnome, DD.Nome_dependente
    FROM FUNCIONARIO F
    JOIN DEPARTAMENTO D ON F.Dnr = D.Dnumero
    LEFT JOIN DEPENDENTE DD ON F.Cpf = DD.Fcpf;
"""


# Executar a consulta SQL
results = execute_query(query)

# Exibir os resultados em uma tabela
st.table(results)