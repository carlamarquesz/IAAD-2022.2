from bd import *
import streamlit as st
import pandas as pd
 
st.set_page_config(layout="wide") 
def exibir_registros(cursor, tabela): 
    st.header(f"Tabela: {tabela}")
    registros = leitura(cursor, tabela)
    if registros:
        colunas = nomes_tabelas(tabela)
        df = pd.DataFrame(registros, columns=colunas)
        st.table(df)
    st.write(f"Total de registros: {len(registros)}")

def main():
    st.title("Aplicativo com Streamlit e MySQL")
    st.sidebar.header("Tabelas") 
    tabelas = todas_tabelas(cursor) 
    menu = st.sidebar.radio("Opções:", tabelas) 

    if menu is not None:
        exibir_registros(cursor, menu) 

if __name__ == "__main__":
    main()