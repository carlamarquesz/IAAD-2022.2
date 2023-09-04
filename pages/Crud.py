import streamlit as st
from bd import *
import pandas as pd
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

    with aba2:
        st.title("Consultas")
        if control_panel == 'funcionario':
            control_panel = 'funcionario'
            colunas = st.multiselect("selecione as colunas",['*']+['Pnome', 
                                     'Minicial', 'Unome', 'Cpf', 'Datanasc', 
                                     'Endereco', 'Sexo', 'Salario', 'Cpf_supervisor', 'Dnr'])
        elif control_panel == 'departamento':
            control_panel = 'departamento'
            colunas = st.multiselect("Selecione as colunas",['*'] + ['Dnome', 'Dnumero', 
                                                                     'Cpf_gerente', 'Data_inicio_gerente'])
            
            
        elif control_panel == 'dependente':
            control_panel = 'dependente'
            colunas = st.multiselect("Selecione as colunas", ['*'] + ['Fcpf', 'Nome_dependente', 
                                                                      'Sexo', 'Datanasc', 'Parentesco'])
        
        if st.button("Executar Consulta"):
            consulta_sql = criar_consulta(control_panel, colunas)
            resultados = executar_consulta(consulta_sql)
            
            st.write("Resultados da Consulta:")
            st.dataframe(resultados)
        else:
            st.write("Nenhum resultado encontrado.")

    with aba3:
        st.title("atualização dos dados")
        if control_panel:
            # Consulta SQL para obter as chaves primárias da tabela selecionada
            consulta_chaves = f"SHOW KEYS FROM {control_panel} WHERE Key_name = 'PRIMARY'"
            conn = connection
            chaves_primarias = pd.read_sql(consulta_chaves, conn)
            chaves_primarias = chaves_primarias["Column_name"].tolist()

            # Barra de seleção única para escolher a chave primária
            chave_primaria_selecionada = st.selectbox("Selecione a chave primária para atualizar:", chaves_primarias)

            if chave_primaria_selecionada:

                # Consulta SQL para obter todos os valores únicos da chave primária
                consulta_valores_chave = f"SELECT DISTINCT {chave_primaria_selecionada} FROM {control_panel}"
                conn = connection
                valores_chave = pd.read_sql(consulta_valores_chave, conn)
                valores_chave = valores_chave[chave_primaria_selecionada].tolist()

                # Barra de seleção única para escolher o valor da chave primária
                valor_chave_selecionado = st.selectbox(f"Selecione o valor da chave primária para atualizar em '{control_panel}':", valores_chave)

                if valor_chave_selecionado:
                    # Consulta SQL para obter os dados do funcionário selecionado
                    consulta_dados = f"SELECT * FROM {control_panel} WHERE {chave_primaria_selecionada} = '{valor_chave_selecionado}'"
                    conn = connection
                    dados_funcionario = pd.read_sql(consulta_dados, conn)

                    if not dados_funcionario.empty:
                        st.write(f"Registro selecionado: {dados_funcionario.iloc[0]}")

                        st.subheader("Atualizar Dados")
                        # Aqui, você pode adicionar campos de entrada de texto para cada coluna que deseja atualizar
                        colunas = dados_funcionario.columns
                        colunas_atualizar = st.multiselect("Escolha as colunas para atualizar:", colunas)
                        
                        for coluna in colunas_atualizar:
                            novo_valor = st.text_input(f"Novo valor para '{coluna}':", dados_funcionario.iloc[0][coluna])
                            dados_funcionario.loc[0, coluna] = novo_valor

                        if st.button("Atualizar Dados"):
                            # Montar a consulta de atualização dinamicamente
                            consulta_atualizacao = f"UPDATE {control_panel} SET "
                            for coluna in colunas_atualizar:
                                valor_atual = dados_funcionario.iloc[0][coluna]
                                consulta_atualizacao += f"{coluna} = '{valor_atual}', "
                            consulta_atualizacao = consulta_atualizacao[:-2]  # Remover a vírgula extra no final
                            consulta_atualizacao += f" WHERE {chave_primaria_selecionada} = '{valor_chave_selecionado}'"
                            executar_consulta_(consulta_atualizacao)
                            st.success("Dados do funcionário atualizados com sucesso!")
                    else:
                        st.warning("Selecione pelo menos uma coluna para atualizar.")
                else:
                    st.warning("Registro não encontrado.")
            else:
                st.warning("Selecione um valor da chave primária.")
        else:
            st.warning("Selecione uma chave primária.")

    

    with aba4:
        st.title("Remover")
        if control_panel:

            # Consulta SQL para obter as chaves primárias da tabela selecionada
            consulta_chaves1 = f"SHOW KEYS FROM {control_panel} WHERE Key_name = 'PRIMARY'"
            conn = connection
            cursor.execute(consulta_chaves1)
            chaves_primarias1 = [row[4] for row in cursor.fetchall()]

            chave_primaria_selecionada1 = st.selectbox("Selecione a chave primária:", chaves_primarias1)

            if chave_primaria_selecionada1:
                # Consulta SQL para listar todos os valores da chave primária
                consulta_valores_chave1 = f"SELECT DISTINCT {chave_primaria_selecionada1} FROM {control_panel}"
                conn = connection
                cursor.execute(consulta_valores_chave1)
                valores_chave1 = [row[0] for row in cursor.fetchall()]

                valor_chave_selecionado1 = st.selectbox(f"Selecione o valor da chave primária para deletar em '{control_panel}':", valores_chave1)

                if valor_chave_selecionado1:
                    # Consulta SQL para obter os dados completos do registro
                    consulta_dados = f"SELECT * FROM {control_panel} WHERE {chave_primaria_selecionada1} = '{valor_chave_selecionado1}'"
                    conn = connection
                    cursor.execute(consulta_dados)
                    dados_funcionario1 = cursor.fetchall()
                    

                    if dados_funcionario1:
                        st.write(f"Registro selecionado: {dados_funcionario1[0]}")

                        colunas1 = [desc[0] for desc in cursor.description]
                        coluna_selecionada1 = st.selectbox("Selecione a coluna a ser deletada:", colunas1)

                        if st.button("Deletar Coluna"):
                            # Consulta SQL para deletar a coluna específica
                            consulta_deletar_coluna = f"UPDATE {control_panel} SET {coluna_selecionada1} = NULL WHERE {chave_primaria_selecionada1} = '{valor_chave_selecionado1}'"
                            executar_consulta_(consulta_deletar_coluna)
                            st.success(f"Coluna '{coluna_selecionada1}' deletada com sucesso do registro com {chave_primaria_selecionada1} igual a '{valor_chave_selecionado1}' em '{control_panel}'.")
                    else:
                        st.warning("Registro não encontrado.")
                else:
                    st.warning("Selecione um valor da chave primária.")
            else:
                st.warning("Selecione uma chave primária.")
        
            
if __name__ == "__main__":
    main()