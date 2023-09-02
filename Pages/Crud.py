import streamlit as st
import pandas as pd
from bd import *

st.set_page_config(layout="wide")
st.title("Operações de CRUD")
aba1, aba2, aba3, ada4= st.tabs(["Insert", "Select", "Update", "Delete"])

inputs_funcionario = ['Pnome', 'Minicial', 'Unome', 'Cpf', 'Datanasc', 'Endereco', 'Sexo', 'Salario', 'Cpf_supervisor', 'Dnr']
inputs_departamento = ['Dnome', 'Dnumero', 'Cpf_gerente','Data_inicio_gerente']
inputs_dependente = ['Fcpf', 'Nome_dependente', 'Sexo', 'Datanasc', 'Parentesco']
inputs_projeto = ['Projnome', 'Projnumero', 'Projlocal', 'Dnum']
inputs_trabalha_em = ['Fcpf', 'Pnr', 'Horas']
inputs_localizacao_dep = ['Dnumero', 'Dlocal'] 
 
def fomulario(inputs): 
    resultado = []
    campos = []

    todos_campos_preenchidos = True   
    for input_label in inputs:
        label_input = st.text_input(f'{input_label}:', key=input_label)
        campos.append(input_label)
        if not label_input: 
            todos_campos_preenchidos = False  
        else:
            resultado.append(label_input)

    btn = st.button("Inserir")
    if btn: 
        if todos_campos_preenchidos:
            return resultado, campos
        else:
            st.warning("Por favor, preencha todos os campos corretamente para prosseguir.")

def main():
    st.sidebar.header("Tabelas") 
    tabelas = todas_tabelas(cursor) 
    menu = st.sidebar.radio("Opções:", tabelas)  
    with aba1:  
        st.header(f"Inserir dados em {menu}")  
        if menu == 'funcionario':
            resultado = fomulario(inputs_funcionario)
        elif menu == 'departamento':
            resultado = fomulario(inputs_departamento)
        elif menu == 'dependente':
            resultado = fomulario(inputs_dependente)
        elif menu == 'projeto':
            resultado = fomulario(inputs_projeto)
        elif menu == 'trabalha_em':
            resultado = fomulario(inputs_trabalha_em)
        elif menu == 'localizacao_dep':
            resultado = fomulario(inputs_localizacao_dep)
        if resultado is not None:
            valores, campos = resultado
            insert(menu, valores, campos)

if __name__ == "__main__":
    main()