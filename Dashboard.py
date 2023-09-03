from bd import *
import streamlit as st
import pandas as pd
 
st.set_page_config(layout="wide") 

def show_record(cursor, tabela): 
    st.header(f"Tabela: {tabela}")
    registros = read_operation(cursor, tabela)
    if registros:
        columns = table_names(tabela)
        df = pd.DataFrame(registros, columns=columns)
        st.table(df)
    st.write(f"Total de registros: {len(registros)}")

def main():
    st.title("Aplicativo com Streamlit e MySQL")
    st.sidebar.header("Tabelas") 
    tables = view_tables(cursor) 
    menu = st.sidebar.radio("Opções:", tables) 

    if menu is not None:
        show_record(cursor, menu) 

if __name__ == "__main__":
    main()