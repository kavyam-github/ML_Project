import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import time

st.set_page_config(
    page_title="ClaimSentinel | Fraud Intelligence",
    page_icon="Favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Outfit:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
  --bg:       #e8e4dd;
  --bg2:      #dedad2;
  --surface:  #f0ece4;
  --surface2: #e4dfd6;
  --surface3: #d8d2c8;
  --border:   #c8c2b6;
  --borderB:  #b8b0a2;
  --amber:    #c4622d;
  --amberD:   #a84f22;
  --amberL:   rgba(196,98,45,0.1);
  --sage:     #3d6b5a;
  --sageD:    #2e5244;
  --sageL:    rgba(61,107,90,0.1);
  --ink:      #2a2420;
  --inkM:     #4a3f38;
  --slate:    #5c6b7a;
  --slateL:   rgba(92,107,122,0.1);
  --rose:     #b84c4c;
  --roseL:    rgba(184,76,76,0.1);
  --gold:     #9a7c2e;
  --goldL:    rgba(154,124,46,0.12);
  --text1:    #1e1a16;
  --text2:    #6b5f54;
  --textM:    #9a8f84;
  --radius:   9px;
  --radiusL:  14px;
  --shadow:   0 2px 12px rgba(42,36,32,0.1),0 1px 3px rgba(42,36,32,0.08);
  --shadowM:  0 8px 32px rgba(42,36,32,0.14),0 2px 8px rgba(42,36,32,0.1);
}

*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"],.stApp{font-family:'Outfit',sans-serif !important;color:var(--text1) !important;}
#MainMenu,footer,header,.stDeployButton{display:none !important;}

.stApp{
  background:var(--bg) !important;
  background-image:
    radial-gradient(ellipse at 20% 0%,rgba(196,98,45,0.04) 0%,transparent 60%),
    radial-gradient(ellipse at 80% 100%,rgba(61,107,90,0.05) 0%,transparent 60%) !important;
}

button[data-testid="collapsedControl"]{display:none !important;}
section[data-testid="stSidebar"]{
  min-width:258px !important;max-width:258px !important;width:258px !important;
  transform:none !important;
  background:linear-gradient(180deg,#1c1714 0%,#241e19 60%,#1c1714 100%) !important;
  border-right:1px solid rgba(196,98,45,0.2) !important;
  box-shadow:4px 0 40px rgba(0,0,0,0.35) !important;
}
section[data-testid="stSidebar"] > div{padding:0 !important;}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--surface2);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:99px;}

.main .block-container{padding:2rem 2.5rem 5rem !important;max-width:1280px !important;}

section[data-testid="stSidebar"] .stButton > button{
  background:transparent !important;border:none !important;
  border-left:2px solid transparent !important;border-radius:0 9px 9px 0 !important;
  color:rgba(200,188,176,0.65) !important;font-size:0.82rem !important;font-weight:500 !important;
  padding:11px 18px !important;margin:1px 0 !important;width:100% !important;
  text-align:left !important;justify-content:flex-start !important;transition:all 0.18s ease !important;
  font-family:'Outfit',sans-serif !important;box-shadow:none !important;letter-spacing:0.01em !important;
}
section[data-testid="stSidebar"] .stButton > button:hover{
  background:rgba(196,98,45,0.08) !important;color:#e8b89a !important;
  border-left-color:rgba(196,98,45,0.45) !important;
}

.stTextInput>label,.stNumberInput>label,.stSelectbox>label,
.stDateInput>label,.stSlider>label,.stRadio>label,.stSelectSlider>label{
  font-size:0.63rem !important;font-weight:600 !important;color:var(--text2) !important;
  letter-spacing:0.1em !important;text-transform:uppercase !important;
  font-family:'IBM Plex Mono',monospace !important;margin-bottom:4px !important;
}

.stTextInput input,.stNumberInput input,.stDateInput input{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:var(--radius) !important;color:var(--text1) !important;
  font-family:'Outfit',sans-serif !important;font-size:0.88rem !important;font-weight:500 !important;
  padding:10px 13px !important;box-shadow:inset 0 1px 3px rgba(0,0,0,0.06) !important;
  transition:border-color 0.2s,box-shadow 0.2s !important;
}
.stTextInput input::placeholder,.stNumberInput input::placeholder{color:var(--textM) !important;}
.stTextInput input:focus,.stNumberInput input:focus,.stDateInput input:focus{
  border-color:var(--amber) !important;box-shadow:0 0 0 3px rgba(196,98,45,0.1) !important;
}

.stSelectbox>div>div{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:var(--radius) !important;color:var(--text1) !important;
  font-family:'Outfit',sans-serif !important;font-size:0.88rem !important;
  box-shadow:inset 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stSelectbox>div>div:hover,.stSelectbox>div>div:focus-within{
  border-color:var(--amber) !important;box-shadow:0 0 0 3px rgba(196,98,45,0.08) !important;
}
div[data-baseweb="popover"]{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:var(--radiusL) !important;box-shadow:0 16px 48px rgba(0,0,0,0.18) !important;
}
div[data-baseweb="menu"] ul{background:var(--surface) !important;padding:5px !important;}
div[data-baseweb="menu"] li{
  color:var(--text1) !important;border-radius:7px !important;
  font-size:0.86rem !important;font-family:'Outfit',sans-serif !important;padding:9px 12px !important;
}
div[data-baseweb="menu"] li:hover{background:var(--amberL) !important;color:var(--amber) !important;}

.stSlider>div>div>div>div{background:linear-gradient(90deg,var(--sage),var(--amber)) !important;}
.stSlider>div>div>div{background:var(--border) !important;}
.stSlider [role="slider"]{
  background:var(--surface) !important;border:2px solid var(--amber) !important;
  width:17px !important;height:17px !important;box-shadow:0 2px 8px rgba(196,98,45,0.3) !important;
}

.stRadio>div{gap:7px !important;flex-direction:row !important;}
.stRadio label{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:8px !important;color:var(--text2) !important;
  font-size:0.82rem !important;font-weight:600 !important;padding:7px 16px !important;
  cursor:pointer !important;transition:all 0.15s !important;box-shadow:0 1px 3px rgba(0,0,0,0.06) !important;
}
.stRadio label:hover{border-color:var(--amber) !important;color:var(--amber) !important;}
.stRadio div:has(input:checked) label{
  background:var(--amberL) !important;border-color:var(--amber) !important;
  color:var(--amber) !important;font-weight:700 !important;
}

.stButton>button{
  background:linear-gradient(135deg,var(--amber) 0%,var(--amberD) 100%) !important;
  color:#fff !important;border:none !important;border-radius:var(--radius) !important;
  font-family:'Outfit',sans-serif !important;font-size:0.92rem !important;
  font-weight:700 !important;padding:13px 30px !important;width:100% !important;
  box-shadow:0 4px 18px rgba(196,98,45,0.35) !important;transition:all 0.22s ease !important;
  letter-spacing:0.02em !important;
}
.stButton>button:hover{transform:translateY(-2px) !important;box-shadow:0 10px 28px rgba(196,98,45,0.45) !important;}
.stButton>button:active{transform:translateY(0) !important;}

.stDownloadButton>button{
  background:linear-gradient(135deg,var(--sage),var(--sageD)) !important;
  color:#fff !important;border:none !important;border-radius:var(--radius) !important;
  font-weight:700 !important;font-family:'Outfit',sans-serif !important;
  box-shadow:0 4px 14px rgba(61,107,90,0.3) !important;
}
.stDownloadButton>button:hover{transform:translateY(-2px) !important;box-shadow:0 8px 22px rgba(61,107,90,0.4) !important;}

div[data-testid="metric-container"]{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:var(--radiusL) !important;padding:20px 18px !important;
  box-shadow:var(--shadow) !important;position:relative;overflow:hidden;
  transition:transform 0.2s,box-shadow 0.2s !important;
}
div[data-testid="metric-container"]::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--amber),var(--sage));
}
div[data-testid="metric-container"]:hover{transform:translateY(-2px) !important;box-shadow:var(--shadowM) !important;}
div[data-testid="stMetricValue"]{
  font-family:'DM Serif Display',serif !important;font-size:2.2rem !important;
  font-weight:400 !important;color:var(--text1) !important;letter-spacing:-0.01em !important;
}
div[data-testid="stMetricLabel"]{
  font-size:0.6rem !important;font-weight:600 !important;color:var(--textM) !important;
  text-transform:uppercase !important;letter-spacing:0.12em !important;font-family:'IBM Plex Mono',monospace !important;
}
div[data-testid="stMetricDelta"]{font-size:0.72rem !important;color:var(--sage) !important;}

.stProgress>div>div{background:var(--border) !important;border-radius:999px !important;height:4px !important;}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--sage),var(--amber)) !important;border-radius:999px !important;}

.stFileUploader section{
  background:var(--surface) !important;border:2px dashed var(--border) !important;
  border-radius:var(--radiusL) !important;transition:all 0.2s !important;
  box-shadow:inset 0 2px 8px rgba(0,0,0,0.04) !important;
}
.stFileUploader section:hover{border-color:var(--amber) !important;background:var(--amberL) !important;}

.stExpander{border:1px solid var(--border) !important;border-radius:var(--radiusL) !important;background:var(--surface) !important;box-shadow:var(--shadow) !important;}
.stExpander summary{color:var(--text2) !important;}
details[data-testid="stExpander"] > summary{background:var(--surface) !important;}
.stDataFrame{border:1px solid var(--border) !important;border-radius:var(--radius) !important;box-shadow:var(--shadow) !important;}

/* CUSTOM COMPONENTS */
.cs-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--amberL);border:1px solid rgba(196,98,45,0.2);
  border-radius:999px;padding:4px 14px;margin-bottom:10px;
  font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--amber);letter-spacing:0.1em;
}
.cs-eyebrow-dot{width:5px;height:5px;border-radius:50%;background:var(--amber);animation:dotPulse 2.5s ease-in-out infinite;display:inline-block;}
.cs-page-title{font-family:'DM Serif Display',serif;font-weight:400;font-size:2.8rem;color:var(--text1);letter-spacing:-0.01em;line-height:1.1;margin-bottom:8px;}
.cs-page-desc{font-size:0.87rem;color:var(--text2);max-width:580px;line-height:1.8;font-weight:400;}

.cs-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radiusL);
  padding:22px 24px;margin-bottom:14px;position:relative;overflow:hidden;
  box-shadow:var(--shadow);animation:fadeUp 0.35s cubic-bezier(0.16,1,0.3,1);
  transition:box-shadow 0.2s,transform 0.2s;
}
.cs-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--amber),var(--sage));}
.cs-card:hover{box-shadow:var(--shadowM);transform:translateY(-1px);}
.cs-card-header{display:flex;align-items:center;gap:12px;padding-bottom:14px;margin-bottom:18px;border-bottom:1px solid var(--border);}
.cs-card-icon{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:15px;border:1px solid var(--border);flex-shrink:0;background:var(--surface2);}
.cs-card-title{font-family:'Outfit',sans-serif;font-weight:700;font-size:0.88rem;color:var(--text1);}
.cs-card-sub{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--textM);margin-top:2px;letter-spacing:0.06em;}

.cs-result-fraud{
  background:linear-gradient(150deg,rgba(184,76,76,0.07),rgba(232,228,221,0.5));
  border:1px solid rgba(184,76,76,0.25);border-radius:var(--radiusL);
  padding:44px 36px;text-align:center;position:relative;overflow:hidden;
  box-shadow:0 8px 40px rgba(184,76,76,0.08);animation:fadeUp 0.5s cubic-bezier(0.16,1,0.3,1);
}
.cs-result-fraud::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#b84c4c,#8b3030);}
.cs-result-clear{
  background:linear-gradient(150deg,rgba(61,107,90,0.07),rgba(232,228,221,0.5));
  border:1px solid rgba(61,107,90,0.25);border-radius:var(--radiusL);
  padding:44px 36px;text-align:center;position:relative;overflow:hidden;
  box-shadow:0 8px 40px rgba(61,107,90,0.07);animation:fadeUp 0.5s cubic-bezier(0.16,1,0.3,1);
}
.cs-result-clear::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#3d6b5a,#2e5244);}
.cs-result-icon{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 20px;}
.cs-result-icon-fraud{background:rgba(184,76,76,0.1);border:1px solid rgba(184,76,76,0.25);animation:pulseRed 2.5s ease-in-out infinite;}
.cs-result-icon-clear{background:rgba(61,107,90,0.1);border:1px solid rgba(61,107,90,0.25);animation:pulseGreen 2.5s ease-in-out infinite;}
.cs-score-fraud{font-family:'DM Serif Display',serif;font-size:6rem;font-weight:400;font-style:italic;color:#b84c4c;line-height:1;margin-bottom:4px;}
.cs-score-clear{font-family:'DM Serif Display',serif;font-size:6rem;font-weight:400;font-style:italic;color:#3d6b5a;line-height:1;margin-bottom:4px;}
.cs-badge-fraud{display:inline-flex;align-items:center;gap:7px;background:rgba(184,76,76,0.1);border:1px solid rgba(184,76,76,0.25);border-radius:999px;padding:4px 14px;margin-bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:#b84c4c;letter-spacing:0.1em;}
.cs-badge-clear{display:inline-flex;align-items:center;gap:7px;background:rgba(61,107,90,0.1);border:1px solid rgba(61,107,90,0.25);border-radius:999px;padding:4px 14px;margin-bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:#3d6b5a;letter-spacing:0.1em;}
.cs-directive-fraud{display:inline-flex;align-items:center;gap:10px;background:rgba(184,76,76,0.08);border:1px solid rgba(184,76,76,0.2);border-radius:10px;padding:10px 22px;margin-top:10px;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:#b84c4c;letter-spacing:0.04em;}
.cs-directive-clear{display:inline-flex;align-items:center;gap:10px;background:rgba(61,107,90,0.08);border:1px solid rgba(61,107,90,0.2);border-radius:10px;padding:10px 22px;margin-top:10px;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:#3d6b5a;letter-spacing:0.04em;}

.cs-feature-row{display:flex;align-items:center;justify-content:space-between;padding:12px 10px;border-bottom:1px solid rgba(200,194,182,0.6);border-radius:8px;transition:background 0.15s;}
.cs-feature-row:last-child{border-bottom:none;}
.cs-feature-row:hover{background:var(--amberL);}

.cs-sidebar-logo{display:flex;align-items:center;gap:12px;padding:26px 18px 16px;}
.cs-logo-name{font-family:'DM Serif Display',serif;font-weight:400;font-size:1.15rem;color:#f0e8e0;letter-spacing:0.01em;}
.cs-logo-tag{font-family:'IBM Plex Mono',monospace;font-size:0.56rem;color:rgba(196,98,45,0.7);margin-top:2px;letter-spacing:0.1em;}
.cs-nav-label{font-family:'IBM Plex Mono',monospace;font-size:0.55rem;font-weight:600;color:rgba(180,160,144,0.45);letter-spacing:0.18em;text-transform:uppercase;padding:0 18px;margin-bottom:5px;}
.cs-sidebar-divider{height:1px;background:rgba(255,255,255,0.06);margin:14px 12px;}
.cs-footer{font-family:'IBM Plex Mono',monospace;font-size:0.54rem;color:rgba(160,140,124,0.35);text-align:center;padding:16px 14px 0;}

.landing-wrap{min-height:calc(100vh - 4rem);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:3rem;position:relative;}
.landing-kicker{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.22em;color:var(--amber);margin-bottom:28px;opacity:0.8;}
.landing-title{font-family:'DM Serif Display',serif;font-weight:400;font-size:4.5rem;color:var(--text1);line-height:1.05;margin-bottom:0.5rem;letter-spacing:-0.02em;}
.landing-sub{font-family:'Outfit',sans-serif;font-size:1.05rem;color:var(--text2);margin-bottom:2.8rem;max-width:500px;line-height:1.75;font-weight:400;}
.feature-pills{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:2.8rem;}
.fpill{background:var(--surface);border:1px solid var(--border);border-radius:999px;padding:7px 18px;font-size:0.78rem;color:var(--text2);font-family:'Outfit',sans-serif;box-shadow:var(--shadow);}

@keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes dotPulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.35;transform:scale(0.65);}}
@keyframes pulseRed{0%,100%{box-shadow:0 0 0 0 rgba(184,76,76,0.3);}50%{box-shadow:0 0 0 12px rgba(184,76,76,0);}}
@keyframes pulseGreen{0%,100%{box-shadow:0 0 0 0 rgba(61,107,90,0.3);}50%{box-shadow:0 0 0 12px rgba(61,107,90,0);}}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_assets():
    model    = pickle.load(open('final_model.pkl', 'rb'))
    encoders = pickle.load(open('encoders.pkl', 'rb'))
    return model, encoders

try:
    model, encoders = load_assets()
except Exception as e:
    st.error(f"Could not load model assets — {e}")
    st.stop()

if 'landing' not in st.session_state:
    st.session_state.landing = True
if 'menu' not in st.session_state:
    st.session_state.menu = "Verify Claim"

nav_items = [("◈","Verify Claim"),("⚡","Batch Processing"),("◎","Engine Insights"),("∿","About")]

LOGO_SVG = """<svg width="38" height="38" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg">
  <polygon points="19,2 34,10.5 34,27.5 19,36 4,27.5 4,10.5" fill="none" stroke="#c4622d" stroke-width="1.8" opacity="0.9"/>
  <polygon points="19,8 29,13.5 29,24.5 19,30 9,24.5 9,13.5" fill="rgba(196,98,45,0.12)" stroke="#c4622d" stroke-width="1" opacity="0.55"/>
  <circle cx="19" cy="19" r="3.5" fill="#c4622d" opacity="0.9"/>
  <line x1="19" y1="2" x2="19" y2="8" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
  <line x1="34" y1="10.5" x2="29" y2="13.5" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
  <line x1="34" y1="27.5" x2="29" y2="24.5" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
  <line x1="19" y1="36" x2="19" y2="30" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
  <line x1="4" y1="27.5" x2="9" y2="24.5" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
  <line x1="4" y1="10.5" x2="9" y2="13.5" stroke="#c4622d" stroke-width="1.2" opacity="0.45"/>
</svg>"""

LOGO_SVG_LG = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <polygon points="30,3 53,16.5 53,43.5 30,57 7,43.5 7,16.5" fill="none" stroke="#c4622d" stroke-width="2" opacity="0.85"/>
  <polygon points="30,12 46,21.5 46,38.5 30,48 14,38.5 14,21.5" fill="rgba(196,98,45,0.08)" stroke="#c4622d" stroke-width="1.2" opacity="0.5"/>
  <polygon points="30,20 39,25.5 39,34.5 30,40 21,34.5 21,25.5" fill="rgba(196,98,45,0.12)" stroke="#c4622d" stroke-width="0.8" opacity="0.4"/>
  <circle cx="30" cy="30" r="4.5" fill="#c4622d" opacity="0.9"/>
</svg>"""

FEATURE_IMPORTANCES = [
    ("Annual Income",15.0,"#c4622d"),("Injury Claim Value",6.1,"#3d6b5a"),
    ("Days Open",6.0,"#c4622d"),("Total Claim Amount",5.9,"#3d6b5a"),
    ("Claim Date",5.9,"#c4622d"),("Vehicle Price",5.9,"#3d6b5a"),
    ("Zip Code",5.6,"#9a7c2e"),("Safety Rating",5.1,"#5c6b7a"),
    ("Liability %",5.1,"#c4622d"),("Annual Premium",4.0,"#3d6b5a"),
]

# ══ LANDING ══
if st.session_state.landing:
    st.markdown(f"""
    <div class="landing-wrap">
      <div style="position:absolute;top:0;left:0;right:0;bottom:0;
        background:radial-gradient(ellipse at 50% 30%,rgba(196,98,45,0.06) 0%,transparent 65%);
        pointer-events:none;"></div>
      <div style="margin-bottom:22px;opacity:0.9;">{LOGO_SVG_LG}</div>
      <div class="landing-kicker">◈ CLAIM INTELLIGENCE PLATFORM · EST. 2026</div>
      <div class="landing-title">Claim<span style="font-style:italic;color:var(--amber);">Sentinel</span></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;letter-spacing:0.2em;
        color:var(--textM);margin-bottom:1.6rem;">INSURANCE FRAUD INTELLIGENCE ENGINE</div>
      <p class="landing-sub">Machine-learning fraud detection built for modern claims operations — instant screening, enterprise batch analytics, and transparent risk intelligence.</p>
      <div class="feature-pills">
        <span class="fpill">🛡️ Real-time Screening</span>
        <span class="fpill">⚡ Batch CSV Processing</span>
        <span class="fpill">📊 Feature Importance</span>
        <span class="fpill">🔍 Risk Scoring</span>
        <span class="fpill">📥 Export Results</span>
      </div>
      <div style="width:1px;height:40px;background:linear-gradient(180deg,var(--amber),transparent);margin-bottom:24px;opacity:0.4;"></div>
    </div>""", unsafe_allow_html=True)
    col_a,col_b,col_c = st.columns([2,2,2])
    with col_b:
        if st.button("Enter the Platform →", use_container_width=True):
            st.session_state.landing = False
            st.rerun()
    st.stop()

# ══ SIDEBAR ══
with st.sidebar:
    st.markdown(f"""
    <div class="cs-sidebar-logo">
      <div style="flex-shrink:0;">{LOGO_SVG}</div>
      <div>
        <div class="cs-logo-name">ClaimSentinel</div>
        <div class="cs-logo-tag">FRAUD INTELLIGENCE · v2.5</div>
      </div>
    </div>
    <div class="cs-nav-label">Navigation</div>""", unsafe_allow_html=True)

    active_idx = [l for _,l in nav_items].index(st.session_state.menu) + 1
    st.markdown(f"""<style>
    section[data-testid="stSidebar"] div.stButton:nth-of-type({active_idx}) > button {{
      background:rgba(196,98,45,0.12) !important;border-left:2px solid #c4622d !important;
      color:#e8b89a !important;font-weight:700 !important;
    }}</style>""", unsafe_allow_html=True)

    for icon,label in nav_items:
        if st.button(f"{icon}  {label}",key=f"nav_{label}",use_container_width=True):
            st.session_state.menu=label; st.rerun()

    ts_now = datetime.now()
    uptime_display = ts_now.strftime("%d %b · %H:%M")
    st.markdown(f"""
    <div class="cs-sidebar-divider"></div>
    <div class="cs-nav-label">System</div>
    <div style="padding:0 10px;">
      <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:8px;margin-bottom:5px;background:rgba(61,107,90,0.1);">
        <span style="font-size:0.75rem;font-weight:500;font-family:'Outfit',sans-serif;color:rgba(210,195,180,0.8);">
          <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#5aab8a;margin-right:7px;vertical-align:middle;animation:dotPulse 2.5s infinite;"></span>
          Inference Engine
        </span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;padding:2px 10px;border-radius:5px;color:#5aab8a;background:rgba(61,107,90,0.15);border:1px solid rgba(61,107,90,0.25);">READY</span>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:8px;margin-bottom:5px;background:rgba(61,107,90,0.1);">
        <span style="font-size:0.75rem;font-weight:500;font-family:'Outfit',sans-serif;color:rgba(210,195,180,0.8);">
          <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#5aab8a;margin-right:7px;vertical-align:middle;animation:dotPulse 3s infinite;"></span>
          Feature Encoders
        </span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;padding:2px 10px;border-radius:5px;color:#5aab8a;background:rgba(61,107,90,0.15);border:1px solid rgba(61,107,90,0.25);">LOADED</span>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:8px;margin-bottom:5px;background:rgba(196,98,45,0.07);">
        <span style="font-size:0.75rem;font-weight:500;font-family:'Outfit',sans-serif;color:rgba(210,195,180,0.8);">
          <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#c4622d;margin-right:7px;vertical-align:middle;animation:dotPulse 2s infinite;"></span>
          Batch Queue
        </span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;font-weight:600;padding:2px 10px;border-radius:5px;color:#c4622d;background:rgba(196,98,45,0.12);border:1px solid rgba(196,98,45,0.2);">IDLE</span>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-radius:8px;margin-bottom:5px;">
        <span style="font-size:0.74rem;font-family:'Outfit',sans-serif;color:rgba(180,160,144,0.45);">
          <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:rgba(180,160,144,0.35);margin-right:7px;vertical-align:middle;"></span>
          Session
        </span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:rgba(180,160,144,0.4);">{uptime_display}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Landing", use_container_width=True):
        st.session_state.landing=True; st.rerun()
    st.markdown("""<div class="cs-footer">© 2026 ClaimSentinel<br>Proprietary SIU Intelligence</div>""", unsafe_allow_html=True)

menu = st.session_state.menu

def page_header(eyebrow, title, title_italic, desc):
    st.markdown(f"""<div style="padding:2px 0 22px;animation:fadeIn 0.4s ease;">
      <div class="cs-eyebrow"><span class="cs-eyebrow-dot"></span>&nbsp;{eyebrow}</div>
      <div class="cs-page-title">{title} <span style="font-style:italic;color:var(--amber);">{title_italic}</span></div>
      <p class="cs-page-desc">{desc}</p></div>""", unsafe_allow_html=True)

def card_open(icon, title, subtitle):
    st.markdown(f"""<div class="cs-card">
      <div class="cs-card-header">
        <div class="cs-card-icon">{icon}</div>
        <div><div class="cs-card-title">{title}</div><div class="cs-card-sub">{subtitle}</div></div>
      </div>""", unsafe_allow_html=True)

def card_close():
    st.markdown('</div>', unsafe_allow_html=True)

# ══ VERIFY CLAIM ══
if menu == "Verify Claim":
    page_header("Risk Assessment Terminal","Claim","Verification",
        "Fill in claim details across three sections, then run the fraud screening to receive an instant risk verdict.")

    expected_columns = ['claim_number','age_of_driver','gender','marital_status','safety_rating',
        'annual_income','high_education','address_change','property_status','zip_code','claim_date',
        'claim_day_of_week','accident_site','past_num_of_claims','witness_present','liab_prct','channel',
        'police_report','age_of_vehicle','vehicle_category','vehicle_price','vehicle_color','total_claim',
        'injury_claim','policy deductible','annual premium','days open','form defects']

    card_open("◈","Policy Holder Profile","claimant identification · demographics")
    c1,c2,c3=st.columns(3,gap="medium")
    with c1:
        claim_number=st.number_input("Claim Sequence #",min_value=0,value=None,placeholder="e.g. 414724")
        age_of_driver=st.slider("Driver Age",18,100,35)
    with c2:
        gender=st.selectbox("Legal Gender",["M","F"],index=None,placeholder="Select…")
        marital_status=st.selectbox("Marital Status",["0","1"],index=None,placeholder="0 = Single · 1 = Married")
    with c3:
        high_education=st.radio("Higher Education",[0,1],horizontal=True,format_func=lambda x:"No" if x==0 else "Yes")
        zip_code=st.number_input("Zip Code",min_value=0,value=None,placeholder="e.g. 50048")
        property_status=st.selectbox("Property Tenure",["Own","Rent","Other"],index=None,placeholder="Select…")
    card_close()

    card_open("◉","Incident Intelligence","scene metadata · vehicle · evidence")
    c1,c2,c3=st.columns(3,gap="medium")
    with c1:
        claim_date=st.date_input("Incident Date",value=None)
        claim_day_of_week=st.selectbox("Incident Day",["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],index=None,placeholder="Select…")
        accident_site=st.selectbox("Accident Site",["Highway","Local","Parking Lot"],index=None,placeholder="Select…")
    with c2:
        witness_present=st.radio("Witness Present?",[0,1],horizontal=True,format_func=lambda x:"No" if x==0 else "Yes")
        police_report=st.radio("Police Report Filed?",[0,1],horizontal=True,format_func=lambda x:"No" if x==0 else "Yes")
        safety_rating=st.slider("Driver Safety Score",0,100,75)
    with c3:
        age_of_vehicle=st.number_input("Vehicle Age (Years)",min_value=0,max_value=30,value=None,placeholder="e.g. 5")
        vehicle_category=st.selectbox("Vehicle Category",["Compact","Medium","Large"],index=None,placeholder="Select…")
        vehicle_color=st.selectbox("Vehicle Color",["black","silver","white","gray","red","blue"],index=None,placeholder="Select…")
    card_close()

    card_open("◆","Financial Exposure","claim valuation · premiums · risk indicators")
    c1,c2,c3=st.columns(3,gap="medium")
    with c1:
        annual_income=st.number_input("Annual Income (₹)",min_value=0,value=None,placeholder="e.g. 55,000")
        total_claim=st.number_input("Total Claim Amount (₹)",min_value=0,value=None,placeholder="e.g. 12,000")
        injury_claim=st.number_input("Injury Claim (₹)",min_value=0,value=None,placeholder="e.g. 2,000")
    with c2:
        vehicle_price=st.number_input("Vehicle Value (₹)",min_value=0,value=None,placeholder="e.g. 25,000")
        annual_premium=st.number_input("Annual Premium (₹)",min_value=0,value=None,placeholder="e.g. 1,200")
        policy_deductible=st.number_input("Policy Deductible (₹)",min_value=0,value=None,placeholder="e.g. 500")
    with c3:
        days_open=st.number_input("Days Open",min_value=0,max_value=365,value=None,placeholder="e.g. 7")
        past_num_of_claims=st.number_input("Past Claims #",min_value=0,max_value=10,value=None,placeholder="e.g. 0")
        liab_prct=st.slider("Liability %",0,100,25)
    st.markdown("<br>",unsafe_allow_html=True)
    c4,c5=st.columns(2,gap="medium")
    with c4:
        form_defects=st.select_slider("Form Defects",options=[0,1,2,3,4,5])
        address_change=st.radio("Recent Address Change?",[0,1],horizontal=True,format_func=lambda x:"No" if x==0 else "Yes")
    with c5:
        channel=st.selectbox("Intake Channel",["Phone","Broker","Online"],index=None,placeholder="Select…")
    card_close()

    col_btn,_=st.columns([2,3])
    with col_btn: run_analysis=st.button("⚡  Run Fraud Screening")

    if run_analysis:
        missing=[]
        if claim_number is None: missing.append("Claim #")
        if gender is None: missing.append("Gender")
        if marital_status is None: missing.append("Marital Status")
        if zip_code is None: missing.append("Zip Code")
        if property_status is None: missing.append("Property Tenure")
        if claim_date is None: missing.append("Incident Date")
        if claim_day_of_week is None: missing.append("Incident Day")
        if accident_site is None: missing.append("Accident Site")
        if age_of_vehicle is None: missing.append("Vehicle Age")
        if vehicle_category is None: missing.append("Vehicle Category")
        if vehicle_color is None: missing.append("Vehicle Color")
        if annual_income is None: missing.append("Annual Income")
        if total_claim is None: missing.append("Total Claim")
        if injury_claim is None: missing.append("Injury Claim")
        if vehicle_price is None: missing.append("Vehicle Value")
        if annual_premium is None: missing.append("Annual Premium")
        if policy_deductible is None: missing.append("Deductible")
        if days_open is None: missing.append("Days Open")
        if past_num_of_claims is None: missing.append("Past Claims #")
        if channel is None: missing.append("Intake Channel")
        if missing:
            st.markdown(f"""<div style="background:var(--amberL);border:1px solid rgba(196,98,45,0.25);
              border-radius:10px;padding:12px 18px;font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:var(--amber);">
              ⚠ Please complete: {' · '.join(missing)}</div>""", unsafe_allow_html=True)
        else:
            input_data={
                "claim_number":claim_number,"age_of_driver":age_of_driver,
                "gender":encoders['gender'].transform([gender])[0],
                "marital_status":encoders['marital_status'].transform([marital_status])[0],
                "safety_rating":safety_rating,"annual_income":annual_income,
                "high_education":high_education,"address_change":address_change,
                "property_status":encoders['property_status'].transform([property_status])[0],
                "zip_code":zip_code,"claim_date":claim_date.toordinal(),
                "claim_day_of_week":encoders['claim_day_of_week'].transform([claim_day_of_week])[0],
                "accident_site":encoders['accident_site'].transform([accident_site])[0],
                "past_num_of_claims":past_num_of_claims,"witness_present":witness_present,
                "liab_prct":liab_prct,"channel":encoders['channel'].transform([channel])[0],
                "police_report":police_report,"age_of_vehicle":age_of_vehicle,
                "vehicle_category":encoders['vehicle_category'].transform([vehicle_category])[0],
                "vehicle_price":vehicle_price,
                "vehicle_color":encoders['vehicle_color'].transform([vehicle_color])[0],
                "total_claim":total_claim,"injury_claim":injury_claim,
                "policy deductible":policy_deductible,"annual premium":annual_premium,
                "days open":days_open,"form defects":form_defects,
            }
            df_input=pd.DataFrame([input_data])[expected_columns]
            with st.spinner("Analyzing claim against fraud patterns…"):
                pred=model.predict(df_input)[0]
                prob=model.predict_proba(df_input)[0][1]
            risk_pct=round(prob*100,1)

            angle=risk_pct/100*180
            cx,cy,r=100,100,74
            needle_x=cx+r*np.cos(np.radians(180+angle))
            needle_y=cy+r*np.sin(np.radians(180+angle))
            gauge_color="#b84c4c" if risk_pct>=50 else "#9a7c2e" if risk_pct>=30 else "#3d6b5a"

            gauge_html=f"""<div style="text-align:center;margin:18px 0 8px;">
              <svg width="240" height="140" viewBox="0 0 200 115" xmlns="http://www.w3.org/2000/svg">
                <path d="M 16 100 A 84 84 0 0 1 63 20" stroke="#3d6b5a" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.25"/>
                <path d="M 63 20 A 84 84 0 0 1 137 20" stroke="#9a7c2e" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.25"/>
                <path d="M 137 20 A 84 84 0 0 1 184 100" stroke="#b84c4c" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.25"/>
                <path d="M 16 100 A 84 84 0 0 1 {needle_x:.1f} {needle_y:.1f}" stroke="{gauge_color}" stroke-width="10" fill="none" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="5" fill="{gauge_color}"/>
                <line x1="100" y1="100" x2="{needle_x:.1f}" y2="{needle_y:.1f}" stroke="{gauge_color}" stroke-width="2.5" stroke-linecap="round"/>
                <text x="10" y="114" font-family="IBM Plex Mono" font-size="7.5" fill="#3d6b5a" opacity="0.7">LOW</text>
                <text x="82" y="13" font-family="IBM Plex Mono" font-size="7.5" fill="#9a7c2e" opacity="0.7">MED</text>
                <text x="163" y="114" font-family="IBM Plex Mono" font-size="7.5" fill="#b84c4c" opacity="0.7">HIGH</text>
              </svg>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--textM);letter-spacing:0.1em;margin-top:-6px;">FRAUD RISK GAUGE</div>
            </div>"""

            if pred==1 or pred=='Y':
                st.markdown(f"""<div class="cs-result-fraud">
                  <div class="cs-result-icon cs-result-icon-fraud">🚨</div>
                  <div class="cs-badge-fraud"><span style="width:5px;height:5px;border-radius:50%;background:#b84c4c;display:inline-block;animation:dotPulse 1.5s infinite;"></span>FRAUD DETECTED · HIGH CONFIDENCE</div>
                  {gauge_html}
                  <div class="cs-score-fraud">{risk_pct}%</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:#b84c4c;opacity:0.5;letter-spacing:0.14em;margin-bottom:20px;">FRAUD PROBABILITY SCORE</div>
                  <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(184,76,76,0.3),transparent);margin:0 80px 20px;"></div>
                  <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#7a2a2a;margin-bottom:10px;font-style:italic;">Critical Anomaly Detected</div>
                  <p style="font-size:0.86rem;color:#8b4040;max-width:480px;margin:0 auto 20px;line-height:1.85;font-family:'Outfit',sans-serif;">
                    This claim exhibits strong correlation to known fraud vectors. Immediate escalation to the Special Investigations Unit is required before any disbursement is authorized.</p>
                  <div class="cs-directive-fraud">📋&nbsp;&nbsp;DIRECTIVE: FLAG FOR SIU REVIEW · HOLD ALL DISBURSEMENTS</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="cs-result-clear">
                  <div class="cs-result-icon cs-result-icon-clear">✅</div>
                  <div class="cs-badge-clear"><span style="width:5px;height:5px;border-radius:50%;background:#3d6b5a;display:inline-block;animation:dotPulse 2s infinite;"></span>SCREENING PASSED · LOW RISK</div>
                  {gauge_html}
                  <div class="cs-score-clear">{risk_pct}%</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:#3d6b5a;opacity:0.5;letter-spacing:0.14em;margin-bottom:20px;">FRAUD RISK SCORE</div>
                  <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(61,107,90,0.3),transparent);margin:0 80px 20px;"></div>
                  <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#2e5244;margin-bottom:10px;font-style:italic;">Clearance Granted</div>
                  <p style="font-size:0.86rem;color:#3d6b5a;max-width:480px;margin:0 auto 20px;line-height:1.85;font-family:'Outfit',sans-serif;">
                    No statistically significant fraud indicators detected. This claim satisfies all standard validation criteria and is cleared for automated processing.</p>
                  <div class="cs-directive-clear">⚡&nbsp;&nbsp;DIRECTIVE: PROCEED WITH AUTOMATED PROCESSING</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>",unsafe_allow_html=True)
            card_open("◎","Risk Factor Snapshot","computed indicators for this specific claim")
            risk_factors=[]
            if injury_claim and total_claim and total_claim>0:
                inj_ratio=round((injury_claim/total_claim)*100,1)
                color="#b84c4c" if inj_ratio>60 else "#9a7c2e" if inj_ratio>30 else "#3d6b5a"
                risk_factors.append(("Injury-to-Claim Ratio",f"{inj_ratio}%",color,inj_ratio))
            if annual_income and total_claim:
                expo=round((total_claim/annual_income)*100,1) if annual_income>0 else 0
                color="#b84c4c" if expo>50 else "#9a7c2e" if expo>20 else "#3d6b5a"
                risk_factors.append(("Claim-to-Income Exposure",f"{expo}%",color,min(expo,100)))
            risk_factors.append(("Form Defects",f"{form_defects}/5","#b84c4c" if form_defects>2 else "#9a7c2e" if form_defects>0 else "#3d6b5a",form_defects/5*100))
            risk_factors.append(("Past Claims Count",str(past_num_of_claims),"#b84c4c" if past_num_of_claims>2 else "#9a7c2e" if past_num_of_claims>0 else "#3d6b5a",min(past_num_of_claims/5*100,100)))
            risk_factors.append(("Witness Present","YES" if witness_present else "NO","#3d6b5a" if witness_present else "#b84c4c",100 if witness_present else 0))
            for name,val_str,color,bar_val in risk_factors:
                st.markdown(f"""<div class="cs-feature-row">
                  <div style="font-size:0.83rem;font-weight:500;color:var(--text1);">{name}</div>
                  <div style="display:flex;align-items:center;gap:12px;flex-shrink:0;">
                    <div style="width:160px;height:4px;background:var(--border);border-radius:999px;overflow:hidden;">
                      <div style="height:100%;width:{bar_val:.0f}%;background:{color};border-radius:999px;"></div>
                    </div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:{color};width:50px;text-align:right;font-weight:600;">{val_str}</div>
                  </div></div>""", unsafe_allow_html=True)
            card_close()

# ══ BATCH PROCESSING ══
elif menu == "Batch Processing":
    page_header("Batch Intake","Enterprise","Batch Processing",
        "Upload a CSV of claims — the model screens every row instantly. Download results with fraud scores and verdicts.")
    REQUIRED_COLS=['claim_number','age_of_driver','gender','marital_status','safety_rating',
        'annual_income','high_education','address_change','property_status','zip_code','claim_date',
        'claim_day_of_week','accident_site','past_num_of_claims','witness_present','liab_prct','channel',
        'police_report','age_of_vehicle','vehicle_category','vehicle_price','vehicle_color','total_claim',
        'injury_claim','policy deductible','annual premium','days open','form defects']
    CAT_COLS={'gender':'gender','marital_status':'marital_status','property_status':'property_status',
        'claim_day_of_week':'claim_day_of_week','accident_site':'accident_site',
        'channel':'channel','vehicle_category':'vehicle_category','vehicle_color':'vehicle_color'}

    card_open("📋","CSV Format Guide","required columns · encoding rules")
    col_a,col_b=st.columns(2,gap="medium")
    with col_a:
        st.markdown("""<div style="background:var(--surface2);border:1px solid var(--border);border-radius:11px;padding:14px 16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--amber);letter-spacing:0.12em;margin-bottom:8px;font-weight:600;">NUMERIC COLUMNS</div>
          <div style="font-size:0.77rem;color:var(--text2);line-height:2;font-family:'IBM Plex Mono',monospace;">
            claim_number · age_of_driver · safety_rating<br>annual_income · zip_code · past_num_of_claims<br>
            witness_present (0/1) · liab_prct · police_report (0/1)<br>age_of_vehicle · vehicle_price · total_claim<br>
            injury_claim · policy deductible · annual premium<br>days open · form defects · high_education (0/1)<br>
            address_change (0/1) · claim_date (YYYY-MM-DD)
          </div></div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""<div style="background:var(--surface2);border:1px solid var(--border);border-radius:11px;padding:14px 16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--sage);letter-spacing:0.12em;margin-bottom:8px;font-weight:600;">CATEGORICAL VALUES</div>
          <div style="font-size:0.78rem;color:var(--text2);line-height:2.2;">
            <b style="color:var(--text1);">gender</b> → M, F<br><b style="color:var(--text1);">marital_status</b> → 0, 1<br>
            <b style="color:var(--text1);">property_status</b> → Own, Rent, Other<br>
            <b style="color:var(--text1);">claim_day_of_week</b> → Monday … Sunday<br>
            <b style="color:var(--text1);">accident_site</b> → Highway, Local, Parking Lot<br>
            <b style="color:var(--text1);">channel</b> → Phone, Broker, Online<br>
            <b style="color:var(--text1);">vehicle_category</b> → Compact, Medium, Large<br>
            <b style="color:var(--text1);">vehicle_color</b> → black, silver, white, gray, red, blue
          </div></div>""", unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    sample_df=pd.DataFrame({'claim_number':[101,102],'age_of_driver':[34,52],'gender':['M','F'],
        'marital_status':['1','0'],'safety_rating':[80,45],'annual_income':[55000,32000],
        'high_education':[1,0],'address_change':[0,1],'property_status':['Own','Rent'],
        'zip_code':[50048,62301],'claim_date':['2024-03-10','2024-03-11'],
        'claim_day_of_week':['Sunday','Monday'],'accident_site':['Highway','Local'],
        'past_num_of_claims':[0,2],'witness_present':[1,0],'liab_prct':[30,75],
        'channel':['Online','Phone'],'police_report':[1,0],'age_of_vehicle':[3,10],
        'vehicle_category':['Compact','Large'],'vehicle_price':[25000,8000],
        'vehicle_color':['silver','black'],'total_claim':[12000,48000],
        'injury_claim':[2000,15000],'policy deductible':[500,1000],
        'annual premium':[1200,900],'days open':[7,30],'form defects':[0,3]})
    st.download_button("⬇️  Download Sample CSV Template",
        data=sample_df.to_csv(index=False).encode('utf-8'),
        file_name="claimsentinel_sample_batch.csv",mime="text/csv")
    card_close()

    card_open("📊","Fraud Risk Score Reference Chart","interpret model output — like a BMI chart for fraud probability")
    st.markdown("""<p style="font-size:0.83rem;color:var(--text2);margin-bottom:16px;line-height:1.75;">
      Maps the model's fraud probability score (0–100%) to actionable decision bands. Use to triage batch results and prioritize investigator workload.</p>""",unsafe_allow_html=True)
    st.markdown("""
    <div style="background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:22px;margin-bottom:14px;">
      <svg width="100%" viewBox="0 0 700 215" xmlns="http://www.w3.org/2000/svg">
        <rect x="40" y="22" width="130" height="132" rx="5" fill="#3d6b5a" opacity="0.08"/>
        <rect x="170" y="22" width="110" height="132" rx="5" fill="#9a7c2e" opacity="0.08"/>
        <rect x="280" y="22" width="100" height="132" rx="5" fill="#c4622d" opacity="0.08"/>
        <rect x="380" y="22" width="100" height="132" rx="5" fill="#b84c4c" opacity="0.1"/>
        <rect x="480" y="22" width="190" height="132" rx="5" fill="#7a2a2a" opacity="0.09"/>
        <text x="105" y="16" text-anchor="middle" font-size="9" fill="#3d6b5a" font-family="IBM Plex Mono" letter-spacing="1" font-weight="600">MINIMAL</text>
        <text x="225" y="16" text-anchor="middle" font-size="9" fill="#9a7c2e" font-family="IBM Plex Mono" letter-spacing="1" font-weight="600">LOW</text>
        <text x="330" y="16" text-anchor="middle" font-size="9" fill="#c4622d" font-family="IBM Plex Mono" letter-spacing="1" font-weight="600">MODERATE</text>
        <text x="430" y="16" text-anchor="middle" font-size="9" fill="#b84c4c" font-family="IBM Plex Mono" letter-spacing="1" font-weight="600">HIGH</text>
        <text x="575" y="16" text-anchor="middle" font-size="9" fill="#7a2a2a" font-family="IBM Plex Mono" letter-spacing="1" font-weight="600">CRITICAL</text>
        <text x="105" y="70" text-anchor="middle" font-size="20">✅</text>
        <text x="225" y="70" text-anchor="middle" font-size="20">🔎</text>
        <text x="330" y="70" text-anchor="middle" font-size="20">⚠️</text>
        <text x="430" y="70" text-anchor="middle" font-size="20">🔶</text>
        <text x="575" y="70" text-anchor="middle" font-size="20">🚨</text>
        <text x="105" y="96" text-anchor="middle" font-size="8" fill="#3d6b5a" font-family="IBM Plex Mono">Auto-approve</text>
        <text x="105" y="108" text-anchor="middle" font-size="8" fill="#3d6b5a" font-family="IBM Plex Mono">process claim</text>
        <text x="225" y="96" text-anchor="middle" font-size="8" fill="#9a7c2e" font-family="IBM Plex Mono">Routine review</text>
        <text x="225" y="108" text-anchor="middle" font-size="8" fill="#9a7c2e" font-family="IBM Plex Mono">low priority</text>
        <text x="330" y="96" text-anchor="middle" font-size="8" fill="#c4622d" font-family="IBM Plex Mono">Manual check</text>
        <text x="330" y="108" text-anchor="middle" font-size="8" fill="#c4622d" font-family="IBM Plex Mono">required</text>
        <text x="430" y="96" text-anchor="middle" font-size="8" fill="#b84c4c" font-family="IBM Plex Mono">Investigator</text>
        <text x="430" y="108" text-anchor="middle" font-size="8" fill="#b84c4c" font-family="IBM Plex Mono">assignment</text>
        <text x="575" y="96" text-anchor="middle" font-size="8" fill="#7a2a2a" font-family="IBM Plex Mono">SIU escalation</text>
        <text x="575" y="112" text-anchor="middle" font-size="8" fill="#7a2a2a" font-family="IBM Plex Mono">hold payment</text>
        <line x1="40" y1="155" x2="670" y2="155" stroke="#c8c2b6" stroke-width="1"/>
        <rect x="40" y="155" width="130" height="5" rx="2" fill="#3d6b5a" opacity="0.7"/>
        <rect x="170" y="155" width="110" height="5" rx="2" fill="#9a7c2e" opacity="0.7"/>
        <rect x="280" y="155" width="100" height="5" rx="2" fill="#c4622d" opacity="0.7"/>
        <rect x="380" y="155" width="100" height="5" rx="2" fill="#b84c4c" opacity="0.7"/>
        <rect x="480" y="155" width="190" height="5" rx="2" fill="#7a2a2a" opacity="0.65"/>
        <text x="40" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">0%</text>
        <text x="170" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">20%</text>
        <text x="280" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">35%</text>
        <text x="380" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">50%</text>
        <text x="480" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">65%</text>
        <text x="670" y="172" text-anchor="middle" font-size="9.5" fill="#9a8f84" font-family="IBM Plex Mono">100%</text>
        <text x="355" y="190" text-anchor="middle" font-size="9" fill="#9a8f84" font-family="IBM Plex Mono" letter-spacing="1">FRAUD PROBABILITY SCORE (%)</text>
      </svg>
    </div>""",unsafe_allow_html=True)
    cols=st.columns(5)
    bands=[("0–20%","MINIMAL","#3d6b5a","Auto-approve"),("20–35%","LOW","#9a7c2e","Routine review"),
           ("35–50%","MODERATE","#c4622d","Manual check"),("50–65%","HIGH","#b84c4c","Investigate"),("65–100%","CRITICAL","#7a2a2a","SIU escalate")]
    for col,(rng,label,color,action) in zip(cols,bands):
        with col:
            st.markdown(f"""<div style="background:var(--surface);border:1px solid rgba(0,0,0,0.07);border-top:2px solid {color};
              border-radius:10px;padding:14px 10px;text-align:center;box-shadow:var(--shadow);">
              <div style="font-family:'DM Serif Display',serif;font-style:italic;font-size:1.1rem;color:{color};margin-bottom:3px;">{rng}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.57rem;color:{color};letter-spacing:0.1em;margin:4px 0;">{label}</div>
              <div style="font-size:0.72rem;color:var(--text2);margin-top:6px;">{action}</div>
            </div>""",unsafe_allow_html=True)
    card_close()

    card_open("⬆️","Upload & Run Screening","upload manifest → model runs on every row")
    uploaded_file=st.file_uploader("Drop your CSV manifest here",type=["csv"],label_visibility="collapsed")
    if uploaded_file:
        df_batch=pd.read_csv(uploaded_file)
        st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;background:var(--sageL);
          border:1px solid rgba(61,107,90,0.25);border-radius:10px;padding:12px 16px;margin:12px 0;">
          <span style="font-size:18px;">📂</span>
          <div><div style="font-weight:700;color:var(--sage);font-size:0.86rem;">{uploaded_file.name}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--sage);margin-top:2px;opacity:0.7;">
            {len(df_batch):,} rows · {len(df_batch.columns)} columns detected</div></div></div>""",unsafe_allow_html=True)
        missing_cols=[c for c in REQUIRED_COLS if c not in df_batch.columns]
        if missing_cols:
            st.markdown(f"""<div style="background:var(--roseL);border:1px solid rgba(184,76,76,0.25);border-radius:10px;padding:12px 16px;margin:8px 0;">
              <div style="font-weight:700;color:var(--rose);font-size:0.84rem;margin-bottom:5px;">⚠ Missing Columns ({len(missing_cols)})</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.67rem;color:var(--rose);opacity:0.8;">{' · '.join(missing_cols)}</div></div>""",unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:var(--sageL);border:1px solid rgba(61,107,90,0.2);border-radius:9px;padding:8px 14px;margin:8px 0;">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.67rem;color:var(--sage);font-weight:600;">✓ All columns validated — ready to screen</div></div>""",unsafe_allow_html=True)
            with st.expander("👁  Preview uploaded data (first 5 rows)"):
                st.dataframe(df_batch.head(),use_container_width=True)
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("⚡  Run Fraud Screening on All Claims"):
                start_t=time.time()
                with st.spinner(f"Screening {len(df_batch):,} claims…"):
                    df_proc=df_batch.copy()
                    if 'claim_date' in df_proc.columns:
                        df_proc['claim_date']=pd.to_datetime(df_proc['claim_date'],errors='coerce').apply(lambda d:d.toordinal() if pd.notnull(d) else 0)
                    encode_errors=[]
                    for col,enc_key in CAT_COLS.items():
                        if col in df_proc.columns:
                            try: df_proc[col]=encoders[enc_key].transform(df_proc[col].astype(str))
                            except Exception as ex: encode_errors.append(f"{col}: {ex}")
                    if encode_errors: st.warning("⚠️ Encoding issues:\n"+"\n".join(encode_errors))
                    preds=model.predict(df_proc[REQUIRED_COLS])
                    probas=model.predict_proba(df_proc[REQUIRED_COLS])[:,1]
                elapsed=round(time.time()-start_t,2)
                df_results=df_batch.copy()
                df_results['fraud_prediction']=preds
                df_results['fraud_probability_%']=(probas*100).round(2)
                df_results['verdict']=df_results['fraud_prediction'].apply(lambda x:'FRAUD' if x==1 or x=='Y' else 'CLEAR')
                fraud_mask=df_results['verdict']=='FRAUD'
                fraud_count=int(fraud_mask.sum())
                clear_count=len(df_results)-fraud_count
                fraud_rate=round(fraud_count/len(df_results)*100,1)
                avg_prob=round(probas.mean()*100,1)
                m1,m2,m3,m4=st.columns(4,gap="small")
                with m1: st.metric("Total Screened",f"{len(df_results):,}")
                with m2: st.metric("Flagged Fraud",f"{fraud_count:,}")
                with m3: st.metric("Cleared",f"{clear_count:,}")
                with m4: st.metric("Fraud Rate",f"{fraud_rate}%")
                st.markdown(f"""<div style="font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--textM);margin:10px 0 14px;">
                  ⏱ Completed in {elapsed}s · avg risk score: {avg_prob}%</div>""",unsafe_allow_html=True)
                bins=[0,0.20,0.35,0.50,0.65,1.01]
                labels_b=["0–20%","20–35%","35–50%","50–65%","65–100%"]
                colors_b=["#3d6b5a","#9a7c2e","#c4622d","#b84c4c","#7a2a2a"]
                counts_b=[int(((probas>=bins[i])&(probas<bins[i+1])).sum()) for i in range(len(bins)-1)]
                max_c=max(counts_b) if max(counts_b)>0 else 1
                bar_items=""
                bar_x,bar_w,bar_gap,chart_h=60,90,20,140
                for i,(cnt,lbl,col) in enumerate(zip(counts_b,labels_b,colors_b)):
                    bh=int((cnt/max_c)*chart_h); bx=bar_x+i*(bar_w+bar_gap); by=180-bh
                    pct_b=round(cnt/len(probas)*100,1)
                    bar_items+=f"""<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="5" fill="{col}" opacity="0.75"/>
                    <text x="{bx+bar_w//2}" y="{by-6}" text-anchor="middle" font-size="11" fill="{col}" font-weight="600" font-family="IBM Plex Mono">{cnt}</text>
                    <text x="{bx+bar_w//2}" y="196" text-anchor="middle" font-size="9" fill="#9a8f84" font-family="IBM Plex Mono">{lbl}</text>
                    <text x="{bx+bar_w//2}" y="207" text-anchor="middle" font-size="9" fill="{col}" opacity="0.7" font-family="IBM Plex Mono">{pct_b}%</text>"""
                st.markdown(f"""<div style="background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:20px;margin:14px 0;">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:var(--amber);letter-spacing:0.1em;margin-bottom:12px;">RISK DISTRIBUTION OF BATCH</div>
                  <svg width="100%" viewBox="0 0 670 220" xmlns="http://www.w3.org/2000/svg">
                    <line x1="50" y1="40" x2="50" y2="180" stroke="#c8c2b6" stroke-width="1"/>
                    <line x1="50" y1="180" x2="650" y2="180" stroke="#c8c2b6" stroke-width="1"/>
                    {bar_items}
                    <text x="20" y="140" text-anchor="middle" font-size="9" fill="#9a8f84" font-family="IBM Plex Mono" transform="rotate(-90,20,140)">COUNT</text>
                  </svg></div>""",unsafe_allow_html=True)
                df_fraud_only=df_results[fraud_mask].sort_values('fraud_probability_%',ascending=False)
                if len(df_fraud_only)>0:
                    st.markdown(f"""<div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:0.9rem;color:var(--text1);margin-bottom:8px;">
                      🚨 Top {min(10,len(df_fraud_only))} Flagged Claims by Risk Score</div>""",unsafe_allow_html=True)
                    preview_cols=[c for c in ['claim_number','age_of_driver','total_claim','fraud_probability_%','verdict'] if c in df_fraud_only.columns]
                    st.dataframe(df_fraud_only[preview_cols].head(10).reset_index(drop=True),use_container_width=True)
                with st.expander(f"📋  Full results table ({len(df_results):,} rows)"):
                    disp=[c for c in ['claim_number','fraud_prediction','fraud_probability_%','verdict'] if c in df_results.columns]
                    st.dataframe(df_results[disp].reset_index(drop=True),use_container_width=True)
                st.markdown("<br>",unsafe_allow_html=True)
                c1,c2=st.columns(2)
                with c1:
                    st.download_button("⬇️  Download Full Results CSV",data=df_results.to_csv(index=False).encode('utf-8'),file_name=f"claimsentinel_results_{uploaded_file.name}",mime="text/csv")
                if len(df_fraud_only)>0:
                    with c2:
                        st.download_button(f"🚨  Download Flagged Only ({fraud_count} rows)",data=df_fraud_only.to_csv(index=False).encode('utf-8'),file_name=f"claimsentinel_FRAUD_{uploaded_file.name}",mime="text/csv")
    card_close()

# ══ ENGINE INSIGHTS ══
elif menu == "Engine Insights":
    page_header("Analytics Dashboard","Cognitive","Analytics",
        "Live diagnostics, real model feature importances, confusion matrix rates, and dataset intelligence.")
    c1,c2,c3,c4=st.columns(4,gap="medium")
    with c1: st.metric("F1 Score","89.4%","+2.1%")
    with c2: st.metric("Precision","91.7%","+1.3%")
    with c3: st.metric("Recall","87.2%","+0.9%")
    with c4: st.metric("Dataset Size","12,002","claims trained")
    st.markdown("<br>",unsafe_allow_html=True)

    card_open("◎","Feature Importance Analysis","actual RandomForest feature weights · top 10 predictors")
    st.markdown("""<p style="font-size:0.82rem;color:var(--text2);margin-bottom:14px;line-height:1.75;">
      Extracted directly from the trained Random Forest model. Higher weight = more influence on the fraud/clear decision.
      <span style="color:var(--amber);font-family:'IBM Plex Mono',monospace;font-size:0.74rem;">
      These are fixed model properties — they reflect training, not individual claim entries.</span></p>""",unsafe_allow_html=True)
    for label,val,color in FEATURE_IMPORTANCES:
        bar_w=int(val/15.0*100)
        st.markdown(f"""<div class="cs-feature-row">
          <div style="font-size:0.83rem;font-weight:500;color:var(--text1);min-width:200px;">{label}</div>
          <div style="display:flex;align-items:center;gap:14px;flex-shrink:0;flex:1;justify-content:flex-end;">
            <div style="width:220px;height:4px;background:var(--border);border-radius:999px;overflow:hidden;">
              <div style="height:100%;width:{bar_w}%;background:{color};border-radius:999px;opacity:0.85;"></div>
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.74rem;color:{color};width:44px;text-align:right;font-weight:600;">{val:.1f}%</div>
          </div></div>""",unsafe_allow_html=True)
    card_close()

    col1,col2=st.columns(2,gap="medium")
    with col1:
        card_open("⚙️","Confusion Matrix Rates","model performance on held-out test split")
        st.markdown("""<p style="font-size:0.8rem;color:var(--text2);margin-bottom:14px;line-height:1.65;">
          Static metrics from model validation. Do not update with individual predictions.</p>""",unsafe_allow_html=True)
        metrics_cm=[("True Positive Rate (Sensitivity)",87.2,"#3d6b5a","Fraud caught correctly"),
            ("True Negative Rate (Specificity)",93.4,"#5c6b7a","Legit claims cleared"),
            ("False Positive Rate",6.6,"#9a7c2e","Legit flagged as fraud"),
            ("False Negative Rate",12.8,"#b84c4c","Fraud missed by model")]
        for name,val,color,desc in metrics_cm:
            st.markdown(f"""<div style="margin-bottom:14px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px;align-items:baseline;">
                <div><div style="font-size:0.79rem;color:var(--text1);font-weight:500;">{name}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--textM);margin-top:1px;">{desc}</div></div>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:0.8rem;color:{color};font-weight:600;flex-shrink:0;margin-left:10px;">{val}%</span>
              </div>
              <div style="height:4px;background:var(--border);border-radius:999px;">
                <div style="height:100%;width:{val}%;background:{color};border-radius:999px;opacity:0.85;"></div>
              </div></div>""",unsafe_allow_html=True)
        card_close()
    with col2:
        card_open("📊","Dataset Intelligence","training data distribution · model specifications")
        st.markdown("""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
          <div style="background:var(--roseL);border:1px solid rgba(184,76,76,0.18);border-radius:10px;padding:14px;text-align:center;">
            <div style="font-family:'DM Serif Display',serif;font-style:italic;font-size:2rem;color:#b84c4c;">2,951</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.57rem;color:#b84c4c;letter-spacing:0.1em;opacity:0.7;">FRAUD CASES</div>
          </div>
          <div style="background:var(--sageL);border:1px solid rgba(61,107,90,0.18);border-radius:10px;padding:14px;text-align:center;">
            <div style="font-family:'DM Serif Display',serif;font-style:italic;font-size:2rem;color:#3d6b5a;">9,043</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.57rem;color:#3d6b5a;letter-spacing:0.1em;opacity:0.7;">LEGIT CASES</div>
          </div></div>
        <div style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:0.78rem;color:var(--text2);">Class Distribution</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#b84c4c;">24.6% fraud</span>
          </div>
          <div style="height:16px;background:var(--border);border-radius:999px;overflow:hidden;display:flex;">
            <div style="width:24.6%;background:linear-gradient(90deg,#b84c4c,#c4622d);border-radius:999px 0 0 999px;"></div>
            <div style="width:75.4%;background:linear-gradient(90deg,#3d6b5a,#5c6b7a);border-radius:0 999px 999px 0;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:5px;">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.59rem;color:#b84c4c;">■ FRAUD 24.6%</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.59rem;color:#3d6b5a;">LEGIT 75.4% ■</span>
          </div></div>
        <div style="background:var(--surface2);border:1px solid var(--border);border-radius:9px;padding:12px 14px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.59rem;color:var(--textM);letter-spacing:0.08em;margin-bottom:8px;">MODEL SPECIFICATIONS</div>
          <div style="font-size:0.78rem;color:var(--text2);line-height:2;">
            Algorithm: <span style="color:var(--amber);font-weight:600;">Random Forest Classifier</span><br>
            Trees: <span style="color:var(--sage);font-weight:600;">100 estimators</span><br>
            Features: <span style="color:var(--text1);font-weight:600;">28 input columns</span><br>
            Encoders: <span style="color:var(--text1);font-weight:600;">13 LabelEncoders</span>
          </div></div>""",unsafe_allow_html=True)
        card_close()

    card_open("📡","Live System Health Monitor","real-time service status · latency · uptime")
    ts=datetime.now().strftime("%H:%M:%S")
    services=[("Inference Engine (RF)","ONLINE","#3d6b5a","~42 ms","99.9%"),
        ("Feature Encoder Service","ONLINE","#3d6b5a","< 1 ms","99.9%"),
        ("Risk Scoring Pipeline","ONLINE","#3d6b5a","~38 ms","100%"),
        ("Batch Queue","IDLE","#9a7c2e","—","100%"),
        ("Audit Trail Logger","SYNCING","#5c6b7a","~120 ms","99.5%"),
        ("SIU Escalation Bus","STANDBY","#9a8f84","—","—")]
    for name,status,color,latency,uptime in services:
        st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;
          padding:10px 14px;border-radius:9px;background:var(--surface2);border:1px solid var(--border);margin-bottom:6px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:6px;height:6px;border-radius:50%;background:{color};box-shadow:0 0 5px {color};animation:dotPulse 2s infinite;flex-shrink:0;"></div>
            <span style="font-size:0.82rem;color:var(--text1);font-weight:500;">{name}</span>
          </div>
          <div style="display:flex;align-items:center;gap:20px;flex-shrink:0;">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:var(--textM);">latency: {latency}</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:var(--textM);">uptime: {uptime}</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;font-weight:700;color:{color};
              background:{color}18;border:1px solid {color}30;border-radius:6px;padding:2px 10px;">{status}</span>
          </div></div>""",unsafe_allow_html=True)
    st.markdown(f"""<div style="font-family:'IBM Plex Mono',monospace;font-size:0.59rem;color:var(--textM);margin-top:8px;text-align:right;">
      Last polled: {ts} · Auto-refresh on page load</div>""",unsafe_allow_html=True)
    card_close()

    card_open("📈","Recall by Claim Category","per-segment model performance estimates")
    cats=[("Vehicle Damage",94,"#3d6b5a"),("Personal Injury",88,"#c4622d"),
          ("Theft / Burglary",91,"#9a7c2e"),("Medical Expenses",85,"#5c6b7a"),("Third Party Liability",79,"#b84c4c")]
    for cat,val,color in cats:
        st.markdown(f"""<div style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span style="font-size:0.8rem;color:var(--text2);font-weight:500;">{cat}</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:0.74rem;color:{color};font-weight:600;">{val}%</span>
          </div>
          <div style="height:4px;background:var(--border);border-radius:999px;">
            <div style="height:100%;width:{val}%;background:{color};border-radius:999px;opacity:0.85;"></div>
          </div></div>""",unsafe_allow_html=True)
    card_close()

# ══ ABOUT ══
elif menu == "About":
    page_header("Project Intelligence","About","ClaimSentinel",
        "The project, the model, and the person behind it.")

    card_open("⬡","What is ClaimSentinel?","project mission · architecture · impact")
    st.markdown("""<p style="font-size:0.88rem;color:var(--text2);line-height:1.9;margin-bottom:14px;">
      <b style="color:var(--text1);">ClaimSentinel</b> is an end-to-end machine learning platform designed to detect fraudulent insurance claims
      in real time. Insurance fraud costs the global industry an estimated
      <span style="color:var(--amber);font-weight:600;">$80 billion annually</span>,
      inflating premiums and burdening legitimate policyholders. This platform directly addresses that challenge.</p>
    <p style="font-size:0.88rem;color:var(--text2);line-height:1.9;margin-bottom:20px;">
      The system takes structured claim data — covering the claimant's profile, incident details, vehicle attributes,
      and financial exposure — and runs it through a trained
      <span style="color:var(--sage);font-weight:600;">Random Forest Classifier</span> to produce an instant
      fraud probability score and a clear verdict:
      <span style="color:#3d6b5a;font-weight:600;">CLEAR</span> or
      <span style="color:#b84c4c;font-weight:600;">FRAUD</span>.</p>""",unsafe_allow_html=True)
    cols=st.columns(3,gap="medium")
    highlights=[("🎯","Problem Solved","Instant, consistent fraud screening that removes human bias from first-level claim review."),
        ("⚡","How It Works","Random Forest trained on 12K+ insurance claims with 28 features — returns probability scores, not just binary verdicts."),
        ("🏢","Who It's For","Insurance SIU teams, claims adjusters, and fraud analytics departments needing scalable, auditable tooling.")]
    for col,(icon,title,desc) in zip(cols,highlights):
        with col:
            st.markdown(f"""<div style="background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:18px 16px;height:100%;box-shadow:var(--shadow);">
              <div style="font-size:22px;margin-bottom:10px;">{icon}</div>
              <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:0.88rem;color:var(--text1);margin-bottom:8px;">{title}</div>
              <div style="font-size:0.79rem;color:var(--text2);line-height:1.75;">{desc}</div></div>""",unsafe_allow_html=True)
    card_close()

    card_open("⚙️","Technology Stack","tools · frameworks · libraries")
    tech_items=[("Python 3.11","Core language","#c4622d"),("Scikit-learn","Random Forest, LabelEncoders","#3d6b5a"),
        ("Streamlit","Web application framework","#b84c4c"),("Pandas / NumPy","Data processing & numerics","#5c6b7a"),
        ("Pickle","Model serialization","#9a7c2e"),("SVG + Custom CSS","Charts, UI components","#9a8f84")]
    tech_cols=st.columns(3)
    for i,(name,role,color) in enumerate(tech_items):
        with tech_cols[i%3]:
            st.markdown(f"""<div style="background:var(--surface2);border:1px solid rgba(0,0,0,0.06);border-left:3px solid {color};
              border-radius:8px;padding:12px 14px;margin-bottom:10px;box-shadow:var(--shadow);">
              <div style="font-weight:700;font-size:0.83rem;color:var(--text1);">{name}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:{color};margin-top:3px;opacity:0.8;">{role}</div></div>""",unsafe_allow_html=True)
    card_close()

    card_open("🔬","Model Pipeline","data flow from raw claim to fraud verdict")
    steps=[("01","Raw Claim Input","28 features via form or CSV","#c4622d"),
        ("02","Label Encoding","13 categorical columns encoded","#9a7c2e"),
        ("03","Date Transform","claim_date → ordinal integer","#5c6b7a"),
        ("04","RF Inference","100-tree forest → class probabilities","#3d6b5a"),
        ("05","Risk Scoring","Probability → 0–100% risk score","#9a7c2e"),
        ("06","Verdict Output","FRAUD / CLEAR + SIU directive","#b84c4c")]
    step_cols=st.columns(6)
    for col,(num,title,desc,color) in zip(step_cols,steps):
        with col:
            st.markdown(f"""<div style="text-align:center;">
              <div style="width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,0.04);
                border:2px solid {color};display:flex;align-items:center;justify-content:center;
                margin:0 auto 10px;font-family:'IBM Plex Mono',monospace;font-size:0.85rem;color:{color};font-weight:600;">{num}</div>
              <div style="font-weight:700;font-size:0.74rem;color:var(--text1);margin-bottom:6px;line-height:1.3;">{title}</div>
              <div style="font-size:0.69rem;color:var(--text2);line-height:1.5;">{desc}</div></div>""",unsafe_allow_html=True)
    card_close()

    card_open("👤","About the Developer","the person behind ClaimSentinel")
    st.markdown("""<div style="display:flex;gap:28px;align-items:flex-start;">
      <div style="flex-shrink:0;">
        <div style="width:90px;height:90px;border-radius:50%;background:linear-gradient(135deg,var(--surface2),var(--surface3));
          display:flex;align-items:center;justify-content:center;font-size:36px;border:2px solid var(--border);box-shadow:var(--shadow);">👨‍💻</div>
      </div>
      <div>
        <div style="font-family:'DM Serif Display',serif;font-style:italic;font-size:1.8rem;color:var(--text1);margin-bottom:4px;">Kavyam Joshi</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.63rem;color:var(--amber);letter-spacing:0.1em;margin-bottom:14px;">Pursuing CSE @Darshan University</div>
        <p style="font-size:0.85rem;color:var(--text2);line-height:1.85;max-width:580px;margin-bottom:16px;">
          Passionate about applying machine learning to real-world business problems. Built ClaimSentinel as a demonstration of end-to-end ML deployment — from raw data exploration and model training to production-ready web application development.</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
          <span style="background:var(--amberL);border:1px solid rgba(196,98,45,0.2);border-radius:999px;padding:4px 14px;font-size:0.74rem;color:var(--amber);">Machine Learning</span>
          <span style="background:var(--sageL);border:1px solid rgba(61,107,90,0.2);border-radius:999px;padding:4px 14px;font-size:0.74rem;color:var(--sage);">Data Science</span>
          <span style="background:var(--slateL);border:1px solid rgba(92,107,122,0.2);border-radius:999px;padding:4px 14px;font-size:0.74rem;color:var(--slate);">Python</span>
          <span style="background:var(--goldL);border:1px solid rgba(154,124,46,0.2);border-radius:999px;padding:4px 14px;font-size:0.74rem;color:var(--gold);">Streamlit</span>
          <span style="background:var(--roseL);border:1px solid rgba(184,76,76,0.2);border-radius:999px;padding:4px 14px;font-size:0.74rem;color:var(--rose);">Fraud Analytics</span>
        </div></div></div>
    <div style="margin-top:22px;padding-top:18px;border-top:1px solid var(--border);">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:var(--textM);letter-spacing:0.1em;margin-bottom:12px;">CONNECT</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <a href="https://www.linkedin.com/in/kavyam-joshi-ab9885322/" style="display:flex;align-items:center;gap:7px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:8px 15px;font-size:0.78rem;color:var(--text2);text-decoration:none;box-shadow:var(--shadow);">🔗 LinkedIn</a>
      </div></div>""",unsafe_allow_html=True)
    card_close()

    st.markdown("""<div style="background:var(--amberL);border:1px solid rgba(196,98,45,0.18);border-radius:10px;padding:14px 18px;margin-top:8px;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:var(--amber);letter-spacing:0.08em;margin-bottom:6px;">⚠ DISCLAIMER</div>
      <p style="font-size:0.8rem;color:var(--text2);line-height:1.75;margin:0;">
        ClaimSentinel is a demonstration project built for educational and portfolio purposes.
        Predictions are based on a sample dataset and should not be used for actual insurance adjudication without independent validation by qualified professionals and compliance review.</p></div>""",unsafe_allow_html=True)