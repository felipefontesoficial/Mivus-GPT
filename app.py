import streamlit as st
from notion_client import Client

# Configuração da API
notion = Client(auth="secret_sHJkVbWjFsK9ChFihQJFKyPiKdXJhuRibzWDgHLXGJz")  # Substitua pela sua chave
page_id = "385257f0fa39428fb5413c5b87de7d8c"  # ID da sua página (extraído do URL)

def display_notion_content():
    blocks = notion.blocks.children.list(block_id=page_id)["results"]
    
    for block in blocks:
        # Exemplo: tratamento de títulos e textos
        if block["type"] == "heading_1":
            st.title(block["heading_1"]["rich_text"][0]["plain_text"])
        elif block["type"] == "paragraph":
            st.write(block["paragraph"]["rich_text"][0]["plain_text"])
        # Adicione mais condições para listas, imagens, etc. (veja docs da API)

display_notion_content()
