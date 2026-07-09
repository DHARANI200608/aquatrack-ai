import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import warnings
import sqlite3
import hashlib
import os
from datetime import datetime
from fpdf import FPDF
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Waterborne Disease EWS", page_icon="💧",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;}
.stApp{background-color:#020d18;}
.stSlider>label{color:#ffffff !important;font-size:14px !important;font-weight:600 !important;}
.stSlider [data-testid="stThumbValue"]{color:#00d4ff !important;}
.block-container{padding:2rem 3rem;}
section[data-testid="stSidebar"]{display:none;}
.stTextInput input{color:#ffffff !important;background-color:#0c2233 !important;
border:1px solid #1e4a6e !important;border-radius:8px !important;padding:10px !important;}
.stTextInput input:focus{border-color:#00d4ff !important;box-shadow:0 0 8px rgba(0,212,255,0.3) !important;}
.stTextInput input::placeholder{color:#5a8099 !important;}
.stTextInput label{color:#00d4ff !important;font-weight:600 !important;font-size:13px !important;}
.stTextInput>div>div{background-color:#0c2233 !important;}
.stSelectbox>div>div{background-color:#0c2233 !important;color:#ffffff !important;border:1px solid #1e4a6e !important;}
.stSelectbox label{color:#00d4ff !important;font-weight:600 !important;}
.stTabs [data-baseweb=tab]{color:#94a3b8 !important;font-size:14px !important;font-weight:600 !important;}
.stTabs [data-baseweb=tab-list]{background-color:#071828 !important;border-radius:10px !important;padding:4px !important;}
.stTabs [aria-selected=true]{color:#00d4ff !important;background-color:#0c2233 !important;border-radius:8px !important;}
.stDataFrame{background-color:#071828 !important;}
div[data-testid="metric-container"]{background-color:#071828 !important;}
.home-title{font-size:42px;font-weight:800;background:linear-gradient(135deg,#00d4ff,#00ff9d);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:8px;}
.home-sub{text-align:center;color:#5a8099;font-size:15px;margin-bottom:40px;letter-spacing:1px;}
.stat-row{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:48px;}
.stat-chip{background:#071828;border:1px solid #0e3a56;border-radius:30px;padding:10px 24px;text-align:center;}
.stat-chip .num{font-size:22px;font-weight:700;color:#00d4ff;}
.stat-chip .lbl{font-size:11px;color:#5a8099;text-transform:uppercase;letter-spacing:1px;}
.nav-card{background:linear-gradient(135deg,#071828,#0c2233);border:1px solid #0e3a56;
border-radius:16px;padding:28px 24px;text-align:center;position:relative;overflow:hidden;}
.nav-card .icon{font-size:36px;margin-bottom:12px;}
.nav-card .title{font-size:17px;font-weight:700;color:#ffffff;margin-bottom:6px;}
.nav-card .desc{font-size:12px;color:#5a8099;line-height:1.5;}
.nav-card .badge{position:absolute;top:12px;right:12px;font-size:10px;padding:3px 10px;
border-radius:20px;font-weight:600;letter-spacing:1px;}
.badge-ml{background:rgba(0,212,255,0.15);color:#00d4ff;border:1px solid #00d4ff;}
.badge-dl{background:rgba(0,255,157,0.15);color:#00ff9d;border:1px solid #00ff9d;}
.badge-ai{background:rgba(255,184,0,0.15);color:#ffb800;border:1px solid #ffb800;}
.badge-ew{background:rgba(255,77,109,0.15);color:#ff4d6d;border:1px solid #ff4d6d;}
.badge-new{background:rgba(167,139,250,0.15);color:#a78bfa;border:1px solid #a78bfa;}
.metric-card{background:linear-gradient(135deg,#071828,#0c2233);border:1px solid #0e3a56;
border-radius:14px;padding:22px 18px;text-align:center;margin:4px;}
.metric-value{font-size:30px;font-weight:700;color:#00d4ff;}
.metric-label{font-size:11px;color:#5a8099;text-transform:uppercase;letter-spacing:2px;margin-top:4px;}
.section-title{font-size:13px;font-weight:600;color:#00d4ff;text-transform:uppercase;
letter-spacing:3px;margin-bottom:16px;border-bottom:1px solid #0e3a56;padding-bottom:8px;}
.alert-red{background:rgba(255,77,109,0.12);border:1px solid #ff4d6d;border-left:4px solid #ff4d6d;
border-radius:10px;padding:14px 20px;color:#ff4d6d;font-weight:600;margin:6px 0;}
.alert-yellow{background:rgba(255,184,0,0.12);border:1px solid #ffb800;border-left:4px solid #ffb800;
border-radius:10px;padding:14px 20px;color:#ffb800;font-weight:600;margin:6px 0;}
.alert-green{background:rgba(0,255,157,0.12);border:1px solid #00ff9d;border-left:4px solid #00ff9d;
border-radius:10px;padding:14px 20px;color:#00ff9d;font-weight:600;margin:6px 0;}
.alert-orange{background:rgba(251,146,60,0.12);border:1px solid #fb923c;border-left:4px solid #fb923c;
border-radius:10px;padding:14px 20px;color:#fb923c;font-weight:600;margin:6px 0;}
.login-card{background:linear-gradient(135deg,#071828,#0c2233);border:1px solid #0e3a56;
border-radius:20px;padding:40px;max-width:450px;margin:60px auto;}
.stTextInput input{color:#ffffff !important;background-color:#0c2233 !important;border:1px solid #0e3a56 !important;}
.stTextInput input::placeholder{color:#5a8099 !important;}
.stTextInput label{color:#00d4ff !important;font-weight:600 !important;}
.stSelectbox label{color:#00d4ff !important;font-weight:600 !important;}
.stTabs [data-baseweb=tab]{color:#ffffff !important;}
.stTabs [data-baseweb=tab-list]{background-color:#071828 !important;}
.stTabs [aria-selected=true]{color:#00d4ff !important;border-bottom:2px solid #00d4ff !important;}
h1{color:#ffffff !important;font-size:28px !important;font-weight:700 !important;}
h2{color:#e2f0f7 !important;}
h3{color:#00d4ff !important;}
.stButton button{background:linear-gradient(135deg,#00d4ff,#0099bb) !important;
color:#020d18 !important;font-weight:700 !important;border:none !important;
border-radius:8px !important;padding:12px !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SQLITE DATABASE SETUP
# ══════════════════════════════════════════
DB_PATH = '../data/waterborne_ews.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'Health Officer',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Predictions table
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        zone TEXT,
        result TEXT,
        confidence REAL,
        risk_score REAL,
        bacteria REAL,
        lead REAL,
        arsenic REAL,
        nitrates REAL,
        timestamp TEXT
    )''')

    # Alerts table
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        zone TEXT,
        alert_level TEXT,
        message TEXT,
        timestamp TEXT
    )''')

    # Create default admin user
    admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
    officer_pass = hashlib.sha256("officer123".encode()).hexdigest()
    lab_pass   = hashlib.sha256("lab12345".encode()).hexdigest()
    field_pass = hashlib.sha256("field123".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  ("admin", admin_pass, "Admin"))
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  ("officer1", officer_pass, "Health Officer"))
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  ("lab1", lab_pass, "Lab Technician"))
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  ("field1", field_pass, "Field Officer"))
    except: pass

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def register_user(username, password, role):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  (username, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def save_prediction(username, zone, result, confidence, risk_score,
                    bacteria, lead, arsenic, nitrates):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO predictions
        (username,zone,result,confidence,risk_score,bacteria,lead,arsenic,nitrates,timestamp)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (username, zone, result, confidence, risk_score,
         bacteria, lead, arsenic, nitrates,
         datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    conn.commit()
    conn.close()

def save_alert(username, zone, level, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO alerts (username,zone,alert_level,message,timestamp)
        VALUES (?,?,?,?,?)''',
        (username, zone, level, message,
         datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    conn.commit()
    conn.close()

def get_predictions(username=None):
    conn = sqlite3.connect(DB_PATH)
    if username and username != "admin":
        df = pd.read_sql("SELECT * FROM predictions WHERE username=? ORDER BY id DESC",
                         conn, params=(username,))
    else:
        df = pd.read_sql("SELECT * FROM predictions ORDER BY id DESC", conn)
    conn.close()
    return df

def get_alerts(username=None):
    conn = sqlite3.connect(DB_PATH)
    if username and username != "admin":
        df = pd.read_sql("SELECT * FROM alerts WHERE username=? ORDER BY id DESC LIMIT 20",
                         conn, params=(username,))
    else:
        df = pd.read_sql("SELECT * FROM alerts ORDER BY id DESC LIMIT 20", conn)
    conn.close()
    return df

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT id,username,role,created_at FROM users", conn)
    conn.close()
    return df

# Initialize database
init_db()

# ══════════════════════════════════════════
# LOAD DATA & MODEL
# ══════════════════════════════════════════
@st.cache_resource
def load_model():
    try:
        with open('../models/xgb_90_model.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Model not found: {e}"); st.stop()

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/waterQuality1.csv')
        df = df[df['is_safe'] != '#NUM!']
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df.dropna()
    except Exception as e:
        st.error(f"Data not found: {e}"); st.stop()

@st.cache_data
def load_cholera():
    try: return pd.read_csv('../data/cholera_timeseries.csv')
    except: return pd.DataFrame({'Year':range(2000,2017),'Cases':[100000]*17})

@st.cache_data
def load_pollution():
    try: return pd.read_csv('../data/water_pollution_clean.csv')
    except: return pd.DataFrame({'Region':['Asia','Africa','Europe','Americas'],
        'Cholera Cases per 100,000 people':[45,80,5,20],
        'Typhoid Cases per 100,000 people':[60,90,8,25]})

@st.cache_data
def load_shap():
    try: return pd.read_csv('../reports/shap_feature_importance.csv')
    except:
        features=['aluminium','ammonia','arsenic','barium','cadmium','chloramine',
                  'chromium','copper','flouride','bacteria','viruses','lead',
                  'nitrates','nitrites','mercury','perchlorate','radium',
                  'selenium','silver','uranium']
        importance=[2.07,1.45,1.23,1.10,0.98,0.87,0.76,0.65,0.54,1.89,
                    1.67,1.34,0.92,0.78,0.67,0.56,0.45,0.34,0.23,0.89]
        return pd.DataFrame({'Feature':features,'SHAP_Importance':importance})

model=load_model(); df=load_data(); cholera=load_cholera()
pollution=load_pollution(); shap_df=load_shap()

PBG='#071828';PPG='#020d18';FC='#ffffff';GC='#0e3a56'
BLUE='#00d4ff';GRN='#00ff9d';RED='#ff4d6d';YLW='#ffb800';ORG='#fb923c'

def theme(fig,title=""):
    fig.update_layout(plot_bgcolor=PBG,paper_bgcolor=PPG,font_color=FC,
        title=dict(text=title,font=dict(color='#e2f0f7',size=15)),
        xaxis=dict(gridcolor=GC,color=FC),yaxis=dict(gridcolor=GC,color=FC),
        legend=dict(bgcolor='rgba(0,0,0,0)'),margin=dict(l=20,r=20,t=50,b=20))
    return fig

def detect_disease(bacteria,viruses,lead,arsenic,nitrates,uranium,cadmium,pred):
    diseases=[]
    if pred==0:
        if bacteria>0 or viruses>0:
            diseases.append(("CRITICAL","Cholera / Typhoid Risk",RED,"Biological contamination detected! Boil water immediately."))
        if arsenic>0.01:
            diseases.append(("CRITICAL","Arsenicosis / Cancer Risk",RED,f"Arsenic {arsenic:.3f} mg/L exceeds WHO limit!"))
        if lead>0.015:
            diseases.append(("HIGH","Lead Poisoning Risk",ORG,f"Lead {lead:.3f} mg/L exceeds WHO limit!"))
        if uranium>0.03:
            diseases.append(("HIGH","Uranium Toxicity",ORG,f"Uranium {uranium:.3f} mg/L exceeds WHO limit!"))
        if nitrates>10:
            diseases.append(("MODERATE","Typhoid / Thyroid Risk",YLW,f"Nitrates {nitrates:.1f} mg/L above 10 mg/L"))
        if cadmium>0.003:
            diseases.append(("HIGH","Cadmium Poisoning",ORG,f"Cadmium {cadmium:.4f} mg/L exceeds WHO limit!"))
        if not diseases:
            diseases.append(("UNSAFE","General Contamination",YLW,"Water parameters indicate contamination."))
    return diseases

def generate_pdf_report(zone,result,confidence,diseases,alerts,param_names,param_values,param_limits):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True,margin=15)
    pdf.set_font("Arial","B",18)
    pdf.set_text_color(0,100,150)
    pdf.cell(0,12,"WATERBORNE DISEASE EARLY WARNING SYSTEM",ln=True,align="C")
    pdf.set_font("Arial","B",13)
    pdf.set_text_color(50,50,50)
    pdf.cell(0,8,"Water Quality Alert Report",ln=True,align="C")
    pdf.ln(3)
    pdf.set_font("Arial","",10)
    pdf.set_text_color(80,80,80)
    pdf.cell(0,6,f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",ln=True)
    pdf.cell(0,6,f"Zone: {zone if zone else 'Not specified'}",ln=True)
    pdf.ln(4)
    pdf.set_draw_color(0,180,220)
    pdf.set_line_width(0.8)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Arial","B",13)
    pdf.set_text_color(0,100,150)
    pdf.cell(0,8,"PREDICTION RESULT",ln=True)
    pdf.set_font("Arial","B",14)
    if result=="SAFE":
        pdf.set_text_color(0,160,80)
        pdf.cell(0,10,f"SAFE WATER - Confidence: {confidence}%",ln=True)
    else:
        pdf.set_text_color(200,50,50)
        pdf.cell(0,10,f"UNSAFE WATER - Confidence: {confidence}%",ln=True)
    pdf.ln(3)
    if diseases:
        pdf.set_font("Arial","B",12)
        pdf.set_text_color(0,100,150)
        pdf.cell(0,8,"DISEASE RISK ASSESSMENT",ln=True)
        pdf.set_font("Arial","",10)
        pdf.set_text_color(180,50,50)
        for level,disease,_,msg in diseases:
            pdf.cell(0,7,f"  [{level}] {disease}: {msg}",ln=True)
        pdf.ln(3)
    pdf.set_line_width(0.8)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Arial","B",12)
    pdf.set_text_color(0,100,150)
    pdf.cell(0,8,"PARAMETER READINGS vs WHO LIMITS",ln=True)
    pdf.set_font("Arial","B",10)
    pdf.set_fill_color(0,100,150)
    pdf.set_text_color(255,255,255)
    pdf.cell(50,8,"Parameter",border=1,fill=True)
    pdf.cell(40,8,"Current Value",border=1,fill=True)
    pdf.cell(40,8,"WHO Limit",border=1,fill=True)
    pdf.cell(40,8,"Status",border=1,fill=True,ln=True)
    pdf.set_font("Arial","",10)
    for name,val,lim in zip(param_names,param_values,param_limits):
        status="ALERT" if (lim==0 and val>0) or (lim>0 and val>lim) else "SAFE"
        pdf.set_text_color(200,50,50) if status=="ALERT" else pdf.set_text_color(0,150,80)
        pdf.cell(50,7,name,border=1)
        pdf.cell(40,7,str(round(val,4)),border=1)
        pdf.cell(40,7,str(lim),border=1)
        pdf.cell(40,7,status,border=1,ln=True)
    pdf.ln(4)
    pdf.set_line_width(0.8)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Arial","B",12)
    pdf.set_text_color(0,100,150)
    pdf.cell(0,8,"ALERT SUMMARY",ln=True)
    pdf.set_font("Arial","",10)
    if not alerts:
        pdf.set_text_color(0,150,80)
        pdf.cell(0,7,"ALL CLEAR - All parameters within WHO safe limits.",ln=True)
    else:
        for lvl,msg in alerts:
            msg_clean=msg.replace("🦠","").replace("🧪","").replace("☠️","").replace("☢️","").replace("⚗️","").replace("⚠️","").strip()
            pdf.set_text_color(200,50,50) if lvl=="RED" else pdf.set_text_color(180,130,0)
            pdf.cell(0,7,f"  [{lvl}] {msg_clean}",ln=True)
    pdf.ln(4)
    pdf.set_line_width(0.8)
    pdf.line(10,pdf.get_y(),200,pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Arial","B",12)
    pdf.set_text_color(0,100,150)
    pdf.cell(0,8,"RECOMMENDED ACTION",ln=True)
    pdf.set_font("Arial","",10)
    if result=="SAFE":
        pdf.set_text_color(0,150,80)
        pdf.cell(0,7,"Water is safe. Continue normal use. Conduct monthly testing.",ln=True)
    else:
        pdf.set_text_color(200,50,50)
        pdf.cell(0,7,"STOP water supply immediately.",ln=True)
        pdf.cell(0,7,"Boil water before any use.",ln=True)
        pdf.cell(0,7,"Report to local health authority.",ln=True)
        pdf.cell(0,7,"Identify and treat contamination source.",ln=True)
    pdf.ln(4)
    pdf.set_font("Arial","I",8)
    pdf.set_text_color(120,120,120)
    pdf.cell(0,6,"Smart Community Health Monitoring | XGBoost 97.12% | WHO Standards",ln=True,align="C")
    return bytes(pdf.output())

# ══════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'role' not in st.session_state:
    st.session_state.role = ''
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_home():
    if st.button("← Back to Home", key="back_"+st.session_state.page):
        st.session_state.page = 'home'
        st.rerun()

# ══════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════
if not st.session_state.logged_in:
    # ── Impressive Login Page ──────────────────────────────────────
    # Full screen background
    st.markdown("""
    <div style='position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg,#020d18 0%,#071828 50%,#0c2233 100%);z-index:-1;'></div>
    """, unsafe_allow_html=True)

    # Logo + Title
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align:center;margin-bottom:8px;'>
            <div style='font-size:64px;'>💧</div>
            <div style='font-size:32px;font-weight:800;background:linear-gradient(135deg,#00d4ff,#00ff9d);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;'>
            Waterborne Disease EWS</div>
            <div style='color:#5a8099;font-size:13px;letter-spacing:2px;text-transform:uppercase;'>
            Smart Community Health Monitoring System</div>
        </div>
        <div style='display:flex;justify-content:center;gap:12px;margin:16px 0;flex-wrap:wrap;'>
            <div style='background:#071828;border:1px solid #0e3a56;border-radius:20px;padding:6px 16px;font-size:11px;color:#00d4ff;'>97.12% Accuracy</div>
            <div style='background:#071828;border:1px solid #0e3a56;border-radius:20px;padding:6px 16px;font-size:11px;color:#00ff9d;'>XGBoost + LSTM</div>
            <div style='background:#071828;border:1px solid #0e3a56;border-radius:20px;padding:6px 16px;font-size:11px;color:#ffb800;'>WHO Standards</div>
            <div style='background:#071828;border:1px solid #0e3a56;border-radius:20px;padding:6px 16px;font-size:11px;color:#f472b6;'>SHAP Explainable AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Login card
        st.markdown("""
        <div style='background:linear-gradient(135deg,#071828,#0c2233);border:1px solid #0e3a56;
        border-radius:20px;padding:32px;box-shadow:0 8px 32px rgba(0,212,255,0.1);'>
        <div style='text-align:center;margin-bottom:24px;'>
            <div style='font-size:13px;font-weight:600;color:#00d4ff;text-transform:uppercase;letter-spacing:3px;'>
            Secure Login Portal</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔐 Login to Dashboard", use_container_width=True):
                if username and password:
                    user = verify_login(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = user[3]
                        st.session_state.page = 'home'
                        st.rerun()
                    else:
                        st.markdown("<div class='alert-red'>❌ Wrong username or password! Try again.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='alert-yellow'>⚠️ Please enter both username and password</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background:#071828;border:1px solid #0e3a56;border-radius:12px;padding:16px;'>
                <div style='font-size:11px;font-weight:600;color:#00d4ff;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;'>
                Default Login Credentials</div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
                    <div style='background:#0c2233;border:1px solid #ff4d6d;border-radius:8px;padding:10px;'>
                        <div style='color:#ff4d6d;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>Admin</div>
                        <div style='color:#ffffff;font-size:12px;margin-top:4px;'>admin / admin123</div>
                    </div>
                    <div style='background:#0c2233;border:1px solid #00ff9d;border-radius:8px;padding:10px;'>
                        <div style='color:#00ff9d;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>Health Officer</div>
                        <div style='color:#ffffff;font-size:12px;margin-top:4px;'>officer1 / officer123</div>
                    </div>
                    <div style='background:#0c2233;border:1px solid #00d4ff;border-radius:8px;padding:10px;'>
                        <div style='color:#00d4ff;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>Lab Technician</div>
                        <div style='color:#ffffff;font-size:12px;margin-top:4px;'>lab1 / lab12345</div>
                    </div>
                    <div style='background:#0c2233;border:1px solid #ffb800;border-radius:8px;padding:10px;'>
                        <div style='color:#ffb800;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>Field Officer</div>
                        <div style='color:#ffffff;font-size:12px;margin-top:4px;'>field1 / field123</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            new_user  = st.text_input("👤 New Username", placeholder="Choose a username")
            new_pass  = st.text_input("🔑 New Password", type="password", placeholder="Min 6 characters")
            new_pass2 = st.text_input("🔑 Confirm Password", type="password", placeholder="Confirm password")
            new_role  = st.selectbox("👔 Role", ["Health Officer", "Lab Technician", "Field Officer", "Admin"])
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝 Create Account", use_container_width=True):
                if new_user and new_pass and new_pass2:
                    if new_pass != new_pass2:
                        st.markdown("<div class='alert-red'>❌ Passwords do not match!</div>", unsafe_allow_html=True)
                    elif len(new_pass) < 6:
                        st.markdown("<div class='alert-yellow'>⚠️ Password must be at least 6 characters</div>", unsafe_allow_html=True)
                    else:
                        if register_user(new_user, new_pass, new_role):
                            st.markdown("<div class='alert-green'>✅ Account created! Go to Login tab.</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='alert-red'>❌ Username already exists!</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='alert-yellow'>⚠️ Please fill all fields</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#5a8099;font-size:11px;'>Smart Community Health Monitoring and Early Warning System for Waterborne Diseases</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# MAIN APP (after login)
# ══════════════════════════════════════════
else:
    # Top bar with user info
    col1,col2,col3 = st.columns([3,1,1])
    with col2:
        st.markdown(f"<div style='color:#00d4ff;font-size:13px;text-align:right;padding-top:8px'>👤 {st.session_state.username} ({st.session_state.role})</div>", unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ''
            st.session_state.role = ''
            st.session_state.page = 'home'
            st.rerun()

    # ══════════════════════════════════════════
    # HOME PAGE
    # ══════════════════════════════════════════
    if st.session_state.page == 'home':
        st.markdown("<div class='home-title'>💧 Waterborne Disease Early Warning System</div>", unsafe_allow_html=True)
        st.markdown("<div class='home-sub'>Smart Community Health Monitoring using Machine Learning and Deep Learning</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='stat-row'>
            <div class='stat-chip'><div class='num' style='color:#00ff9d'>97.12%</div><div class='lbl'>XGBoost Accuracy</div></div>
            <div class='stat-chip'><div class='num' style='color:#00d4ff'>7,996</div><div class='lbl'>Water Samples</div></div>
            <div class='stat-chip'><div class='num' style='color:#ffb800'>3</div><div class='lbl'>ML Models</div></div>
            <div class='stat-chip'><div class='num' style='color:#f472b6'>20</div><div class='lbl'>Parameters</div></div>
            <div class='stat-chip'><div class='num' style='color:#fb923c'>10 Yrs</div><div class='lbl'>LSTM Forecast</div></div>
            <div class='stat-chip'><div class='num' style='color:#a78bfa'>WHO</div><div class='lbl'>Standards</div></div>
            <div class='stat-chip'><div class='num' style='color:#00d4ff'>4</div><div class='lbl'>User Roles</div></div>
        </div>""", unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown("""<div class='nav-card'><span class='badge badge-ml'>ML</span>
            <div class='icon'>📊</div><div class='title'>Overview</div>
            <div class='desc'>Project summary, KPI metrics, water safety distribution and cholera trend</div></div>""", unsafe_allow_html=True)
            if st.button("Open Overview", use_container_width=True, key="btn_overview"):
                st.session_state.page='overview'; st.rerun()
        with c2:
            st.markdown("""<div class='nav-card'><span class='badge badge-ml'>97.12%</span>
            <div class='icon'>💧</div><div class='title'>Risk Prediction</div>
            <div class='desc'>Enter 20 chemical parameters and get instant disease risk prediction</div></div>""", unsafe_allow_html=True)
            if st.button("Open Risk Prediction", use_container_width=True, key="btn_risk"):
                st.session_state.page='risk'; st.rerun()
        with c3:
            st.markdown("""<div class='nav-card'><span class='badge badge-ai'>XAI</span>
            <div class='icon'>🔍</div><div class='title'>SHAP Explainability</div>
            <div class='desc'>Explainable AI showing which chemicals drive unsafe predictions most</div></div>""", unsafe_allow_html=True)
            if st.button("Open SHAP", use_container_width=True, key="btn_shap"):
                st.session_state.page='shap'; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c4,c5,c6 = st.columns(3)
        with c4:
            st.markdown("""<div class='nav-card'><span class='badge badge-dl'>LSTM</span>
            <div class='icon'>📈</div><div class='title'>Outbreak Forecast</div>
            <div class='desc'>LSTM deep learning forecasting cholera outbreaks for next 10 years</div></div>""", unsafe_allow_html=True)
            if st.button("Open Forecast", use_container_width=True, key="btn_forecast"):
                st.session_state.page='forecast'; st.rerun()
        with c5:
            st.markdown("""<div class='nav-card'><span class='badge badge-ml'>EDA</span>
            <div class='icon'>🧪</div><div class='title'>Water Quality EDA</div>
            <div class='desc'>Explore chemical distributions, correlations and disease patterns</div></div>""", unsafe_allow_html=True)
            if st.button("Open EDA", use_container_width=True, key="btn_eda"):
                st.session_state.page='eda'; st.rerun()
        with c6:
            st.markdown("""<div class='nav-card'><span class='badge badge-ew'>LIVE</span>
            <div class='icon'>🚨</div><div class='title'>Early Warning Alerts</div>
            <div class='desc'>Real time WHO contamination alerts with gauges and PDF report download</div></div>""", unsafe_allow_html=True)
            if st.button("Open Alerts", use_container_width=True, key="btn_alerts"):
                st.session_state.page='alerts'; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c7,c8,c9 = st.columns(3)
        with c7:
            st.markdown("""<div class='nav-card'><span class='badge badge-new'>DB</span>
            <div class='icon'>📋</div><div class='title'>Prediction History</div>
            <div class='desc'>All predictions saved in SQLite database — permanent storage</div></div>""", unsafe_allow_html=True)
            if st.button("Open History", use_container_width=True, key="btn_history"):
                st.session_state.page='history'; st.rerun()
        with c8:
            st.markdown("""<div class='nav-card'><span class='badge badge-new'>NEW</span>
            <div class='icon'>🏥</div><div class='title'>Disease Info</div>
            <div class='desc'>Cholera, Typhoid, Dysentery — symptoms, causes and prevention</div></div>""", unsafe_allow_html=True)
            if st.button("Open Disease Info", use_container_width=True, key="btn_disease"):
                st.session_state.page='disease'; st.rerun()
        with c9:
            st.markdown("""<div class='nav-card'><span class='badge badge-new'>NEW</span>
            <div class='icon'>📊</div><div class='title'>Zone Comparison</div>
            <div class='desc'>Compare water quality across 4 zones — identify most at-risk area</div></div>""", unsafe_allow_html=True)
            if st.button("Open Zone Compare", use_container_width=True, key="btn_zone"):
                st.session_state.page='zone'; st.rerun()

        # Admin panel
        if st.session_state.role == "Admin":
            st.markdown("<br>", unsafe_allow_html=True)
            c10,c11,c12 = st.columns(3)
            with c10:
                st.markdown("""<div class='nav-card'><span class='badge badge-ew'>ADMIN</span>
                <div class='icon'>⚙️</div><div class='title'>Admin Panel</div>
                <div class='desc'>Manage users, view all predictions and alerts from all officers</div></div>""", unsafe_allow_html=True)
                if st.button("Open Admin Panel", use_container_width=True, key="btn_admin"):
                    st.session_state.page='admin'; st.rerun()

        st.markdown("<hr style='border-color:#0e3a56'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#5a8099;font-size:12px'>Smart Community Health Monitoring & Early Warning System | XGBoost 97.12% | LSTM | SHAP | SQLite Database</p>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # OVERVIEW PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'overview':
        go_home()
        st.markdown("<h1>📊 Overview</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Project summary and key metrics</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>", unsafe_allow_html=True)

        c1,c2,c3,c4=st.columns(4)
        for col,val,lbl in zip([c1,c2,c3,c4],["97.12%","7,996","20","10 Yrs"],
            ["Model Accuracy","Water Samples","Parameters","LSTM Forecast"]):
            col.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{lbl}</div></div>",unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            counts=df['is_safe'].value_counts()
            fig=px.pie(values=counts.values,names=['Unsafe','Safe'],color_discrete_sequence=[RED,GRN],hole=0.5)
            fig=theme(fig,"Water Safety Distribution")
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            yearly=cholera.groupby('Year')['Cases'].sum().reset_index()
            fig=px.area(yearly,x='Year',y='Cases',color_discrete_sequence=[BLUE])
            fig.update_traces(fill='tozeroy',fillcolor='rgba(0,212,255,0.08)',line_width=2)
            fig=theme(fig,"Global Cholera Cases Over Years")
            st.plotly_chart(fig,use_container_width=True)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Model Performance Summary</div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.markdown("<div class='metric-card'><div class='metric-label'>Random Forest</div><div class='metric-value' style='font-size:24px;color:#ffb800'>66.77%</div><div class='metric-label'>Accuracy</div></div>",unsafe_allow_html=True)
        c2.markdown("<div class='metric-card'><div class='metric-label'>XGBoost Final</div><div class='metric-value' style='font-size:24px;color:#00ff9d'>97.12%</div><div class='metric-label'>Accuracy</div></div>",unsafe_allow_html=True)
        c3.markdown("<div class='metric-card'><div class='metric-label'>LSTM Forecast</div><div class='metric-value' style='font-size:24px;color:#00d4ff'>132,506</div><div class='metric-label'>RMSE Cases</div></div>",unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # RISK PREDICTION PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'risk':
        go_home()
        st.markdown("<h1>💧 Water Safety Risk Prediction</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Adjust chemical parameters and click Predict</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)

        zone_name=st.text_input("📍 Zone / Location Name",placeholder="e.g. Zone A, Ward 5, River Area")

        c1,c2,c3=st.columns(3)
        with c1:
            st.markdown("<div class='section-title'>Group 1 - Metals</div>",unsafe_allow_html=True)
            aluminium =st.slider("Aluminium", 0.0,5.0, 1.0,0.01)
            ammonia   =st.slider("Ammonia",   0.0,35.0,5.0,0.1)
            arsenic   =st.slider("Arsenic",   0.0,0.5, 0.05,0.001)
            barium    =st.slider("Barium",    0.0,5.0, 1.0,0.01)
            cadmium   =st.slider("Cadmium",   0.0,0.02,0.003,0.0001)
            chloramine=st.slider("Chloramine",0.0,10.0,4.0,0.1)
            chromium  =st.slider("Chromium",  0.0,1.0, 0.05,0.01)
        with c2:
            st.markdown("<div class='section-title'>Group 2 - Biological</div>",unsafe_allow_html=True)
            copper  =st.slider("Copper",  0.0,5.0, 1.0,0.01)
            flouride=st.slider("Flouride",0.0,2.0, 0.5,0.01)
            bacteria=st.slider("Bacteria",0.0,1.0, 0.0,0.01)
            viruses =st.slider("Viruses", 0.0,1.0, 0.0,0.01)
            lead    =st.slider("Lead",    0.0,0.1, 0.01,0.001)
            nitrates=st.slider("Nitrates",0.0,20.0,5.0,0.1)
            nitrites=st.slider("Nitrites",0.0,5.0, 1.0,0.01)
        with c3:
            st.markdown("<div class='section-title'>Group 3 - Chemical</div>",unsafe_allow_html=True)
            mercury    =st.slider("Mercury",    0.0,0.01,0.002,0.0001)
            perchlorate=st.slider("Perchlorate",0.0,60.0,20.0,0.1)
            radium     =st.slider("Radium",     0.0,10.0,3.0,0.01)
            selenium   =st.slider("Selenium",   0.0,0.5, 0.05,0.001)
            silver     =st.slider("Silver",     0.0,1.0, 0.1,0.01)
            uranium    =st.slider("Uranium",    0.0,0.1, 0.02,0.001)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        if st.button("Predict Water Safety",use_container_width=True):
            inp=pd.DataFrame([[aluminium,ammonia,arsenic,barium,cadmium,chloramine,chromium,
                               copper,flouride,bacteria,viruses,lead,nitrates,nitrites,
                               mercury,perchlorate,radium,selenium,silver,uranium]],
                             columns=df.drop('is_safe',axis=1).columns)
            pred=model.predict(inp)[0]
            prob=model.predict_proba(inp)[0]
            confidence=round(prob[1]*100,1) if pred==1 else round(prob[0]*100,1)
            result="SAFE" if pred==1 else "UNSAFE"
            risk_score=round(prob[0]*100,1)

            st.markdown("<br>",unsafe_allow_html=True)
            if pred==1:
                st.markdown(f"<div class='alert-green'>SAFE WATER - Confidence: {confidence}%<br><span style='font-size:13px;font-weight:400'>All parameters within acceptable limits.</span></div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='alert-red'>UNSAFE WATER - Confidence: {confidence}%<br><span style='font-size:13px;font-weight:400'>Do NOT consume without treatment.</span></div>",unsafe_allow_html=True)

            diseases=detect_disease(bacteria,viruses,lead,arsenic,nitrates,uranium,cadmium,pred)
            if diseases:
                st.markdown("<br>",unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Disease Risk Assessment</div>",unsafe_allow_html=True)
                for level,disease_name,color,msg in diseases:
                    st.markdown(f"<div style='background:rgba(255,77,109,0.08);border:1px solid {color};border-left:4px solid {color};border-radius:10px;padding:14px 20px;margin:6px 0;'><div style='color:{color};font-size:15px;font-weight:700;'>{level} - {disease_name}</div><div style='color:#e2f0f7;font-size:13px;margin-top:4px;'>{msg}</div></div>",unsafe_allow_html=True)

            # Gauge
            fig=go.Figure(go.Indicator(mode="gauge+number",value=round(prob[1]*100,1),
                number={'suffix':'%','font':{'color':GRN if pred==1 else RED,'size':40}},
                title={'text':"Safe Water Probability",'font':{'color':FC,'size':14}},
                gauge={'axis':{'range':[0,100]},'bar':{'color':GRN if pred==1 else RED},
                    'bgcolor':PBG,'bordercolor':GC,
                    'steps':[{'range':[0,40],'color':'rgba(255,77,109,0.2)'},
                              {'range':[40,70],'color':'rgba(255,184,0,0.2)'},
                              {'range':[70,100],'color':'rgba(0,255,157,0.2)'}],
                    'threshold':{'line':{'color':YLW,'width':3},'thickness':0.75,'value':50}}))
            fig.update_layout(paper_bgcolor=PPG,font_color=FC,height=300,margin=dict(t=40,b=10))
            st.plotly_chart(fig,use_container_width=True)

            # Action
            st.markdown("<div class='section-title'>Recommended Action</div>",unsafe_allow_html=True)
            if pred==1:
                st.markdown("<div class='alert-green'>Continue normal use. Conduct monthly testing.</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='alert-red'>Stop supply | Boil water | Report to health authority | Find contamination source</div>",unsafe_allow_html=True)

            # Save to SQLite database
            save_prediction(st.session_state.username, zone_name, result,
                          confidence, risk_score, bacteria, lead, arsenic, nitrates)
            st.markdown("<div class='alert-green'>Prediction saved to database!</div>",unsafe_allow_html=True)

            # PDF download
            param_n=['Bacteria','Viruses','Lead','Arsenic','Uranium','Nitrates','Cadmium']
            param_v=[bacteria,viruses,lead,arsenic,uranium,nitrates,cadmium]
            param_l=[0,0,0.015,0.01,0.03,10,0.003]
            alerts_list=[]
            if bacteria>0:    alerts_list.append(("RED","Bacteria detected!"))
            if viruses>0:     alerts_list.append(("RED","Viruses detected!"))
            if lead>0.015:    alerts_list.append(("RED",f"Lead {lead:.3f} mg/L exceeds limit!"))
            if arsenic>0.01:  alerts_list.append(("RED",f"Arsenic {arsenic:.3f} mg/L exceeds limit!"))
            if uranium>0.03:  alerts_list.append(("RED",f"Uranium {uranium:.3f} mg/L exceeds limit!"))
            if cadmium>0.003: alerts_list.append(("RED",f"Cadmium {cadmium:.4f} mg/L exceeds limit!"))
            if nitrates>10:   alerts_list.append(("YELLOW",f"Nitrates {nitrates:.1f} mg/L above limit!"))
            pdf_bytes=generate_pdf_report(zone_name,result,confidence,diseases,alerts_list,param_n,param_v,param_l)
            st.download_button(label="Download PDF Report",data=pdf_bytes,
                file_name=f"water_report_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf",
                mime="application/pdf",use_container_width=True)

    # ══════════════════════════════════════════
    # SHAP PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'shap':
        go_home()
        st.markdown("<h1>SHAP Explainability</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Which chemicals drive water safety predictions most?</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        sdf=shap_df.sort_values('SHAP_Importance',ascending=True)
        fig=px.bar(sdf,x='SHAP_Importance',y='Feature',orientation='h',
                   color='SHAP_Importance',color_continuous_scale=[[0,RED],[0.5,YLW],[1,GRN]])
        fig=theme(fig,"SHAP Feature Importance - Chemical Impact on Water Safety")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Top 5 Most Dangerous Contaminants</div>",unsafe_allow_html=True)
        top5=shap_df.sort_values('SHAP_Importance',ascending=False).head(5)
        cols=st.columns(5)
        colors=[RED,'#ff7043',YLW,BLUE,GRN]
        for i,(_,row) in enumerate(top5.iterrows()):
            cols[i].markdown(f"<div class='metric-card'><div style='font-size:11px;color:#5a8099;letter-spacing:2px;text-transform:uppercase'>Rank {i+1}</div><div style='font-size:17px;font-weight:700;color:{colors[i]};margin:8px 0'>{row['Feature'].capitalize()}</div><div style='font-size:11px;color:#5a8099'>SHAP: {round(row['SHAP_Importance'],3)}</div></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>How to Read SHAP</div>",unsafe_allow_html=True)
        st.markdown("<div class='metric-card' style='text-align:left;padding:20px'><div style='color:#e2f0f7;font-size:14px;line-height:2.2'>High SHAP value = This chemical has most impact on prediction<br>Medium SHAP value = Moderate influence on water safety<br>Low SHAP value = Less impact on final prediction<br><br><b style='color:#00d4ff'>Example:</b> Aluminium SHAP=2.07 means it is the #1 reason model predicted unsafe water.</div></div>",unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # FORECAST PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'forecast':
        go_home()
        st.markdown("<h1>Cholera Outbreak Forecast</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>LSTM deep learning - 10 year cholera prediction</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        yearly=cholera.groupby('Year')['Cases'].sum().reset_index()
        future_years=list(range(2017,2027))
        future_cases=[133763,129168,123900,119288,114817,111335,108235,105464,103023,100870]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=yearly['Year'],y=yearly['Cases'],name='Historical',
            mode='lines',line=dict(color=BLUE,width=2.5),
            fill='tozeroy',fillcolor='rgba(0,212,255,0.06)'))
        fig.add_trace(go.Scatter(x=future_years,y=future_cases,name='LSTM Forecast',
            mode='lines+markers',line=dict(color=RED,width=2.5,dash='dash'),
            marker=dict(size=7,color=RED)))
        fig=theme(fig,"Global Cholera Cases - Historical + LSTM 10 Year Forecast")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        c1,c2=st.columns([2,1])
        with c1:
            st.markdown("<div class='section-title'>Forecast Table</div>",unsafe_allow_html=True)
            fdf=pd.DataFrame({'Year':future_years,'Predicted Cases':[f"{c:,}" for c in future_cases],'Trend':['Decreasing']*10})
            st.dataframe(fdf,use_container_width=True,hide_index=True)
        with c2:
            st.markdown("<div class='metric-card' style='margin-top:30px'><div class='metric-label'>RMSE</div><div class='metric-value' style='font-size:20px'>132,506</div><div class='metric-label' style='margin-top:12px'>MAE</div><div class='metric-value' style='font-size:20px'>89,491</div><div class='metric-label' style='margin-top:12px'>Trend</div><div class='metric-value' style='font-size:20px;color:#00ff9d'>Falling</div></div>",unsafe_allow_html=True)
        st.markdown("<div class='alert-green'>LSTM predicts cholera cases will reduce from 133,763 (2017) to 100,870 (2026) - a 24.6% decrease.</div>",unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # EDA PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'eda':
        go_home()
        st.markdown("<h1>Water Quality EDA</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Explore water quality parameters and disease patterns</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            feature=st.selectbox("Select Chemical Parameter",df.drop('is_safe',axis=1).columns)
            fig=px.histogram(df,x=feature,color='is_safe',barmode='overlay',
                             color_discrete_map={0:RED,1:GRN},labels={'is_safe':'Safe'})
            fig=theme(fig,feature+" - Safe vs Unsafe Distribution")
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            corr=df.drop('is_safe',axis=1).corr()
            fig=px.imshow(corr,color_continuous_scale='RdBu',aspect='auto')
            fig=theme(fig,"Feature Correlation Matrix")
            st.plotly_chart(fig,use_container_width=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        rdf=pollution.groupby('Region')[['Cholera Cases per 100,000 people','Typhoid Cases per 100,000 people']].mean().reset_index()
        fig=px.bar(rdf,x='Region',y=['Cholera Cases per 100,000 people','Typhoid Cases per 100,000 people'],
                   barmode='group',color_discrete_sequence=[RED,YLW])
        fig=theme(fig,"Average Disease Cases by Region")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Dataset Summary</div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.markdown("<div class='metric-card'><div class='metric-value'>7,996</div><div class='metric-label'>Total Samples</div></div>",unsafe_allow_html=True)
        c2.markdown("<div class='metric-card'><div class='metric-value'>20</div><div class='metric-label'>Chemical Parameters</div></div>",unsafe_allow_html=True)
        c3.markdown("<div class='metric-card'><div class='metric-value'>0</div><div class='metric-label'>Missing Values</div></div>",unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ALERTS PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'alerts':
        go_home()
        st.markdown("<h1>Early Warning Alert System</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Real time WHO standard water contamination monitoring</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)

        zone=st.text_input("Zone / Area Name",placeholder="e.g. Zone A, Ward 12")
        st.markdown("<div class='section-title'>Set Contamination Levels</div>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.markdown("<div style='color:#ff4d6d;font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;'>Biological Contaminants</div>",unsafe_allow_html=True)
            a_bact=st.slider("Bacteria Level (CFU/mL)",  0.0,1.0, 0.0,0.01)
            a_viru=st.slider("Viruses Level (PFU/mL)",   0.0,1.0, 0.0,0.01)
            a_lead=st.slider("Lead Concentration (mg/L)",0.0,0.1, 0.0,0.001)
            a_arse=st.slider("Arsenic Level (mg/L)",     0.0,0.5, 0.0,0.001)
        with c2:
            st.markdown("<div style='color:#ffb800;font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;'>Chemical Contaminants</div>",unsafe_allow_html=True)
            a_uran=st.slider("Uranium Level (mg/L)", 0.0,0.1, 0.0,0.001)
            a_nitr=st.slider("Nitrates Level (mg/L)",0.0,20.0,0.0,0.1)
            a_cadm=st.slider("Cadmium Level (mg/L)", 0.0,0.02,0.0,0.0001)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Live Parameter Status</div>",unsafe_allow_html=True)

        param_names =['Bacteria','Viruses','Lead','Arsenic','Uranium','Nitrates','Cadmium']
        param_values=[a_bact,a_viru,a_lead,a_arse,a_uran,a_nitr,a_cadm]
        param_limits=[0,0,0.015,0.01,0.03,10,0.003]
        param_units =['CFU/mL','PFU/mL','mg/L','mg/L','mg/L','mg/L','mg/L']

        cols=st.columns(7)
        for col,name,val,lim,unit in zip(cols,param_names,param_values,param_limits,param_units):
            if lim==0:
                if val>0: color='#ff4d6d';status='ALERT';bg='rgba(255,77,109,0.08)';border='#ff4d6d'
                else:     color='#00ff9d';status='SAFE'; bg='rgba(0,255,157,0.08)'; border='#00ff9d'
            elif val==0:  color='#00ff9d';status='SAFE'; bg='rgba(0,255,157,0.08)'; border='#00ff9d'
            elif val>lim: color='#ff4d6d';status='ALERT';bg='rgba(255,77,109,0.08)';border='#ff4d6d'
            elif val>lim*0.7: color='#ffb800';status='WARN';bg='rgba(255,184,0,0.08)';border='#ffb800'
            else:         color='#00ff9d';status='SAFE'; bg='rgba(0,255,157,0.08)'; border='#00ff9d'
            col.markdown(f"<div style='background:{bg};border:1px solid {border};border-radius:10px;padding:14px 8px;text-align:center;'><div style='color:{color};font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;'>{status}</div><div style='color:#ffffff;font-size:13px;font-weight:700;margin:6px 0;'>{name}</div><div style='color:{color};font-size:16px;font-weight:700;'>{round(val,4)}</div><div style='color:#5a8099;font-size:10px;margin-top:2px;'>{unit}</div><div style='color:#5a8099;font-size:9px;margin-top:4px;'>Limit: {lim}</div></div>",unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        bar_colors=[]
        for v,l in zip(param_values,param_limits):
            if l==0 and v>0: bar_colors.append(RED)
            elif v>l:        bar_colors.append(RED)
            elif v>l*0.7:    bar_colors.append(YLW)
            else:            bar_colors.append(GRN)

        fig=go.Figure()
        fig.add_trace(go.Bar(x=param_names,y=param_values,marker_color=bar_colors,name='Current Value',
            text=[str(round(v,4)) for v in param_values],textposition='outside',textfont=dict(color='white',size=11)))
        fig.add_trace(go.Scatter(x=param_names,y=param_limits,mode='markers+lines',name='WHO Limit',
            line=dict(color=YLW,width=2,dash='dash'),marker=dict(size=10,color=YLW,symbol='diamond')))
        fig=theme(fig,"Current Contamination Levels vs WHO Safety Limits")
        fig.update_layout(height=320)
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Parameter Gauges</div>",unsafe_allow_html=True)
        gc1,gc2,gc3,gc4=st.columns(4)
        gauge_data=[("Bacteria",a_bact,1.0,0),("Lead",a_lead,0.1,0.015),("Arsenic",a_arse,0.5,0.01),("Nitrates",a_nitr,20.0,10)]
        for col,(name,val,maxv,limit) in zip([gc1,gc2,gc3,gc4],gauge_data):
            bar_color=RED if (limit==0 and val>0) or (limit>0 and val>limit) else GRN
            fig=go.Figure(go.Indicator(mode="gauge+number",value=val,
                title={'text':name,'font':{'color':'#ffffff','size':14}},
                number={'font':{'color':bar_color,'size':22}},
                gauge={'axis':{'range':[0,maxv],'tickcolor':FC},'bar':{'color':bar_color},'bgcolor':PBG,'bordercolor':GC,
                    'threshold':{'line':{'color':YLW,'width':3},'thickness':0.75,'value':limit},
                    'steps':[{'range':[0,limit if limit>0 else 0.5],'color':'rgba(0,255,157,0.1)'},
                              {'range':[limit if limit>0 else 0.5,maxv],'color':'rgba(255,77,109,0.1)'}]}))
            fig.update_layout(paper_bgcolor=PPG,font_color=FC,height=200,margin=dict(t=40,b=10,l=10,r=10))
            col.plotly_chart(fig,use_container_width=True)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        if st.button("Generate Alert Report",use_container_width=True):
            alerts=[]
            if a_bact>0:     alerts.append(("RED","Bacteria detected - Cholera/Typhoid outbreak risk!"))
            if a_viru>0:     alerts.append(("RED","Viruses detected - Hepatitis A risk!"))
            if a_lead>0.015: alerts.append(("RED",f"Lead {a_lead:.3f} mg/L exceeds WHO limit - Kidney damage!"))
            if a_arse>0.01:  alerts.append(("RED",f"Arsenic {a_arse:.3f} mg/L exceeds WHO limit - Cancer risk!"))
            if a_uran>0.03:  alerts.append(("RED",f"Uranium {a_uran:.3f} mg/L exceeds WHO limit!"))
            if a_cadm>0.003: alerts.append(("RED",f"Cadmium {a_cadm:.4f} mg/L exceeds WHO limit!"))
            if a_nitr>10:    alerts.append(("YELLOW",f"Nitrates {a_nitr:.1f} mg/L above 10 mg/L - Thyroid risk!"))

            zone_label=zone if zone else "Unknown Zone"
            if not alerts:
                st.markdown(f"<div class='alert-green'>ALL CLEAR - {zone_label} - All parameters within WHO safe limits.</div>",unsafe_allow_html=True)
            else:
                rc=sum(1 for a in alerts if a[0]=="RED")
                yc=sum(1 for a in alerts if a[0]=="YELLOW")
                sc=7-rc-yc
                if rc>=2:   st.markdown(f"<div class='alert-red'>CRITICAL ALERT - {zone_label} - {rc} parameters exceed WHO limits!</div>",unsafe_allow_html=True)
                elif rc==1: st.markdown(f"<div class='alert-orange'>HIGH ALERT - {zone_label} - {rc} parameter exceeds WHO limit!</div>",unsafe_allow_html=True)
                else:       st.markdown(f"<div class='alert-yellow'>CAUTION - {zone_label}</div>",unsafe_allow_html=True)
                st.markdown("<br>",unsafe_allow_html=True)
                c1,c2,c3=st.columns(3)
                c1.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#ff4d6d;font-size:40px'>{rc}</div><div class='metric-label'>Red Alerts</div></div>",unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#ffb800;font-size:40px'>{yc}</div><div class='metric-label'>Caution Alerts</div></div>",unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#00ff9d;font-size:40px'>{sc}</div><div class='metric-label'>Parameters Safe</div></div>",unsafe_allow_html=True)
                st.markdown("<br>",unsafe_allow_html=True)
                for lvl,msg in alerts:
                    if lvl=="RED": st.markdown(f"<div class='alert-red'>{msg}</div>",unsafe_allow_html=True)
                    else:          st.markdown(f"<div class='alert-yellow'>{msg}</div>",unsafe_allow_html=True)
                fig=go.Figure(go.Pie(values=[rc,yc,sc],labels=['Red Alerts','Yellow Alerts','Safe'],hole=0.5,marker_colors=[RED,YLW,GRN]))
                fig=theme(fig,"Alert Summary")
                st.plotly_chart(fig,use_container_width=True)

                # Save alerts to database
                for lvl,msg in alerts:
                    save_alert(st.session_state.username, zone_label, lvl, msg)
                st.markdown("<div class='alert-green'>Alerts saved to database!</div>",unsafe_allow_html=True)

            # PDF download
            pdf_bytes=generate_pdf_report(zone_label,"UNSAFE" if alerts else "SAFE",
                                          "-",[], alerts,param_names,param_values,param_limits)
            st.download_button(label="Download Alert PDF Report",data=pdf_bytes,
                file_name=f"alert_report_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf",
                mime="application/pdf",use_container_width=True)

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>WHO Safety Reference</div>",unsafe_allow_html=True)
        ldf=pd.DataFrame({'Parameter':['Bacteria','Viruses','Lead','Arsenic','Uranium','Nitrates','Cadmium'],
            'WHO Limit':['0 CFU/mL','0 PFU/mL','0.015 mg/L','0.01 mg/L','0.03 mg/L','10 mg/L','0.003 mg/L'],
            'Alert Level':['RED','RED','RED','RED','RED','YELLOW','RED'],
            'Disease Risk':['Cholera, Typhoid','Hepatitis A','Kidney damage','Cancer risk','Kidney damage','Thyroid issues','Kidney damage'],
            'Action':['Boil water immediately','Disinfect supply','Filter & treat','Report to health dept','Stop supply','Dilute & treat','Report to health dept']})
        st.dataframe(ldf,use_container_width=True,hide_index=True)

    # ══════════════════════════════════════════
    # PREDICTION HISTORY PAGE (SQLite)
    # ══════════════════════════════════════════
    elif st.session_state.page == 'history':
        go_home()
        st.markdown("<h1>Prediction History</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>All predictions saved permanently in SQLite database</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)

        hist_df=get_predictions(st.session_state.username)
        if not hist_df.empty:
            for col in hist_df.columns:
                if col not in ['timestamp','username','zone','result']:
                    hist_df[col]=pd.to_numeric(hist_df[col], errors='coerce').fillna(0)

        if hist_df.empty:
            st.markdown("<div class='alert-yellow'>No predictions yet. Go to Risk Prediction page first.</div>",unsafe_allow_html=True)
        else:
            total=len(hist_df)
            unsafe=sum(hist_df['result']=='UNSAFE')
            safe=sum(hist_df['result']=='SAFE')
            avg_rs=hist_df['risk_score'].mean()

            c1,c2,c3,c4=st.columns(4)
            c1.markdown(f"<div class='metric-card'><div class='metric-value'>{total}</div><div class='metric-label'>Total Predictions</div></div>",unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#ff4d6d'>{unsafe}</div><div class='metric-label'>Unsafe Results</div></div>",unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#00ff9d'>{safe}</div><div class='metric-label'>Safe Results</div></div>",unsafe_allow_html=True)
            c4.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#ffb800'>{avg_rs:.1f}</div><div class='metric-label'>Avg Risk Score</div></div>",unsafe_allow_html=True)

            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Prediction Log</div>",unsafe_allow_html=True)
            st.dataframe(hist_df[['timestamp','username','zone','result','confidence','risk_score','bacteria','lead','arsenic','nitrates']],
                         use_container_width=True,hide_index=True)

            if len(hist_df)>1:
                hist_df['risk_score']=pd.to_numeric(hist_df['risk_score'],errors='coerce').fillna(0)
                fig=px.line(hist_df.sort_values('id'),x='timestamp',y='risk_score',
                            color_discrete_sequence=[BLUE],markers=True)
                fig.add_hline(y=50,line_dash="dash",line_color=YLW,annotation_text="Risk Threshold")
                fig=theme(fig,"Risk Score Trend")
                st.plotly_chart(fig,use_container_width=True)

        # Alert history
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Alert History</div>",unsafe_allow_html=True)
        alert_df=get_alerts(st.session_state.username)
        if alert_df.empty:
            st.markdown("<div class='alert-yellow'>No alerts yet.</div>",unsafe_allow_html=True)
        else:
            st.dataframe(alert_df,use_container_width=True,hide_index=True)

    # ══════════════════════════════════════════
    # DISEASE INFO PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'disease':
        go_home()
        st.markdown("<h1>Disease Information</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Know your waterborne disease</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)

        disease=st.selectbox("Select Disease",["Cholera","Typhoid","Dysentery","Hepatitis A","Arsenicosis"])
        info={
            "Cholera":{"icon":"Cholera","color":RED,
                "cause":"Vibrio cholerae bacteria in contaminated water",
                "symptoms":["Severe watery diarrhea","Vomiting","Leg cramps","Dehydration","Shock in severe cases"],
                "water_params":"High bacteria count, low chlorine, high turbidity",
                "prevention":["Boil drinking water","Use purification tablets","Wash hands with soap","Avoid raw foods"],
                "who_limit":"0 bacteria CFU/100mL","mortality":"25-50% untreated, less than 1% with treatment"},
            "Typhoid":{"icon":"Typhoid","color":ORG,
                "cause":"Salmonella typhi bacteria through contaminated water",
                "symptoms":["High fever 39-40C","Headache","Abdominal pain","Constipation or diarrhea","Rose spots on skin"],
                "water_params":"High nitrates, moderate bacteria, low chlorine",
                "prevention":["Drink safe treated water","Typhoid vaccination","Proper sanitation","Safe food handling"],
                "who_limit":"Nitrates less than 10 mg/L","mortality":"10-30% untreated, less than 1% with antibiotics"},
            "Dysentery":{"icon":"Dysentery","color":YLW,
                "cause":"Shigella bacteria in contaminated water",
                "symptoms":["Bloody diarrhea","Stomach cramps","Fever","Nausea","Vomiting"],
                "water_params":"High bacteria, high turbidity, poor sanitation",
                "prevention":["Proper water treatment","Hand hygiene","Safe sanitation","Avoid contaminated sources"],
                "who_limit":"0 bacteria CFU/100mL","mortality":"Rarely fatal with treatment"},
            "Hepatitis A":{"icon":"Hepatitis A","color":BLUE,
                "cause":"Hepatitis A virus through contaminated water",
                "symptoms":["Fatigue","Nausea","Jaundice - yellow skin/eyes","Abdominal pain","Dark urine"],
                "water_params":"Presence of viruses, poor water treatment",
                "prevention":["Hepatitis A vaccination","Boil water","Avoid raw shellfish","Hand washing"],
                "who_limit":"0 viruses detected","mortality":"0.1-0.3% fatality rate"},
            "Arsenicosis":{"icon":"Arsenicosis","color":"#a78bfa",
                "cause":"Long-term exposure to arsenic in drinking water above WHO limit",
                "symptoms":["Skin lesions","Keratosis","Cancer risk","Peripheral neuropathy","Weakness"],
                "water_params":"Arsenic greater than 0.01 mg/L",
                "prevention":["Arsenic removal filters","Use safe water sources","Regular water testing","Community monitoring"],
                "who_limit":"Arsenic less than 0.01 mg/L","mortality":"Increases cancer risk by 20-30x"}
        }
        d=info[disease]
        st.markdown(f"<h2>{d['icon']}</h2>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            symp="".join(["<div style='color:#e2f0f7;font-size:13px;padding:4px 0'>- "+s+"</div>" for s in d["symptoms"]])
            html1="<div class='metric-card' style='text-align:left;padding:20px'>"
            html1+="<div class='section-title'>Cause</div>"
            html1+="<div style='color:#e2f0f7;font-size:14px;margin-bottom:16px'>"+d["cause"]+"</div>"
            html1+="<div class='section-title'>Key Symptoms</div>"+symp+"</div>"
            st.markdown(html1,unsafe_allow_html=True)
        with c2:
            prev="".join(["<div style='color:#e2f0f7;font-size:13px;padding:4px 0'>- "+p+"</div>" for p in d["prevention"]])
            html2="<div class='metric-card' style='text-align:left;padding:20px'>"
            html2+="<div class='section-title'>Water Parameters</div>"
            html2+="<div style='color:"+d["color"]+";font-size:14px;margin-bottom:16px'>"+d["water_params"]+"</div>"
            html2+="<div class='section-title'>WHO Limit</div>"
            html2+="<div style='color:#00d4ff;font-size:14px;margin-bottom:16px'>"+d["who_limit"]+"</div>"
            html2+="<div class='section-title'>Prevention</div>"+prev+"</div>"
            st.markdown(html2,unsafe_allow_html=True)
        st.markdown("<div class='alert-red'>Mortality Rate: "+d["mortality"]+"</div>",unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # ZONE COMPARISON PAGE
    # ══════════════════════════════════════════
    elif st.session_state.page == 'zone':
        go_home()
        st.markdown("<h1>Zone Comparison</h1>",unsafe_allow_html=True)
        st.markdown("<p style='color:#5a8099;margin-top:-10px'>Compare water quality across 4 zones</p>",unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Enter Values for 4 Zones</div>",unsafe_allow_html=True)

        zones=[]
        cols=st.columns(4)
        default_names=["Zone A","Zone B","Zone C","Zone D"]
        for i,(col,dname) in enumerate(zip(cols,default_names)):
            with col:
                st.markdown(f"<div style='color:#00d4ff;font-weight:700;margin-bottom:8px;'>{dname}</div>",unsafe_allow_html=True)
                name    =st.text_input("Name",value=dname,key=f"zn_{i}")
                bacteria=st.slider("Bacteria",0.0,1.0, 0.0,0.01,key=f"bact_{i}")
                lead    =st.slider("Lead",    0.0,0.1, 0.0,0.001,key=f"lead_{i}")
                arsenic =st.slider("Arsenic", 0.0,0.5, 0.0,0.001,key=f"arse_{i}")
                nitrates=st.slider("Nitrates",0.0,20.0,5.0,0.1,  key=f"nitr_{i}")
                zones.append({"name":name,"bacteria":bacteria,"lead":lead,"arsenic":arsenic,"nitrates":nitrates})

        st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
        if st.button("Compare All Zones",use_container_width=True):
            for z in zones:
                score=0
                if z['bacteria']>0:     score+=40
                if z['lead']>0.015:     score+=25
                if z['arsenic']>0.01:   score+=25
                if z['nitrates']>10:    score+=10
                z['risk_score']=min(score,100)
                if score>=70:   z['level']="CRITICAL"; z['color']=RED;  z['icon']="CRITICAL"
                elif score>=50: z['level']="HIGH";     z['color']=ORG;  z['icon']="HIGH"
                elif score>=30: z['level']="MODERATE"; z['color']=YLW;  z['icon']="MODERATE"
                else:           z['level']="SAFE";     z['color']=GRN;  z['icon']="SAFE"

            zdf=pd.DataFrame(zones)
            fig=go.Figure(go.Bar(x=zdf['name'],y=zdf['risk_score'],
                marker_color=[z['color'] for z in zones],
                text=[f"{z['risk_score']}/100" for z in zones],
                textposition='outside',textfont=dict(color='white',size=13)))
            fig.add_hline(y=50,line_dash="dash",line_color=YLW,annotation_text="Risk Threshold")
            fig=theme(fig,"Zone-wise Disease Risk Score Comparison")
            fig.update_layout(height=350,yaxis=dict(range=[0,120]))
            st.plotly_chart(fig,use_container_width=True)

            st.markdown("<div class='section-title'>Zone Risk Summary</div>",unsafe_allow_html=True)
            rcols=st.columns(4)
            for col,z in zip(rcols,zones):
                col.markdown(f"<div class='metric-card'><div style='font-size:16px;font-weight:700;color:{z['color']};margin:6px 0'>{z['name']}</div><div style='font-size:24px;font-weight:700;color:{z['color']}'>{z['risk_score']}/100</div><div style='font-size:12px;color:#5a8099;margin-top:4px'>{z['level']}</div></div>",unsafe_allow_html=True)

            most=max(zones,key=lambda z:z['risk_score'])
            safe=min(zones,key=lambda z:z['risk_score'])
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown(f"<div class='alert-red'>MOST AT-RISK: {most['name']} - Risk Score {most['risk_score']}/100 - Immediate action required!</div>",unsafe_allow_html=True)
            st.markdown(f"<div class='alert-green'>SAFEST ZONE: {safe['name']} - Risk Score {safe['risk_score']}/100</div>",unsafe_allow_html=True)

            categories=['Bacteria','Lead x10','Arsenic x20','Nitrates/20']
            fig2=go.Figure()
            zcols_r=[BLUE,GRN,RED,YLW]
            for z,col in zip(zones,zcols_r):
                vals=[z['bacteria'],z['lead']*10,z['arsenic']*20,z['nitrates']/20]
                vals_closed=vals+[vals[0]]
                cats_closed=categories+[categories[0]]
                fig2.add_trace(go.Scatterpolar(r=vals_closed,theta=cats_closed,
                    fill='toself',name=z['name'],line=dict(color=col,width=2)))
            fig2.update_layout(polar=dict(bgcolor=PBG,
                radialaxis=dict(visible=True,color=FC,gridcolor=GC),
                angularaxis=dict(color=FC)),
                paper_bgcolor=PPG,font_color=FC,
                title=dict(text="Zone Contamination Radar Chart",font=dict(color='#e2f0f7',size=15)),
                legend=dict(bgcolor='rgba(0,0,0,0)'),margin=dict(l=40,r=40,t=60,b=40))
            st.plotly_chart(fig2,use_container_width=True)

    # ══════════════════════════════════════════
    # ADMIN PANEL
    # ══════════════════════════════════════════
    elif st.session_state.page == 'admin':
        go_home()
        if st.session_state.role != "Admin":
            st.markdown("<div class='alert-red'>Access Denied! Admin only.</div>",unsafe_allow_html=True)
        else:
            st.markdown("<h1>Admin Panel</h1>",unsafe_allow_html=True)
            st.markdown("<p style='color:#5a8099;margin-top:-10px'>Manage users and view all system data</p>",unsafe_allow_html=True)
            st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)

            # Stats
            all_pred=get_predictions()
            all_alerts=get_alerts()
            all_users=get_all_users()

            c1,c2,c3=st.columns(3)
            c1.markdown(f"<div class='metric-card'><div class='metric-value'>{len(all_users)}</div><div class='metric-label'>Total Users</div></div>",unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><div class='metric-value'>{len(all_pred)}</div><div class='metric-label'>Total Predictions</div></div>",unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><div class='metric-value'>{len(all_alerts)}</div><div class='metric-label'>Total Alerts</div></div>",unsafe_allow_html=True)

            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<div class='section-title'>All Registered Users</div>",unsafe_allow_html=True)
            st.dataframe(all_users,use_container_width=True,hide_index=True)

            st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
            st.markdown("<div class='section-title'>All Predictions (All Officers)</div>",unsafe_allow_html=True)
            if all_pred.empty:
                st.markdown("<div class='alert-yellow'>No predictions yet.</div>",unsafe_allow_html=True)
            else:
                st.dataframe(all_pred,use_container_width=True,hide_index=True)

            st.markdown("<hr style='border-color:#0e3a56'>",unsafe_allow_html=True)
            st.markdown("<div class='section-title'>All Alerts (All Officers)</div>",unsafe_allow_html=True)
            if all_alerts.empty:
                st.markdown("<div class='alert-yellow'>No alerts yet.</div>",unsafe_allow_html=True)
            else:
                st.dataframe(all_alerts,use_container_width=True,hide_index=True)