import streamlit as st
from pathlib import Path
import base64
import os

# ==========================================
# CONFIGURACIÓN INICIAL DE STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Pijao, Ciudad Sin Prisa",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# GESTIÓN DE RUTAS Y RECURSOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def find_asset(name, asset_types=["video", "image", "audio"]):
    """
    Busca dinámicamente el recurso en la carpeta assets/ independientemente de su extensión.
    No falla si el archivo no existe, devuelve None.
    """
    if not ASSETS_DIR.exists():
        return None
        
    extensions = {
        "video": [".mp4", ".webm", ".mov", ".mkv", ".MP4", ".WEBM", ".MOV"],
        "image": [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"],
        "audio": [".mp3", ".wav", ".ogg", ".MP3", ".WAV"]
    }
    
    for atype in asset_types:
        for ext in extensions.get(atype, []):
            file_path = ASSETS_DIR / f"{name}{ext}"
            if file_path.exists():
                return file_path
    return None

def render_missing(asset_name, height="200px"):
    """Muestra un espacio elegante cuando falta un recurso."""
    html = f"""
    <div style="height: {height}; display: flex; align-items: center; justify-content: center; 
                background-color: #EAE6DF; color: #8C867A; border-radius: 8px; font-style: italic; 
                margin: 1rem 0; border: 1px dashed #C4A484;">
        Recurso audiovisual pendiente: {asset_name}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_base64_image(file_path):
    """Convierte imágenes a Base64 para inyectarlas en componentes HTML (ej. Carrusel)"""
    if file_path and file_path.exists():
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = file_path.suffix.replace('.', '')
            return f"data:image/{ext};base64,{encoded}"
    return None

# ==========================================
# CONTROL DE ESTADO (PORTADA VS EXPERIENCIA)
# ==========================================
if 'started' not in st.session_state:
    st.session_state.started = False

def iniciar_travesia():
    st.session_state.started = True

# ==========================================
# PANTALLA 1: PORTADA CINEMATOGRÁFICA (HERO)
# ==========================================
if not st.session_state.started:
    # CSS Específico para forzar pantalla completa cinematográfica
    st.markdown("""
        <style>
        /* Ocultar elementos por defecto de Streamlit */
        header[data-testid="stHeader"] {display: none;}
        footer {display: none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        
        /* Convertir el video en fondo */
        div[data-testid="stVideo"] {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
        }
        div[data-testid="stVideo"] video {
            object-fit: cover; width: 100%; height: 100%;
        }
        
        /* Capa oscura superpuesta */
        .hero-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.45); z-index: -1;
        }
        
        /* Textos de la portada */
        .hero-content {
            position: fixed; top: 40%; left: 50%; transform: translate(-50%, -50%);
            text-align: center; color: white; z-index: 1; width: 100%;
            font-family: 'Playfair Display', serif;
        }
        .hero-content h1 {
            font-size: 6vw; font-weight: 700; margin: 0; letter-spacing: 2px;
            text-shadow: 2px 4px 10px rgba(0,0,0,0.7);
        }
        .hero-content h3 {
            font-size: 2vw; font-weight: 300; margin-top: 10px; font-family: 'Lato', sans-serif;
            text-shadow: 1px 2px 6px rgba(0,0,0,0.6); letter-spacing: 1px;
        }
        
        /* Botón Iniciar Travesía */
        div.stButton {
            position: fixed; top: 70%; left: 50%; transform: translate(-50%, -50%); z-index: 2;
        }
        div.stButton > button {
            background-color: transparent !important; color: white !important;
            border: 1px solid white !important; border-radius: 0px !important;
            padding: 15px 40px !important; font-size: 1.2rem !important;
            font-family: 'Lato', sans-serif; letter-spacing: 2px; transition: all 0.4s ease;
        }
        div.stButton > button:hover {
            background-color: rgba(255,255,255,0.2) !important; color: #fff !important; border-color: white !important;
        }
        
        /* Ajuste móvil */
        @media (max-width: 768px) {
            .hero-content h1 { font-size: 12vw; }
            .hero-content h3 { font-size: 4vw; }
            div.stButton { top: 75%; }
        }
        </style>
        
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1>PIJAO, CIUDAD SIN PRISA</h1>
            <h3>Te invitamos a recorrer lento a nuestro municipio</h3>
        </div>
    """, unsafe_allow_html=True)

    vpinicio = find_asset("VPINICIO", ["video"])
    if vpinicio:
        # Se inyecta usando st.video para no saturar RAM con Base64, el CSS lo convierte en fondo
        st.video(str(vpinicio), autoplay=True, loop=True, muted=True)
    else:
        st.markdown("<div style='position:fixed; top:0; left:0; width:100vw; height:100vh; background:#2C3E2D; z-index:-3;'></div>", unsafe_allow_html=True)
        render_missing("VPINICIO", height="100vh")
    
    st.button("INICIAR TRAVESÍA", on_click=iniciar_travesia)

# ==========================================
# PANTALLA 2: EXPERIENCIA PRINCIPAL
# ==========================================
else:
    # CSS de Diseño Editorial, Tipografías y Animaciones
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
        
        /* Reseteos y Fondos */
        header[data-testid="stHeader"] {display: none;}
        .block-container {padding-top: 2rem !important; padding-bottom: 5rem !important;}
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F8F5F0; color: #2A2A2A; font-family: 'Lato', sans-serif;
        }
        
        /* Tipografía Editorial */
        h1, h2, h3, h4 { font-family: 'Playfair Display', serif; color: #1E2B1E; }
        .section-title {
            font-size: 3rem; margin-top: 4rem; margin-bottom: 2rem; border-bottom: 2px solid #D4C4B4; 
            padding-bottom: 10px; color: #2C3E2D;
        }
        .editorial-text { font-size: 1.15rem; line-height: 1.8; text-align: justify; margin-bottom: 1.5rem; color: #3A3A3A;}
        
        /* Línea de tiempo */
        .timeline-container { border-left: 2px solid #8C7A6B; padding-left: 20px; margin-top: 2rem; margin-bottom: 2rem; }
        .timeline-item { margin-bottom: 2rem; position: relative; }
        .timeline-item::before {
            content: ''; position: absolute; left: -27px; top: 5px; width: 12px; height: 12px; 
            background-color: #4A5D23; border-radius: 50%;
        }
        .timeline-year { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: #6F4E37; margin-bottom: 0.2rem;}
        .timeline-desc { font-size: 1.1rem; line-height: 1.6; }
        
        /* Reproductor de Audio Flotante */
        .audio-container {
            position: fixed; bottom: 20px; right: 20px; z-index: 999;
            background: rgba(248, 245, 240, 0.9); padding: 10px 15px; border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #D4C4B4;
        }
        .audio-label { font-family: 'Playfair Display', serif; font-size: 0.9rem; font-weight: bold; color: #4A5D23; margin-bottom: 5px; text-align: center;}
        audio { height: 30px; width: 200px; }
        
        /* Botón Conoce Más */
        .btn-conoce-mas {
            display: inline-block; padding: 12px 30px; background-color: transparent; 
            color: #4A5D23; text-decoration: none; font-family: 'Lato', sans-serif; 
            border: 1px solid #4A5D23; letter-spacing: 1px; transition: 0.3s;
            margin-top: 2rem; font-weight: bold; text-align: center;
        }
        .btn-conoce-mas:hover { background-color: #4A5D23; color: #F8F5F0; }
        
        /* Carrusel CSS */
        .carousel-wrapper {
            width: 100%; overflow: hidden; margin: 4rem 0; position: relative;
        }
        .carousel-track {
            display: flex; gap: 15px; width: max-content;
            animation: scroll 60s linear infinite;
        }
        .carousel-track:hover { animation-play-state: paused; }
        .carousel-img {
            height: 400px; width: auto; object-fit: cover; border-radius: 4px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        
        /* Tarjetas Descubre */
        .descubre-card {
            background: white; padding: 2rem; border-top: 4px solid #4A5D23;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;
        }
        .descubre-card h3 { color: #6F4E37; font-size: 1.4rem; margin-top: 0;}
        
        /* Elementos Audiovisuales */
        div[data-testid="stVideo"] video { border-radius: 4px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)

    # REPRODUCTOR DE AUDIO AMBIENTAL (M1)
    m1 = find_asset("M1", ["audio"])
    if m1:
        # Codificamos el audio en Base64 para el reproductor flotante HTML/CSS
        with open(m1, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
            ext = m1.suffix.replace('.', '')
            audio_html = f"""
            <div class="audio-container">
                <div class="audio-label">SONIDO AMBIENTAL</div>
                <audio controls loop>
                    <source src="data:audio/{ext};base64,{audio_b64}">
                    Tu navegador no soporta el elemento de audio.
                </audio>
            </div>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

    # VIDEO INTRODUCTORIO (VIDEO)
    video_principal = find_asset("VIDEO", ["video"])
    if video_principal:
        st.video(str(video_principal))
    else:
        render_missing("VIDEO", height="500px")

    # ==========================================
    # SECCIÓN: CASAS DEL AYER
    # ==========================================
    st.markdown('<div class="section-title">CASAS DEL AYER</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("""
        <div class="editorial-text">
            La identidad visual de Pijao está esculpida en la madera de sus balcones y la solidez del bahareque. 
            Esta arquitectura tradicional, propia del Eje Cafetero, no es solo estética; es una respuesta sabia al clima de la cordillera y a la topografía del paisaje.
            <br><br>
            Las fachadas coloridas rinden homenaje al patrimonio vivo de un pueblo que decidió conservar su memoria intacta frente al paso del tiempo. Caminar por Pijao es recorrer un museo a cielo abierto de arquitectura cafetera.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        vp2 = find_asset("VP2", ["video"])
        if vp2:
            st.video(str(vp2), autoplay=True, loop=True, muted=True)
        else:
            render_missing("VP2")

    # ==========================================
    # SECCIÓN INTERMEDIA (BANNER)
    # ==========================================
    st.write("---")
    banner = find_asset("BANNER", ["video", "image"])
    if banner:
        if banner.suffix.lower() in [".mp4", ".webm", ".mov"]:
            st.video(str(banner), autoplay=True, loop=True, muted=True)
        else:
            st.image(str(banner), use_container_width=True)
    else:
        render_missing("BANNER")

    # ==========================================
    # SECCIÓN: HISTORIA DE GUERREROS
    # ==========================================
    st.markdown('<div class="section-title">HISTORIA DE GUERREROS</div>', unsafe_allow_html=True)
    
    hist_col1, hist_col2 = st.columns([1.2, 1], gap="large")
    with hist_col1:
        st.markdown("""
        <div class="editorial-text">
            Pijao es un territorio forjado por el temple de sus fundadores. Su nombre hace eco de la resistencia indígena ancestral, 
            mientras sus calles atestiguan el avance colonizador del siglo XX. Un municipio con corazón de café, 
            tejido entre montañas e historia departamental.
        </div>
        <div class="timeline-container">
            <div class="timeline-item">
                <div class="timeline-year">1902</div>
                <div class="timeline-desc">Fundación y denominación inicial como <strong>San José de Colón</strong> por don Antonio María Quintero, don Luis Jaramillo y Claudio Rivera.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1905</div>
                <div class="timeline-desc">Conversión en corregimiento de Calarcá, formando parte del naciente Departamento de Manizales (hoy Caldas).</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1912</div>
                <div class="timeline-desc">Creación oficial de la parroquia.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1926</div>
                <div class="timeline-desc">Mediante la Ordenanza 011 de la Asamblea Departamental de Caldas, es erigido como municipio.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">1931</div>
                <div class="timeline-desc">Adopta definitivamente el nombre de <strong>Pijao</strong>, honrando a la población indígena ancestral de la región.</div>
            </div>
            <div class="timeline-item">
                <div class="timeline-year">2014</div>
                <div class="timeline-desc">Ingresa orgullosamente a la red internacional <strong>Cittaslow</strong>, consolidándose como "Ciudad Sin Prisa".</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hist_col2:
        v3 = find_asset("V3", ["video"])
        if v3:
            st.video(str(v3), autoplay=True, loop=True, muted=True)
        else:
            render_missing("V3")
            
        st.write("")
        # Mostrar algunas fotos históricas sugeridas
        fotos_historia = ["F2", "F5", "F6", "F16", "F17"]
        for f_name in fotos_historia:
            f_path = find_asset(f_name, ["image"])
            if f_path:
                st.image(str(f_path), use_container_width=True)

    # ==========================================
    # SECCIÓN: CONOCE PIJAO E IDENTIDAD (V1)
    # ==========================================
    st.markdown('<div class="section-title">CONOCE PIJAO</div>', unsafe_allow_html=True)
    
    conoce_col1, conoce_col2 = st.columns([1, 1], gap="large")
    with conoce_col1:
        v1 = find_asset("V1", ["video"])
        if v1:
            st.video(str(v1))
        else:
            render_missing("V1")

    with conoce_col2:
        st.markdown("""
        <div class="editorial-text">
            Pijao es un paraíso enclavado en la Cordillera Central de Colombia. Aquí, la prisa es forastera. 
            El aroma a café tostado, el murmullo de sus ríos y la hospitalidad de su gente invitan a un turismo responsable y contemplativo.<br><br>
            Como primera <strong>Ciudad Sin Prisa</strong> de América Latina (Cittaslow), Pijao promueve la buena vida: 
            valorar el entorno local, proteger el patrimonio arquitectónico, saborear lo autóctono y respirar la naturaleza pura.
        </div>
        <a href="https://www.youtube.com/watch?v=UPRAk3g7YVg" target="_blank" class="btn-conoce-mas">CONOCE MÁS EN VIDEO</a>
        """, unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN: EL TERRITORIO Y CLIMA
    # ==========================================
    terr_col1, terr_col2 = st.columns([1, 1], gap="large")
    with terr_col1:
        st.markdown('<div class="section-title" style="margin-top:2rem;">EL TERRITORIO</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="editorial-text">
            Pijao se despliega sobre la imponente <strong>Cordillera Central</strong> andina. 
            Su geografía es un espectáculo de contrastes, dividido en tres paisajes predominantes:
            <br><br>
            <strong>Montaña:</strong> Cumbre rocosa y biodiversa que vigila el municipio.<br>
            <strong>Piedemonte:</strong> Tierra fértil y ondulada donde nace el café.<br>
            <strong>Valle:</strong> La cuna suave por donde discurre el agua fresca.<br><br>
            <strong>Ubicación Geográfica:</strong><br>
            • Norte: Córdoba<br>
            • Oriente: Departamento del Tolima<br>
            • Sur: Génova<br>
            • Occidente: Valle del Cauca<br>
            • Noroccidente: Buenavista<br>
            <br>
            <em>Centro poblado principal: La Mariela (A 32 km aprox. de Armenia).</em>
        </div>
        """, unsafe_allow_html=True)
        
    with terr_col2:
        st.markdown('<div class="section-title" style="margin-top:2rem;">CLIMA</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="editorial-text">
            La temperatura y el agua dictan el ritmo de vida y los ciclos agrícolas en Pijao.
            <br><br>
            El municipio goza de un clima bendecido por la cordillera, registrando:
            <ul>
                <li><strong>Alta Montaña:</strong> Precipitaciones superiores a los 2400 mm anuales, alimentando nacimientos de agua.</li>
                <li><strong>Otras zonas:</strong> Un balance térmico con lluvias aproximadas de 1800 mm anuales.</li>
                <li><strong>Vientos:</strong> Refrescado durante el día por brisas que ascienden desde el valle del río Cauca hacia las cumbres.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # CARRUSEL FOTOGRÁFICO CINEMATOGRÁFICO
    # ==========================================
    st.write("---")
    fotos_nombres = [f"F{i}" for i in range(1, 19)]
    fotos_html = ""
    for f_name in fotos_nombres:
        img_path = find_asset(f_name, ["image"])
        if img_path:
            b64_img = get_base64_image(img_path)
            if b64_img:
                fotos_html += f'<img src="{b64_img}" class="carousel-img">'
    
    if fotos_html:
        st.markdown(f"""
            <div class="carousel-wrapper">
                <div class="carousel-track">
                    {fotos_html}
                    {fotos_html} <!-- Duplicado para loop infinito fluido -->
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN: DESCUBRE PIJAO
    # ==========================================
    st.markdown('<div class="section-title">DESCUBRE PIJAO</div>', unsafe_allow_html=True)
    
    cat1, cat2, cat3 = st.columns(3)
    with cat1:
        st.markdown("""
        <div class="descubre-card">
            <h3>Arquitectura y Patrimonio</h3>
            <p>Recorre calles tapizadas de color, bahareque y balcones florecidos que susurran las historias de la colonización antioqueña.</p>
        </div>
        """, unsafe_allow_html=True)
    with cat2:
        st.markdown("""
        <div class="descubre-card">
            <h3>Naturaleza Viva</h3>
            <p>Respira aire puro entre cascadas, miradores y valles verdes. El piedemonte ofrece una conexión directa con la tierra fértil.</p>
        </div>
        """, unsafe_allow_html=True)
    with cat3:
        st.markdown("""
        <div class="descubre-card">
            <h3>Cultura de Café</h3>
            <p>Experimenta el proceso del mejor café del mundo desde el grano hasta la taza, de la mano amorosa de las familias campesinas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    cat4, cat5, cat6 = st.columns(3)
    with cat4:
        st.markdown("""
        <div class="descubre-card">
            <h3>Rutas y Recorridos</h3>
            <p>Camina sin afán por senderos que bordean ríos y ascienden montañas. Cada paso es un reencuentro con el bienestar espiritual.</p>
        </div>
        """, unsafe_allow_html=True)
    with cat5:
        st.markdown("""
        <div class="descubre-card">
            <h3>Tradición Local</h3>
            <p>Deléitate con la gastronomía tradicional y el calor humano de habitantes que cultivan la sonrisa tanto como la tierra.</p>
        </div>
        """, unsafe_allow_html=True)
    with cat6:
        st.markdown("""
        <div class="descubre-card">
            <h3>Experiencias Cittaslow</h3>
            <p>Desconéctate de la hiperactividad moderna. Aquí se valora el silencio, el sonido de las aves y las conversaciones pausadas.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)