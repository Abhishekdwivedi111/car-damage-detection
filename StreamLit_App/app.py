import streamlit as st
from model_helper import predict

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarScan AI — Damage Detection",
    page_icon="🚗",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- Root variables ---- */
:root {
    --bg:        #0a0b0e;
    --surface:   #13151a;
    --border:    #1f2330;
    --accent:    #e8ff47;
    --accent2:   #ff5c5c;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --radius:    16px;
}

/* ---- Global reset ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 720px !important; margin: 0 auto; }

/* ---- Hero header ---- */
.hero {
    padding: 56px 24px 32px;
    text-align: center;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: var(--accent);
    color: #0a0b0e;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 20px;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(32px, 6vw, 52px) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -1.5px !important;
    color: var(--text) !important;
    margin: 0 0 12px !important;
}
.hero h1 span { color: var(--accent); }
.hero p {
    font-size: 15px;
    color: var(--muted);
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}
.glow-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 10px var(--accent);
    margin-right: 6px;
    vertical-align: middle;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.85); }
}

/* ---- Divider ---- */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 0 24px 36px;
}

/* ---- Upload zone ---- */
.upload-wrapper {
    background: var(--surface);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    padding: 36px 24px;
    margin: 0 24px 24px;
    text-align: center;
    transition: border-color .2s;
}
.upload-wrapper:hover { border-color: var(--accent); }
.upload-icon { font-size: 40px; margin-bottom: 10px; }
.upload-label {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}
.upload-sub { font-size: 13px; color: var(--muted); }

/* Override Streamlit file uploader */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 28px 24px !important;
    margin: 0 24px 24px !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] label {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
    font-size: 15px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div span {
    font-size: 14px !important;
    color: var(--muted) !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #0a0b0e !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: opacity .15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ---- Image card ---- */
.img-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin: 0 24px 20px;
}
.img-card-header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
[data-testid="stImage"] {
    border-radius: 0 !important;
}
[data-testid="stImage"] img {
    width: 100% !important;
    border-radius: 0 !important;
    display: block !important;
}

/* ---- Result card ---- */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 28px 24px;
    margin: 0 24px 40px;
    display: flex;
    align-items: flex-start;
    gap: 20px;
}
.result-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}
.result-icon.damage  { background: rgba(255, 92, 92, 0.12); }
.result-icon.normal  { background: rgba(232, 255, 71, 0.10); }
.result-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
    font-family: 'Syne', sans-serif;
}
.result-class {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 6px;
}
.result-class.damage { color: var(--accent2); }
.result-class.normal { color: var(--accent); }
.result-desc { font-size: 13px; color: var(--muted); line-height: 1.5; }

/* ── badges ── */
.badges {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin: 0 24px 12px;
}
.badge {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--muted);
    font-weight: 500;
}
.badge span { color: var(--text); font-weight: 600; }

/* ---- Spinner override ---- */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ---- Streamlit info/success/error overrides ---- */
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* ---- Footer ---- */
.footer {
    text-align: center;
    padding: 16px;
    font-size: 12px;
    color: var(--muted);
    border-top: 1px solid var(--border);
    margin-top: 16px;
}
.footer a { color: var(--accent); text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
DAMAGE_CLASSES  = {'Front Breakage', 'Front Crushed', 'Rear Breakage', 'Rear Crushed'}
NORMAL_CLASSES  = {'Front Normal', 'Rear Normal'}

CLASS_META = {
    'Front Breakage': ('💥', 'damage', 'Structural breakage detected at the front of the vehicle.'),
    'Front Crushed':  ('🚧', 'damage', 'Significant crush damage found at the front section.'),
    'Rear Breakage':  ('💥', 'damage', 'Structural breakage detected at the rear of the vehicle.'),
    'Rear Crushed':   ('🚧', 'damage', 'Significant crush damage found at the rear section.'),
    'Front Normal':   ('✅', 'normal', 'No visible damage detected at the front. Looks good!'),
    'Rear Normal':    ('✅', 'normal', 'No visible damage detected at the rear. Looks good!'),
}


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge"><span class="glow-dot"></span>AI-Powered</div>
    <h1>Car<span>Scan</span> AI</h1>
    <p>Upload a photo of the front or rear of any vehicle and get an instant damage assessment.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Stats badges ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="badges">
    <div class="badge">Model &nbsp;<span>ResNet-50</span></div>
    <div class="badge">Classes &nbsp;<span>6</span></div>
    <div class="badge">Format &nbsp;<span>JPG · PNG</span></div>
    <div class="badge">Max size &nbsp;<span>200 MB</span></div>
</div>
""", unsafe_allow_html=True)


# ── File uploader ─────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📂  Drop your vehicle photo here",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible",
)


# ── Processing ────────────────────────────────────────────────────────────────
if uploaded_file:
    # Save temp file
    image_path = "temp_file.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Image preview card
    st.markdown('<div class="img-card"><div class="img-card-header">📸 &nbsp;Uploaded Image</div>', unsafe_allow_html=True)
    st.image(uploaded_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Predict with spinner
    with st.spinner("Analyzing vehicle damage…"):
        prediction = predict(image_path)

    # Result card
    icon, kind, desc = CLASS_META.get(prediction, ('🔍', 'damage', ''))
    st.markdown(f"""
    <div class="result-card">
        <div class="result-icon {kind}">{icon}</div>
        <div>
            <div class="result-label">Prediction Result</div>
            <div class="result-class {kind}">{prediction}</div>
            <div class="result-desc">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <a href="https://streamlit.io">Streamlit</a> &amp; PyTorch · CarScan AI &copy; 2026
</div>
""", unsafe_allow_html=True)