
import streamlit as st
import requests

# Substitua pelos seus dados
NOTION_API_KEY = "secret_PK98Ne77Y1JxRa2dC1cIFQvHJyFQp5W1RaJlDkRxvmp"
PAGE_ID = "385257f0fa39428fb5413c5b87de7d8c"  # Extraia o ID da sua página Notion

def get_page_blocks(page_id):
    """
    Busca os blocos (conteúdos) da página Notion via API.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Erro ao buscar os dados do Notion.")
        st.write(response.text)
        return []
    return response.json().get("results", [])

def render_blocks(blocks):
    """
    Renderiza alguns dos blocos mais comuns (parágrafos e cabeçalhos)
    no Streamlit.
    """
    for block in blocks:
        block_type = block.get("type")
        if block_type == "paragraph":
            texts = block["paragraph"]["text"]
            for text in texts:
                st.write(text.get("plain_text", ""))
        elif block_type == "heading_1":
            texts = block["heading_1"]["text"]
            for text in texts:
                st.header(text.get("plain_text", ""))
        elif block_type == "heading_2":
            texts = block["heading_2"]["text"]
            for text in texts:
                st.subheader(text.get("plain_text", ""))
        elif block_type == "heading_3":
            texts = block["heading_3"]["text"]
            for text in texts:
                st.markdown(f"### {text.get('plain_text', '')}")
        else:
            # Aqui você pode tratar outros tipos de bloco conforme necessário
            st.info(f"Bloco do tipo '{block_type}' não está sendo renderizado.")

# Busca os blocos da página
blocks = get_page_blocks(PAGE_ID)

if blocks:
    render_blocks(blocks)
else:
    st.write("Nenhum conteúdo encontrado.")
