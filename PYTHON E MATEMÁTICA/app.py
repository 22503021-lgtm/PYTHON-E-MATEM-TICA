import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="PYTHON E MATEMÁTICA", layout="wide", page_icon = "📐", initial_sidebar_state="expanded")

caminho_ou_arquivo = r"Tabela_13_Meio_de_transporte.xlsx"

st.title("Indicador_5: Transporte e Mobilidade Urbana (Tabela 13)")

st.write("______________________________________________________")
st.header("Dashboard Indicador 5")


st.sidebar.title("📌 Menu & Filtros")

st.sidebar.subheader("📂 Arquivos de Entrada (Pandas)")

file_afazeres = st.sidebar.file_uploader("Upload Tabela_13_Meio_de_transporte):", type=["xls", "xlsx", "csv"])

caminho_ou_arquivo = r"Tabela_13_Meio_de_transporte.xlsx"

@st.cache_data
def carregar_e_limpar_afazeres(caminho_ou_arquivo):
    if isinstance(caminho_ou_arquivo, str):
        if caminho_ou_arquivo.lower().endswith(".csv"):
            bruto = pd.read_csv(caminho_ou_arquivo, header=None)
        else:
            bruto = pd.read_excel(caminho_ou_arquivo, engine="xlrd", header=None)
    else:
        nome = caminho_ou_arquivo.name.lower()
        if nome.endswith(".csv"):
            bruto = pd.read_csv(caminho_ou_arquivo, header=None)
        elif nome.endswith(".xls"):
            bruto = pd.read_excel(caminho_ou_arquivo, engine="xlrd", header=None)
        else:
            bruto = pd.read_excel(caminho_ou_arquivo, header=None)

    df = bruto.iloc[8:41].copy()

    df.columns = [
        "uf_regiao",
        "total",
        "total_branca",
        "total_preta_parda",
        "homem_branca",
        "homem_preta_parda",
        "mulher_branca",
        "mulher_preta_parda",
    ]
    df = df.reset_index(drop=True)

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["homens_media"] = ((df["homem_branca"] + df["homem_preta_parda"]) / 2).round(2)
    df["mulheres_media"] = ((df["mulher_branca"] + df["mulher_preta_parda"]) / 2).round(2)
    df["diferenca_genero"] = (df["mulheres_media"] - df["homens_media"]).round(2)

    return df

import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'Regiao': ['Suldeste', 'Nordeste', 'Sul', 'Norte', 'Centro-Oeste'],
    'Mulheres': [18.5, 19.2, 17.8, 18.0, 17.5],
    'Homens': [10.2, 11.0, 9.8, 10.5, 10.0]
}).melt(id_vars=['Regiao'], var_name='Gênero', value_name='Horas')

fig = px.bar(
    df, 
    x='Regiao', y='Horas', 
    color='Gênero',
    barmode='group',
    orientation='v',
    color_continuous_scale='Viridis',
    title="Tabela 13 - Distribuição percentual das mulheres de 10 anos ou mais de idade, ocupadas na semana de referência, por meio de transporte"
)

st.plotly_chart(fig, use_container_width=True)