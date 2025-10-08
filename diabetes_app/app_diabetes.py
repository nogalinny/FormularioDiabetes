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
# Interface do Streamlit
# ---------------------------
st.set_page_config(page_title="Previsão de Diabetes", layout="centered")
st.title("🔹 Previsão de Diabetes")
st.write("Preencha os dados abaixo para calcular o risco estimado de diabetes:")

# Session state para controlar múltiplos cálculos
if "calcular" not in st.session_state:
    st.session_state.calcular = False

# ---------------------------
# Formulário do paciente
# ---------------------------
with st.form("formulario_paciente"):
    imc = st.number_input("Digite seu IMC", min_value=10.0, max_value=60.0, value=25.0)
    pressao_alta = st.selectbox("Você tem pressão alta?", ["Não", "Sim"])
    colesterol_alto = st.selectbox("Você tem colesterol alto?", ["Não", "Sim"])
    fumante = st.selectbox("Você é fumante?", ["Não", "Sim"])
    atividade_fisica = st.selectbox("Você pratica atividade física regularmente?", ["Não", "Sim"])
    alcool_excessivo = st.selectbox("Você consome álcool em excesso?", ["Não", "Sim"])
    frutas = st.selectbox("Você consome frutas regularmente?", ["Não", "Sim"])
    vegetais = st.selectbox("Você consome vegetais regularmente?", ["Não", "Sim"])
    
    submitted = st.form_submit_button("Calcular risco")

# ---------------------------
# Processamento após submit
# ---------------------------
if submitted:
    # Converter respostas para 0 ou 1
    pressao_alta_val = 1 if pressao_alta == "Sim" else 0
    colesterol_alto_val = 1 if colesterol_alto == "Sim" else 0
    fumante_val = 1 if fumante == "Sim" else 0
    atividade_fisica_val = 1 if atividade_fisica == "Sim" else 0
    alcool_excessivo_val = 1 if alcool_excessivo == "Sim" else 0
    frutas_val = 1 if frutas == "Sim" else 0
    vegetais_val = 1 if vegetais == "Sim" else 0
    
    # Calcular risco
    risco = calcular_risco(imc, pressao_alta_val, colesterol_alto_val, fumante_val,
                           atividade_fisica_val, alcool_excessivo_val, frutas_val, vegetais_val)
    
    st.success(f"🔹 Risco estimado de diabetes: {risco:.2f}%")
    st.session_state.calcular = True

# ---------------------------
# Botão para novo paciente
# ---------------------------
if st.session_state.calcular:
    if st.button("Novo paciente"):
        # Resetar session_state
        st.session_state.calcular = False
        st.experimental_rerun()  # opcional, mas garante reset completo do formulário
