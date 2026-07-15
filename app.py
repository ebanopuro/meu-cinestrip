import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="CineStrip Pro", layout="wide")

def get_ai_image_url(prompt, style):
    full_prompt = f"Cinematic film still, {prompt}, {style}, 8k, high quality"
    encoded_prompt = requests.utils.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"

class StoryboardPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CINESTRIP AI - STORYBOARD', ln=True, align='C')

st.title("🎬 CineStrip AI")

# Entrada de dados
txt = st.text_area("Descreva as cenas (uma por linha):", "Um astronauta em Marte\nO foguete decolando")
estilo = st.selectbox("Estilo", ["Ultra-Realista", "Noir", "Cyberpunk"])

if st.button("Gerar Storyboard"):
    scenes = [{"cena": i+1, "acao": l} for i, l in enumerate(txt.split('\n')) if l.strip()]
    for s in scenes:
        st.write(f"### Cena {s['cena']}")
        url = get_ai_image_url(s['acao'], estilo)
        st.image(url)
        st.session_state[f"img_{s['cena']}"] = url

st.info("Para PDF e uso avançado, rode o deploy completo.")
