import streamlit as st
import requests

# Credenciais OAuth (atenção: armazene de forma segura em produção)
CLIENT_ID = "1a8d872b-594c-8027-a9d6-003709543248"
CLIENT_SECRET = "secret_PK98Ne77Y1JxRa2dC1cIFQvHJyFQp5W1RaJlDkRxvmp"
# Defina o REDIRECT_URI conforme configurado na integração do Notion
REDIRECT_URI = "https://mivus-gpt.streamlit.app/"  # Ajuste conforme necessário
PAGE_ID = "385257f0fa39428fb5413c5b87de7d8c"

def exchange_code_for_token(auth_code):
    """
    Troca o código de autorização pelo token de acesso utilizando a API OAuth do Notion.
    """
    token_url = "https://api.notion.com/v1/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(token_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        st.error("Erro ao trocar o código de autorização pelo token de acesso.")
        st.write(response.text)
        return None

def get_page_blocks(access_token, page_id):
    """
    Busca os blocos (conteúdos) da página Notion utilizando o token de acesso.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    headers = {
        "Authorization": f"Bearer {access_token}",
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
    Renderiza os blocos básicos do Notion (parágrafos e cabeçalhos).
    """
    for block in blocks:
        block_type = block.get("type")
        if block_type == "paragraph":
            for text in block["paragraph"]["text"]:
                st.write(text.get("plain_text", ""))
        elif block_type == "heading_1":
            for text in block["heading_1"]["text"]:
                st.header(text.get("plain_text", ""))
        elif block_type == "heading_2":
            for text in block["heading_2"]["text"]:
                st.subheader(text.get("plain_text", ""))
        elif block_type == "heading_3":
            for text in block["heading_3"]["text"]:
                st.markdown(f"### {text.get('plain_text', '')}")
        else:
            st.info(f"Bloco do tipo '{block_type}' não está sendo renderizado.")

# Início da aplicação Streamlit
st.title("Integração Notion via OAuth com Streamlit")

st.markdown("### Passos para autenticação com o Notion:")
st.markdown("1. Acesse o link de autorização abaixo e autorize o acesso:")
auth_url = f"https://api.notion.com/v1/oauth/authorize?client_id={CLIENT_ID}&response_type=code&owner=user&redirect_uri={REDIRECT_URI}"
st.write(auth_url)
st.markdown("2. Após autorizar, você será redirecionado para a URL definida. Copie o parâmetro `code` (código de autorização) da URL e cole no campo abaixo:")

auth_code = st.text_input("Insira o código de autorização:")

if auth_code:
    access_token = exchange_code_for_token(auth_code)
    if access_token:
        st.success("Autenticação realizada com sucesso!")
        st.markdown("### Conteúdo da Página Notion:")
        blocks = get_page_blocks(access_token, PAGE_ID)
        if blocks:
            render_blocks(blocks)
        else:
            st.write("Nenhum conteúdo encontrado na página.")
