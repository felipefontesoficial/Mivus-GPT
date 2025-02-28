import streamlit as st
from notion_client import Client
import os

# Carregar chave de variáveis de ambiente (recomendado)
NOTION_KEY = os.getenv("secret_sHJkVbWjFsK9ChFihQJFKyPiKdXJhuRibzWDgHLXGJz")  # Ou st.secrets["NOTION_KEY"]
page_id = "385257f0fa39428fb5413c5b87de7d8c"

try:
    notion = Client(auth=NOTION_KEY)
    page = notion.pages.retrieve(page_id=page_id)
    st.write(page)  # Exibir dados brutos para debug
except Exception as e:
    st.error(f"Erro na conexão com o Notion: {e}")
