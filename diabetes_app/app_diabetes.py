# app_diabetes.py
import streamlit as st
import pandas as pd
import joblib  # Para carregar o modelo

#  Carregar o modelo treinado
import os

# Caminho absoluto relativo ao script
caminho_modelo = os.path.join(os.path.dirname(__file__), "modelo_diabetes.pkl")
modelo = joblib.load(caminho_modelo)


# Função para calcular risco
def calcular_risco(imc, pressao_alta, colesterol_alto, fumante, atividade_fisica,
                   alcool_excessivo, frutas, vegetais):
    estilo_risco = int(fumante==1 or alcool_excessivo==1)
    alimentacao_saudavel = int(frutas==1 and vegetais==1)
    
    pessoa = pd.DataFrame({
        "imc_tratado":[imc],
        "pressao_alta":[pressao_alta],
        "colesterol_alto":[colesterol_alto],
        "fumante":[fumante],
        "atividade_fisica":[atividade_fisica],
        "alcool_excessivo":[alcool_excessivo],
        "frutas":[frutas],
        "vegetais":[vegetais],
        "estilo_vida_risco":[estilo_risco],
        "alimentacao_saudavel":[alimentacao_saudavel]
    })
    prob = modelo.predict_proba(pessoa)[0][1]*100
    return prob

# Interface do Streamlit
st.title("Previsão de Diabetes")
st.header("Informe seus dados:")

imc = st.number_input("Digite seu IMC", min_value=10.0, max_value=60.0, value=25.0)
pressao_alta = st.selectbox("Você tem pressão alta?", ["Não", "Sim"])
colesterol_alto = st.selectbox("Você tem colesterol alto?", ["Não", "Sim"])
fumante = st.selectbox("Você é fumante?", ["Não", "Sim"])
atividade_fisica = st.selectbox("Você pratica atividade física regularmente?", ["Não", "Sim"])
alcool_excessivo = st.selectbox("Você consome álcool em excesso?", ["Não", "Sim"])
frutas = st.selectbox("Você consome frutas regularmente?", ["Não", "Sim"])
vegetais = st.selectbox("Você consome vegetais regularmente?", ["Não", "Sim"])

# Converter respostas para 0 ou 1
pressao_alta = 1 if pressao_alta=="Sim" else 0
colesterol_alto = 1 if colesterol_alto=="Sim" else 0
fumante = 1 if fumante=="Sim" else 0
atividade_fisica = 1 if atividade_fisica=="Sim" else 0
alcool_excessivo = 1 if alcool_excessivo=="Sim" else 0
frutas = 1 if frutas=="Sim" else 0
vegetais = 1 if vegetais=="Sim" else 0

if st.button("Calcular risco"):
    risco = calcular_risco(imc, pressao_alta, colesterol_alto, fumante,
                           atividade_fisica, alcool_excessivo, frutas, vegetais)
    st.success(f"🔹 Risco estimado de diabetes: {risco:.2f}%")
