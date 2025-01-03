import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dashboard de Produção", layout="wide")

# Função para carregar dados de produção
def load_production_data(file):
    df = pd.read_excel(file)
    return df

# Função para calcular métricas
def calculate_metrics(df):
    total_ordens = len(df)
    tempo_total = df['tempo_execucao'].sum()
    ordens_alta_prioridade = len(df[df['prioridade'] == 'Alta'])
    return total_ordens, tempo_total, ordens_alta_prioridade

# Interface principal
st.title("Dashboard de Controle de Produção")

# Upload das planilhas
col1, col2, col3 = st.columns(3)
with col1:
    producao_file = st.file_uploader("Planilha de Produção", type=['xlsx'])
with col2:
    previsao_file = st.file_uploader("Planilha de Previsão", type=['xlsx'])
with col3:
    entregas_file = st.file_uploader("Planilha de Entregas", type=['xlsx'])

if producao_file:
    # Carrega dados principais
    df_producao = load_production_data(producao_file)
    
    # Métricas principais
    st.header("Métricas Gerais")
    total_ordens, tempo_total, ordens_prioritarias = calculate_metrics(df_producao)
    
    # Display métricas em colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Ordens", total_ordens)
    with col2:
        st.metric("Tempo Total (horas)", f"{tempo_total:.1f}")
    with col3:
        st.metric("Ordens Prioritárias", ordens_prioritarias)
    
    # Gráficos
    st.header("Análise de Produção")
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza por prioridade
        fig_pie = px.pie(df_producao, 
                        names='prioridade', 
                        title='Distribuição por Prioridade')
        st.plotly_chart(fig_pie)
    
    with col2:
        # Gráfico de barras do tempo por ordem
        fig_bar = px.bar(df_producao, 
                        x='ordem_producao', 
                        y='tempo_execucao',
                        color='prioridade',
                        title='Tempo de Execução por Ordem')
        st.plotly_chart(fig_bar)
    
    # Tabela detalhada
    st.header("Detalhamento das Ordens")
    st.dataframe(df_producao)

    # Se tiver dados de previsão e entregas
    if previsao_file and entregas_file:
        df_previsao = pd.read_excel(previsao_file)
        df_entregas = pd.read_excel(entregas_file)
        
        st.header("Análise de Previsão vs Realizado")
        # Adicione aqui visualizações comparativas
        
else:
    st.info("Faça upload das planilhas para visualizar o dashboard completo")

# Sidebar com filtros
st.sidebar.header("Filtros")
if 'df_producao' in locals():
    prioridade_filter = st.sidebar.multiselect(
        "Filtrar por Prioridade",
        options=df_producao['prioridade'].unique()
    )
