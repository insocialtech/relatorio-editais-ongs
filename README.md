# 📊 Gerador de Relatório de Editais para ONGs

Esta aplicação permite que você gere relatórios em Excel e PDF com oportunidades (editais) abertos para ONGs, usando filtros como tema, país e prazo.

✅ Interface feita com [Streamlit](https://streamlit.io)  
✅ Raspagem de sites como Funds for NGOs e UNDP  
✅ Exportação automática dos relatórios  
✅ Download direto (sem login ou e-mail)

## 🚀 Como usar

1. Acesse o app online: [link do Streamlit Cloud](https://)
2. Selecione os filtros desejados
3. Clique em **Gerar Relatório**
4. Baixe os arquivos Excel ou PDF diretamente

## 🛠️ Tecnologias usadas

- `streamlit`
- `pandas`
- `requests`
- `beautifulsoup4`
- `fpdf`

## 📦 Como rodar localmente

```bash
git clone https://github.com/seu-usuario/relatorio-editais-ongs.git
cd relatorio-editais-ongs
pip install -r requirements.txt
streamlit run app_streamlit.py
