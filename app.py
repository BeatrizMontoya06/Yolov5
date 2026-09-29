from PIL import Image
import io
import streamlit as st
import numpy as np
import pandas as pd
import torch

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bee's _ Cyber Object Detector v8.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS CYBERPUNK / HACKER TERMINAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@400;600;700&display=swap');

    /* Fondo Principal Matrix Cyber Grid */
    .stApp {
        background-color: #030208 !important;
        background-image: 
            radial-gradient(#140a24 15%, transparent 16%),
            linear-gradient(to right, rgba(0, 255, 65, 0.04) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0, 255, 65, 0.04) 1px, transparent 1px) !important;
        background-size: 50px 50px, 20px 20px, 20px 20px !important;
        color: #00ff41 !important;
        font-family: 'Fira Code', monospace !important;
    }

    /* Sidebar / Control Panel Hacker */
    [data-testid="stSidebar"] {
        background-color: #090412 !important;
        border-right: 3px solid #ff007f !important;
        box-shadow: 5px 0px 15px rgba(255, 0, 127, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #00ff41 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.25rem !important;
    }

    /* Header Cyber-Terminal */
    .hacker-header {
        background: #090412;
        border: 3px solid #00ff41;
        box-shadow: 6px 6px 0px #ff007f, -6px -6px 0px #00f0ff;
        padding: 15px 25px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .hacker-title {
        font-family: 'VT323', monospace !important;
        color: #00ff41 !important;
        font-size: 2.8rem;
        letter-spacing: 3px;
        margin: 0;
        text-shadow: 3px 3px 0px #ff007f;
    }

    .hacker-badge {
        background: #ff007f;
        color: #000000;
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        padding: 4px 12px;
        font-weight: bold;
        box-shadow: 3px 3px 0px #00ff41;
    }

    /* Paneles Cyber-HUD */
    .cyber-card {
        background: #080312;
        border: 2px solid #00f0ff;
        box-shadow: 5px 5px 0px #ff007f;
        padding: 20px;
        margin-bottom: 20px;
    }

    .cyber-card-green {
        background: #041207;
        border: 2px solid #00ff41;
        box-shadow: 5px 5px 0px #00f0ff;
        padding: 20px;
        margin-bottom: 20px;
    }

    .hud-title {
        font-family: 'VT323', monospace;
        font-size: 1.8rem;
        color: #00f0ff;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Consola Log Estilo Hacker */
    .sys-log {
        background: #000000;
        border: 1px solid #00ff41;
        color: #00ff41;
        padding: 10px;
        font-size: 0.85rem;
        font-family: 'Fira Code', monospace;
        height: 100px;
        overflow-y: auto;
        margin-bottom: 15px;
    }

    /* Sliders y Controles */
    .stSlider > div {
        color: #00ff41 !important;
    }

    /* Botones y Camara */
    button[data-testid="stBaseButton-secondary"] {
        background: #ff007f !important;
        color: #000000 !important;
        border: 2px solid #00ff41 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.5rem !important;
        box-shadow: 4px 4px 0px #00f0ff !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background: #00ff41 !important;
        color: #000000 !important;
        box-shadow: 4px 4px 0px #ff007f !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CARGA DEL MODELO YOLOv5
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        from ultralytics import YOLO
        model = YOLO("yolov5su.pt")
        return model
    except Exception as e:
        st.error(f"❌ [SYSTEM CRITICAL]: Error al cargar el núcleo neural YOLOv5: {str(e)}")
        return None

# ─────────────────────────────────────────────
# BANNER PRINCIPAL DE LA TERMINAL HACKER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hacker-header">
    <div>
        <h1 class="hacker-title">⚡ Bee's _ CYBER OBJECT DETECTOR</h1>
        <span style="color: #ff007f; font-family: 'VT323'; font-size: 1.2rem;">[SYSTEM_OPTICS_V8.0] // NEURAL RECOGNITION INTERFACE</span>
    </div>
    <div class="hacker-badge">SAT_LINK: ONLINE 🟢</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TELEMETRÍA SUPERIOR DE SISTEMA (DECORATIVO)
# ─────────────────────────────────────────────
col_t1, col_t2, col_t3, col_t4 = st.columns(4)
with col_t1:
    st.markdown("<div class='cyber-card' style='padding:10px;'><b style='color:#00f0ff;'>CPU LOAD:</b> 24.8%<br><small>NEURAL ENGINE READY</small></div>", unsafe_allow_html=True)
with col_t2:
    st.markdown("<div class='cyber-card' style='padding:10px;'><b style='color:#ff007f;'>TARGETING:</b> OPTICAL FEED<br><small>RESOLUTION: AUTO-SCALED</small></div>", unsafe_allow_html=True)
with col_t3:
    st.markdown("<div class='cyber-card' style='padding:10px;'><b style='color:#00ff41;'>ENCRYPTION:</b> AES-256<br><small>NODE: 127.0.0.1:8501</small></div>", unsafe_allow_html=True)
with col_t4:
    st.markdown("<div class='cyber-card' style='padding:10px;'><b style='color:#ffff00;'>ALGORITHM:</b> YOLOv5s-u<br><small>PYTORCH BACKEND</small></div>", unsafe_allow_html=True)

with st.spinner(">> INICIALIZANDO RED NEURAL DE RECONOCIMIENTO..."):
    model = load_model()

if model:
    # ─────────────────────────────────────────────
    # BARRA LATERAL: PARÁMETROS DE DETECCIÓN
    # ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ HACK_PARÁMETROS")
        st.markdown("Ajusta los umbrales de sensibilidad del escáner cibernético:")
        
        conf_threshold = st.slider("🔍 Confianza Mínima (CONF)", 0.0, 1.0, 0.25, 0.01)
        iou_threshold  = st.slider("📐 Umbral IoU", 0.0, 1.0, 0.45, 0.01)
        max_det        = st.number_input("💥 Máximas Detecciones", 10, 2000, 1000, 10)
        
        st.markdown("---")
        st.markdown("### 📟 SYSTEM LOGS")
        st.markdown("""
        <div class="sys-log">
        > SYSTEM BOOT OK...<br>
        > YOLO ENGINE LOADED<br>
        > CAMERA SENSOR ACTIVE<br>
        > WAITING FOR USER CAPTURE...
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # PANEL CENTRAL ARRIBA: CAPTURA ÓPTICA (CÁMARA)
    # ─────────────────────────────────────────────
    st.markdown("""
    <div class="cyber-card">
        <div class="hud-title">> OPTICAL_SENSOR // CAPTURA DE IMAGEN SATEIITAL</div>
    """, unsafe_allow_html=True)
    
    picture = st.camera_input("PROCESAR CAPTURA", key="camera")
    st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # RESULTADOS DE DETECCIÓN (LAYOUT INFERIOR)
    # ─────────────────────────────────────────────
    if picture:
        bytes_data = picture.getvalue()

        # Decodificación Pillow → BGR para YOLO
        pil_img = Image.open(io.BytesIO(bytes_data)).convert("RGB")
        np_img  = np.array(pil_img)[..., ::-1]

        with st.spinner(">> EJECUTANDO BÚSQUEDA Y EXTRACCIÓN DE PATRONES..."):
            try:
                results = model(
                    np_img,
                    conf=conf_threshold,
                    iou=iou_threshold,
                    max_det=int(max_det)
                )
            except Exception as e:
                st.error(f"❌ Error durante la detección: {str(e)}")
                st.stop()

        result        = results[0]
        boxes         = result.boxes
        annotated     = result.plot()
        annotated_rgb = annotated[:, :, ::-1]

        st.markdown("---")
        st.markdown("<h2 style='font-family:VT323; color:#00ff41; font-size:2.3rem;'>🎯 ANALYTICS HUD // OBJETOS LOCALIZADOS</h2>", unsafe_allow_html=True)

        col_img, col_data = st.columns([1.2, 1])

        with col_img:
            st.markdown("""
            <div class="cyber-card-green">
                <div class="hud-title" style="color:#00ff41;">> VISUAL_TARGET_ACQUIRED</div>
            """, unsafe_allow_html=True)
            st.image(annotated_rgb, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_data:
            st.markdown("""
            <div class="cyber-card">
                <div class="hud-title">> TELEMETRÍA_DE_OBJETOS</div>
            """, unsafe_allow_html=True)

            if boxes is not None and len(boxes) > 0:
                label_names    = model.names
                category_count = {}
                category_conf  = {}

                for box in boxes:
                    cat  = int(box.cls.item())
                    conf = float(box.conf.item())
                    category_count[cat] = category_count.get(cat, 0) + 1
                    category_conf.setdefault(cat, []).append(conf)

                data = [
                    {
                        "Categoría":          label_names[cat],
                        "Cantidad":           count,
                        "Confianza promedio": f"{np.mean(category_conf[cat]):.2f}"
                    }
                    for cat, count in category_count.items()
                ]

                df = pd.DataFrame(data)
                
                st.dataframe(df, use_container_width=True)
                
                st.markdown("<b style='color:#ff007f;'>MÉTRICA DE FRECUENCIA DETECTADA:</b>", unsafe_allow_html=True)
                st.bar_chart(df.set_index("Categoría")["Cantidad"])
            else:
                st.warning("⚠️ [NO TARGETS DETECTED]: No se encontraron patrones con los umbrales actuales.")
                st.caption("> Ajusta la Confianza Mínima (CONF) en el panel lateral para incrementar sensibilidad.")
            
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("❌ No se pudo cargar la red neural. Revisa los módulos PyTorch/Ultralytics.")
    st.stop()

# ─────────────────────────────────────────────
# PIE DE PÁGINA HACKER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-family: 'VT323'; color: #00f0ff; font-size: 1.2rem;">
    [BEE'S HACK_LABS] // CYBER OBJECT DETECTOR // POWERED BY YOLOV5 + PYTORCH + STREAMLIT
</div>
""", unsafe_allow_html=True)
