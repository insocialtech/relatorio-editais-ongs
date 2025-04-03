# app_streamlit.py
# Streamlit Web App para gerar relatório de editais para ONGs (apenas download, sem envio por e-mail)

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fpdf import FPDF
import os

# --- Funções de raspagem ---
def scrape_fundsforngos():
    url = "https://www2.fundsforngos.org/category/latest-funds-for-ngos/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = []
    articles = soup.select("h2.entry-title")
    for article in articles[:10]:
        title = article.text.strip()
        link = article.find("a")["href"]
        data.append({"Fonte": "FundsforNGOs", "Edital": title, "Prazo": "Não informado", "Link": link, "País": "Internacional", "Tema": "Diversos"})
    return data

def scrape_undp():
    url = "https://procurement-notices.undp.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = []
    rows = soup.select("table#noticeTable tbody tr")
    for row in rows[:10]:
        cols = row.find_all("td")
        title = cols[1].text.strip()
        deadline = cols[4].text.strip()
        link = "https://procurement-notices.undp.org/" + cols[1].find("a")["href"]
        data.append({"Fonte": "UNDP", "Edital": title, "Prazo": deadline, "Link": link, "País": "Internacional", "Tema": "Cooperação internacional"})
    return data

def coletar_oportunidades():
    return scrape_fundsforngos() + scrape_undp()

# --- Gera PDF ---
def gerar_pdf(df, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Relatório de Editais para ONGs", ln=True, align="C")
    pdf.ln(10)
    for _, row in df.iterrows():
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, row["Edital"])
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, f"Prazo: {row['Prazo']}", ln=True)
        pdf.cell(0, 6, f"Fonte: {row['Fonte']} | Tema: {row['Tema']}", ln=True)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 6, row["Link"], ln=True, link=row["Link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
    pdf.output(filename)

# --- INTERFACE ---
st.set_page_config(page_title="Relatório de Editais para ONGs", layout="centered")
st.title("📊 Gerador de Relatório de Editais para ONGs")

with st.form("filtros"):
    temas = st.multiselect("Temas", ["Educação", "Agricultura", "Tecnologia social", "Cidadania", "Cooperação internacional", "Diversos"], default=["Educação"])
    paises = st.multiselect("Países", ["Brasil", "Internacional"], default=["Internacional"])
    prazo_ate = st.date_input("Prazo até", value=datetime(2025, 6, 30))
    gerar = st.form_submit_button("🚀 Gerar Relatório")

if gerar:
    dados = coletar_oportunidades()
    df = pd.DataFrame(dados)
    df["PrazoFormatado"] = pd.to_datetime(df["Prazo"], dayfirst=True, errors='coerce')
    df = df[df["Tema"].isin(temas)]
    df = df[df["País"].isin(paises)]
    df = df[(df["PrazoFormatado"].notnull()) & (df["PrazoFormatado"] <= pd.to_datetime(prazo_ate))]
    df = df.drop(columns=["PrazoFormatado"])

    if df.empty:
        st.warning("Nenhum edital encontrado com os filtros selecionados.")
    else:
        agora = datetime.now().strftime("%Y-%m-%d_%H%M")
        excel_file = f"relatorio_{agora}.xlsx"
        pdf_file = f"relatorio_{agora}.pdf"
        df.to_excel(excel_file, index=False)
        gerar_pdf(df, pdf_file)

        st.success("Relatório gerado com sucesso! Faça o download abaixo:")
        with open(excel_file, "rb") as f:
            st.download_button("⬇️ Baixar Excel", data=f, file_name=excel_file)
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ Baixar PDF", data=f, file_name=pdf_file)
