import streamlit as st
from bd import *

st.set_page_config(layout="wide")
st.title("Operações de CRUD")

aba1, aba2, aba3, aba4 = st.tabs(["Insert", "Select", "Update", "Delete"])

inputs = {
    'FUNCIONARIO': ['Pnome', 'Minicial', 'Unome', 'Cpf', 'Datanasc', 'Endereco', 'Sexo', 'Salario', 'Cpf_supervisor', 'Dnr'],
    'DEPARTAMENTO': ['Dnome', 'Dnumero', 'Cpf_gerente', 'Data_inicio_gerente'],
    'DEPENDENTE': ['Fcpf', 'Nome_dependente', 'Sexo', 'Datanasc', 'Parentesco'],
    'PROJETO': ['Projnome', 'Projnumero', 'Projlocal', 'Dnum'],
    'TRABALHA_EM': ['Fcpf', 'Pnr', 'Horas'],
    'LOCALIZACAO_DEP': ['Dnumero', 'Dlocal']
}

def forms(inputs, operation_crud):
    key = operation_crud
    result = []
    form_fields = []

    for input_label in inputs:
        label_input = st.text_input(f'{input_label}:', key=f'{input_label}_{key}')
        form_fields.append(input_label)
        result.append(label_input)

    btn = st.button(f'{key}')
    if btn:
        return result, form_fields
    else:
        return [], form_fields  
def main():
    st.sidebar.header("Tabelas")
    tabelas = view_tables(cursor) 
    control_panel = st.sidebar.radio("Opções:", tabelas)

    with aba1:
        st.header(f"Inserir dados em {control_panel}")
        if control_panel:
            insert_values, insert_field = forms(inputs.get(control_panel, []), 'Inserir')
            if insert_values:
                insert_operation(control_panel, insert_values, insert_field)

    with aba3:
        menu_input = inputs.get(control_panel)
        
        if menu_input:
            st.header(f"Atualize os dados em {control_panel}")

            old_values = [st.text_input(f'{old_field} Antigo ({old_field}):') for old_field in menu_input]
            st.header('Atualizar dados')
            new_values = [st.text_input(f'Novo {new_field} ({new_field}):') for new_field in menu_input]

            if st.button('Atualizar Registro'):
                if all(old_values) and all(new_values):
                    update_operation(control_panel, menu_input, old_values, new_values)
                else:
                    st.warning('Por favor, preencha todos os campos corretamente para atualizar.')

        else:
            st.warning(f"Menu '{control_panel}' não encontrado nas opções de menu disponíveis.")

    with aba4:
        st.header(f"Delete dados em {control_panel}")
        if control_panel:
            delete_values, delete_field = forms(inputs.get(control_panel, []), 'Delete')
            if delete_values:
                delete_operation(control_panel, delete_values, delete_field)

if __name__ == "__main__":
    main()