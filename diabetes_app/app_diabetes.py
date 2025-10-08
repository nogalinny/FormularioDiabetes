# app_diabetes.py
import streamlit as st
import pandas as pd
import joblib
import os

# ---------------------------
# Carregar o modelo
# ---------------------------
caminho_modelo = os.path.join(os.path.dirname(__file__), "modelo_diabetes.pkl")
modelo = joblib.load(caminho_modelo)

# ---------------------------
# Função para calcular risco
# ---------------------------
def calcular_risco(imc, pressao_alta, colesterol_alto, fumante, atividade_fisica,
                   alcool_excessivo, frutas, vegetais):
    estilo_risco = int(fumante == 1 or alcool_excessivo == 1)
    alimentacao_saudavel = int(frutas == 1 and vegetais == 1)
    
    pessoa = pd.DataFrame({
        "imc_tratado": [imc],
        "pressao_alta": [pressao_alta],
        "colesterol_alto": [colesterol_alto],
        "fumante": [fumante],
        "atividade_fisica": [atividade_fisica],
        "alcool_excessivo": [alcool_excessivo],
        "frutas": [frutas],
        "vegetais": [vegetais],
        "estilo_vida_risco": [estilo_risco],
        "alimentacao_saudavel": [alimentacao_saudavel]
    })
    prob = modelo.predict_proba(pessoa)[0][1] * 100
    return prob

# ---------------------------
# Configuração da página
# ---------------------------
st.set_page_config(page_title="Previsão de Diabetes", layout="centered")
st.title("🩺 Previsão de Diabetes")
st.write("Preencha os dados abaixo para calcular o risco estimado de diabetes:")

# ---------------------------
# Inicializar session_state
# ---------------------------
if "dados" not in st.session_state:
    st.session_state.dados = {
        "imc": 25.0,
        "pressao_alta": 0,
        "colesterol_alto": 0,
        "fumante": 0,
        "atividade_fisica": 0,
        "alcool_excessivo": 0,
        "frutas": 0,
        "vegetais": 0
    }

if "risco" not in st.session_state:
    st.session_state.risco = None

# ---------------------------
# Função para resetar formulário
# ---------------------------
def reset_form():
    st.session_state.dados = {
        "imc": 25.0,
        "pressao_alta": 0,
        "colesterol_alto": 0,
        "fumante": 0,
        "atividade_fisica": 0,
        "alcool_excessivo": 0,
        "frutas": 0,
        "vegetais": 0
    }
    st.session_state.risco = None

# ---------------------------
# Formulário do paciente
# ---------------------------
with st.form("formulario_paciente"):
    imc = st.number_input("Digite seu IMC", min_value=10.0, max_value=60.0,
                          value=st.session_state.dados["imc"])
    
    pressao_alta = st.selectbox("Você tem pressão alta?", ["Não", "Sim"],
                                index=st.session_state.dados["pressao_alta"])
    colesterol_alto = st.selectbox("Você tem colesterol alto?", ["Não", "Sim"],
                                   index=st.session_state.dados["colesterol_alto"])
    fumante = st.selectbox("Você é fumante?", ["Não", "Sim"],
                           index=st.session_state.dados["fumante"])
    atividade_fisica = st.selectbox("Você pratica atividade física regularmente?", ["Não", "Sim"],
                                    index=st.session_state.dados["atividade_fisica"])
    alcool_excessivo = st.selectbox("Você consome álcool em excesso?", ["Não", "Sim"],
                                    index=st.session_state.dados["alcool_excessivo"])
    frutas = st.selectbox("Você consome frutas regularmente?", ["Não", "Sim"],
                          index=st.session_state.dados["frutas"])
    vegetais = st.selectbox("Você consome vegetais regularmente?", ["Não", "Sim"],
                            index=st.session_state.dados["vegetais"])
    
    submitted = st.form_submit_button("Calcular risco")

# ---------------------------
# Processamento após submit
# ---------------------------
if submitted:
    st.session_state.dados = {
        "imc": imc,
        "pressao_alta": 1 if pressao_alta == "Sim" else 0,
        "colesterol_alto": 1 if colesterol_alto == "Sim" else 0,
        "fumante": 1 if fumante == "Sim" else 0,
        "atividade_fisica": 1 if atividade_fisica == "Sim" else 0,
        "alcool_excessivo": 1 if alcool_excessivo == "Sim" else 0,
        "frutas": 1 if frutas == "Sim" else 0,
        "vegetais": 1 if vegetais == "Sim" else 0
    }
    
    st.session_state.risco = calcular_risco(**st.session_state.dados)

# ---------------------------
# Mostrar resultado de forma visual
# ---------------------------
if st.session_state.risco is not None:
    risco = st.session_state.risco
    
    if risco < 20:
        cor = "green"
        nivel = "Baixo"
    elif risco < 50:
        cor = "orange"
        nivel = "Moderado "
    else:
        cor = "red"
        nivel = "Alto"
    
    st.markdown(f"### Risco estimado de diabetes: {risco:.2f}% ({nivel})")
    
    st.progress(int(risco))  # barra de progresso
    st.button("Novo paciente", on_click=reset_form)
