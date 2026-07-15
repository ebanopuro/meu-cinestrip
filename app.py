import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
from io import BytesIO

# Configuração da página para visualização ampla
st.set_page_config(page_title="CineStrip Pro", layout="wide")

# --- ESTILO CSS PARA CINTA CINEMATOGRÁFICA ---
st.markdown("""
<style>
    /* Faz as imagens terem bordas de película */
    .stImage img {
        border: 15px solid #1a1a1a;
        border-left: 2px solid #333;
        border-right: 2px solid #333;
        border-radius: 4px;
    }
    /* Estiliza o título da cena */
    .scene-label {
        font-size: 12px;
        font-weight: bold;
        text-align: center;
        background: #e63946;
        color: white;
        padding: 2px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

def get_ai_image_url(prompt, style):
    full_prompt = f"Cinematic film still, {prompt}, {style}, 8k, highly detailed, anamorphic lens"
    encoded_prompt = requests.utils.quote(full_prompt)
    # Reduzi a resolução para 512x288 para carregar mais rápido no celular
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=288&nologo=true"

def download_image_bytes(url):
    try:
        response = requests.get(url, timeout=15)
        return BytesIO(response.content)
    except: return None

# --- INTERFACE ---
st.title("🎬 CineStrip Pro")

if 'scenes_list' not in st.session_state:
    st.session_state.scenes_list = []

# BARRA LATERAL (ENTRADA)
with st.sidebar:
    st.header("Configurações")
    estilo = st.selectbox("Estilo", ["Realista", "Noir", "Cyberpunk", "Esboço"])
    txt_input = st.text_area("Roteiro (uma cena por linha):", "Abertura do filme\nClose no herói\nA grande explosão", height=200)
    
    # Controle de tamanho para o usuário
    cols_per_row = st.slider("Cenas por linha", 1, 4, 3)
    
    if st.button("🚀 GERAR CINTA"):
        with st.spinner("Criando película..."):
            lines = [l.strip() for l in txt_input.split('\n') if l.strip()]
            new_scenes = []
            for i, line in enumerate(lines):
                url = get_ai_image_url(line, estilo)
                new_scenes.append({"cena": i+1, "acao": line, "url": url})
            st.session_state.scenes_list = new_scenes

# --- EXIBIÇÃO EM CINTA (COLUNAS) ---
if st.session_state.scenes_list:
    st.subheader("🎞️ Película de Storyboard")
    
    # Criamos as colunas dinamicamente para as imagens aparecerem lado a lado
    idx = 0
    while idx < len(st.session_state.scenes_list):
        cols = st.columns(cols_per_row)
        for col in cols:
            if idx < len(st.session_state.scenes_list):
                scene = st.session_state.scenes_list[idx]
                with col:
                    st.markdown(f"<div class='scene-label'>CENA {scene['cena']}</div>", unsafe_allow_html=True)
                    st.image(scene['url'], use_column_width=True)
                    with st.expander("Ver Ação"):
                        st.caption(scene['acao'])
                idx += 1

    # --- PDF ---
    st.divider()
    if st.button("📄 Preparar PDF para Exportação"):
        with st.spinner("Compilando PDF..."):
            pdf = FPDF()
            for scene in st.session_state.scenes_list:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"CENA {scene['cena']}", ln=True)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 8, f"Acao: {scene['acao']}")
                img_data = download_image_bytes(scene['url'])
                if img_data:
                    pdf.image(img_data, x=10, w=190)
            
            pdf_bytes = pdf.output(dest='S')
            st.download_button("⬇️ BAIXAR PDF", data=bytes(pdf_bytes), file_name="cinta_cinematografica.pdf")
else:
    st.info("Preencha o roteiro à esquerda e clique em 'Gerar Cinta'.")
