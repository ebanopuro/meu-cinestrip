import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
from io import BytesIO

# Configuração da página para Mobile
st.set_page_config(page_title="CineStrip Pro", layout="wide")

# --- FUNÇÕES CORE ---
def get_ai_image_url(prompt, style):
    # Engenharia de prompt automática para cinema
    full_prompt = f"Cinematic film still, movie scene, {prompt}, {style}, 8k, highly detailed, masterpiece, anamorphic lens"
    encoded_prompt = requests.utils.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"

def download_image_bytes(url):
    try:
        response = requests.get(url, timeout=15)
        return BytesIO(response.content)
    except:
        return None

# --- INTERFACE ---
st.title("🎬 CineStrip Pro")
st.write("Crie seu Storyboard e exporte em PDF")

# Estado da Sessão para as imagens não sumirem
if 'scenes_list' not in st.session_state:
    st.session_state.scenes_list = []

with st.sidebar:
    st.header("Configurações")
    estilo = st.selectbox("Estilo Visual", ["Realista", "Noir (P&B)", "Cyberpunk", "Esboço"])
    txt_input = st.text_area("Descreva as cenas (uma por linha):", "Um detetive na chuva\nUm carro preto em alta velocidade\nO vilão nas sombras")
    
    if st.button("🚀 GERAR STORYBOARD"):
        with st.spinner("Gerando imagens cinematográficas..."):
            lines = [l.strip() for l in txt_input.split('\n') if l.strip()]
            new_scenes = []
            for i, line in enumerate(lines):
                url = get_ai_image_url(line, estilo)
                new_scenes.append({"cena": i+1, "acao": line, "url": url})
            st.session_state.scenes_list = new_scenes

# --- EXIBIÇÃO DAS IMAGENS ---
if st.session_state.scenes_list:
    for scene in st.session_state.scenes_list:
        with st.container():
            st.markdown(f"### 🎞️ Cena {scene['cena']}")
            st.image(scene['url'], use_column_width=True)
            st.caption(f"Ação: {scene['acao']}")
            st.divider()

    # --- GERAÇÃO DE PDF ---
    st.subheader("📄 Exportar Trabalho")
    if st.button("Preparar PDF para Download"):
        with st.spinner("Criando PDF... isso pode levar alguns segundos."):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            for scene in st.session_state.scenes_list:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"CENA {scene['cena']}", ln=True)
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, f"Acao: {scene['acao']}")
                
                # Baixa a imagem para inserir no PDF
                img_data = download_image_bytes(scene['url'])
                if img_data:
                    pdf.image(img_data, x=10, w=190)
                
            pdf_output = pdf.output(dest='S')
            st.download_button(
                label="⬇️ BAIXAR PDF AGORA",
                data=bytes(pdf_output),
                file_name="storyboard_cinestrip.pdf",
                mime="application/pdf"
            )
else:
    st.info("Escreva o roteiro na lateral e clique em 'Gerar Storyboard'.")

# Estilo para parecer um rolo de filme
st.markdown("""
<style>
    .stImage { border: 10px solid #1a1a1a; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)
