
import streamlit as st
import random

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Nampi Awajún", page_icon="🌿", layout="centered")

# Fondo selva amazónica
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?fit=crop&w=1400&q=80');
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
[data-testid="stToolbar"] {visibility: hidden;}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==============================
# BASE DE DATOS DE CARTAS
# ==============================
cartas = [
    ("Jabalí", "wájin", "imagenes/jabali.gif"),
    ("Tucán", "túkán", "imagenes/tucan.gif"),
    ("Arco", "ápin", "imagenes/arco.gif"),
    ("Cerbatana", "tsúin", "imagenes/cerbatana.gif"),
    ("Plátano", "bánan", "imagenes/platano.gif"),
    ("Yuca", "yáká", "imagenes/yuca.gif"),
    ("Río", "tsáim", "imagenes/rio.gif"),
    ("Flor", "táwen", "imagenes/flor.gif"),
]

# ==============================
# INICIALIZAR ESTADO
# ==============================
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
    st.session_state.puntuacion = 0
    st.session_state.cartas_volteadas = []
    st.session_state.matched = []

# Calcular número de pares por nivel
pares_por_nivel = 4 + (st.session_state.nivel - 1) * 2
cartas_nivel = random.sample(cartas, min(pares_por_nivel, len(cartas)))
cartas_nivel = cartas_nivel * 2  # duplicar para formar pares
random.shuffle(cartas_nivel)

st.title(f"🌿 Nampi Awajún – Nivel {st.session_state.nivel} 🌿")
st.write("¡Explora la selva y encuentra los pares! Aprende vocabulario en Awajún mientras juegas.")

# ==============================
# MOSTRAR CARTAS
# ==============================
cols = st.columns(4)
for idx, carta in enumerate(cartas_nivel):
    nombre_es, nombre_aw, img_url = carta
    if idx in st.session_state.matched:
        cols[idx % 4].image(img_url, caption=f"{nombre_es} ({nombre_aw})", use_column_width=True)
    else:
        if cols[idx % 4].button("🂠", key=f"{st.session_state.nivel}_{idx}"):
            if len(st.session_state.cartas_volteadas) < 2:
                st.session_state.cartas_volteadas.append((idx, carta))

# ==============================
# LÓGICA DE COMPARACIÓN
# ==============================
if len(st.session_state.cartas_volteadas) == 2:
    (idx1, c1), (idx2, c2) = st.session_state.cartas_volteadas
    if c1[1] == c2[1] and idx1 != idx2:
        st.session_state.puntuacion += 5
        st.session_state.matched.extend([idx1, idx2])
        st.success(f"✅ ¡Correcto! {c1[0]} = {c1[1]}")
    else:
        st.error("❌ Intenta de nuevo")
    st.session_state.cartas_volteadas = []
    st.experimental_rerun()

# ==============================
# PUNTUACIÓN Y FIN DE NIVEL
# ==============================
st.write(f"🏆 Puntuación actual: {st.session_state.puntuacion}")

if len(st.session_state.matched) == len(cartas_nivel):
    st.balloons()
    st.success(f"🎉 ¡Nivel {st.session_state.nivel} completado!")
    if st.session_state.nivel < 30:
        if st.button("➡️ Siguiente nivel"):
            st.session_state.nivel += 1
            st.session_state.cartas_volteadas = []
            st.session_state.matched = []
            st.experimental_rerun()
    else:
        st.success("🏁 ¡Has completado los 30 niveles! Felicitaciones!")
        if st.button("🔁 Jugar de nuevo"):
            st.session_state.nivel = 1
            st.session_state.puntuacion = 0
            st.session_state.cartas_volteadas = []
            st.session_state.matched = []
            st.experimental_rerun()
