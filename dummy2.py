import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
from google import genai
import pandas as pd
from tools.boxscore2_0 import BoxScoreMaker
from tools.boxscore_analysis import BoxScoreAnalysis 
from utils.mongo_utils import store_boxscore
from tools.mongo_tools import get_team_boxscores, extract_players_from_games
from tools.practice import PracticeGen
from utils.langfuse_utils import init_tracing
from langfuse import observe, Langfuse

# ---------- Load environment variables ----------
load_dotenv()

# ---------- Initialize Langfuse Tracing ----------
LANGFUSE_ENABLED = init_tracing()

# ---------- Langfuse client singleton ----------
_langfuse_client = None
def get_client():
    global _langfuse_client
    if _langfuse_client is None:
        _langfuse_client = Langfuse()
    return _langfuse_client

# ---------- Database Functions ----------
def create_usertable():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    hashed_pswd = hashlib.sha256(str.encode(password)).hexdigest()
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, hashed_pswd))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    hashed_pswd = hashlib.sha256(str.encode(password)).hexdigest()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, hashed_pswd))
    data = c.fetchall()
    conn.close()
    return data

# ---------- Global Constants ----------
MODEL = "gemini-2.5-flash-lite"
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

# ---------- Initialize Session States ----------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "form_mode" not in st.session_state: st.session_state.form_mode = "Login"
if "show_results" not in st.session_state: st.session_state.show_results = False
if "page" not in st.session_state: st.session_state.page = "Conversations"
if "gemini_client" not in st.session_state: st.session_state.gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
if "boxscore_maker" not in st.session_state: st.session_state.boxscore_maker = BoxScoreMaker(st.session_state.gemini_client, MODEL)
if "boxscore_analysis" not in st.session_state: st.session_state.boxscore_analysis = BoxScoreAnalysis(st.session_state.gemini_client, MODEL)
if "practice_gen" not in st.session_state: st.session_state.practice_gen = PracticeGen(st.session_state.gemini_client, MODEL)

# ---------- Helper Functions ----------
def img_to_base64(filename: str) -> str:
    path = IMAGES_DIR / filename
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def show_header(hide_bg=False):
    opacity = "0" if hide_bg else "1"
    try:
        bg_data = img_to_base64('court.png')
        logo_data = img_to_base64('logo_sys.png')
    except Exception as e:
        st.error(f"Image Error: {e}")
        return
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{ background-color: #0E1117; }}
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: url("data:image/png;base64,{bg_data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: {opacity};
            transition: opacity 0.8s ease-in-out;
            z-index: 0;
        }}
        [data-testid="stHeader"], [data-testid="stApp"], [data-testid="stToolbar"] {{
            background: rgba(0,0,0,0) !important;
        }}
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.75);
            border-radius: 25px;
            padding: 50px;
            margin-top: 15vh;
            z-index: 1;
            text-align: center;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        }}
        .stTextInput, .stButton {{ text-align: left; }}
        h1, p {{ text-align: center !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )
    logo_base64 = img_to_base64("logo_sys.png")
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 120px;">
            <img src="data:image/png;base64,{logo_base64}" style="height:200px;">
        </div>
        """,
        unsafe_allow_html=True
    )

def boxscore_to_tables(boxscore: dict):
    team, data = next(iter(boxscore.items()))
    players_df = pd.DataFrame(data.get("Players", []))
    scores_rows = []
    for entry in data.get("Scores", []):
        quarter = list(entry.keys())[0]
        home = entry[quarter][0].get("Home") if len(entry[quarter]) > 0 else None
        away = entry[quarter][1].get("Away") if len(entry[quarter]) > 1 else None
        scores_rows.append({"Period": quarter,"Home": home,"Away": away})
    scores_df = pd.DataFrame(scores_rows)
    return team, players_df, scores_df

# ---------- Traced Functions ----------
@observe(name="gemini_chat_send")
def send_traced_message(message: str, chat_session, user_id: str | None = None) -> str:
    """Send a message in Gemini chat session (Langfuse-traced)."""
    if user_id:
        langfuse = get_client()
        langfuse.update_current_trace(
            user_id=user_id,
            tags=["streamlit", "chat", "production"],
            metadata={"model": MODEL, "environment": "streamlit"},
        )
    response = chat_session.send_message(message)
    return response.text

@observe(name="boxscore_analysis")
def analyze_boxscore(boxscore, n_insights: int, focus: str):
    return st.session_state.boxscore_analysis.boxscore_analysis(
        boxscore, n_insights=n_insights, focus=focus
    )

@observe(name="practice_generation")
def generate_practice(level, time, focus, venue, equip_dict):
    return st.session_state.practice_gen.practice_planner(
        level, time, focus, venue, equip_dict
    )

@observe(name="boxscore_extraction")
def extract_boxscore(uploaded, team_name):
    return st.session_state.boxscore_maker.boxscore_from_upload(uploaded, team=team_name)

# ---------- Page Config ----------
st.set_page_config(page_title="STATYOURSQUAD", page_icon="🏀", layout="centered")
create_usertable()

# =========================================================
# 1. LOGIN SCREEN
# =========================================================
if not st.session_state.logged_in:
    show_header(hide_bg=False)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader(st.session_state.form_mode)
            user = st.text_input("Username")
            pswd = st.text_input("Password", type="password")
            if st.session_state.form_mode == "Sign Up":
                if st.button("Create Account", use_container_width=True):
                    if user and pswd:
                        add_userdata(user, pswd)
                        st.success("Account created! Log In now.")
                        st.session_state.form_mode = "Login"
                        st.rerun()
                st.button("Back", on_click=lambda: st.session_state.update({"form_mode": "Login"}))
            else:
                if st.button("Login", use_container_width=True):
                    if login_user(user, pswd):
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                st.button("Need an account? Sign Up", on_click=lambda: st.session_state.update({"form_mode": "Sign Up"}))

# =========================================================
# 2. MAIN APP
# =========================================================
else:
    # Sidebar
    st.sidebar.image(IMAGES_DIR / "logo_sys.png")
    st.sidebar.write(f"Welcome, **{st.session_state.user}**")
    for page_name in ["Insights","BoxScoreAnalysis","Practice","Conversations"]:
        if st.sidebar.button(page_name):
            st.session_state.page = page_name
            st.session_state.show_results = False
            st.rerun()
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Initialize Gemini Chat session if not exist
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
            model=MODEL, config={"temperature": 0.7}
        )
    if "messages" not in st.session_state: st.session_state.messages = []

    # -------------------- Page Routing --------------------
    if st.session_state.page == "Conversations":
        show_header(hide_bg=st.session_state.show_results)
        if user_input := st.chat_input("Ask your question here..."):
            st.session_state.show_results = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                response_text = send_traced_message(
                    message=user_input,
                    chat_session=st.session_state.gemini_chat,
                    user_id=st.session_state.get("user")
                )
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Chat error: {e}")
            st.rerun()
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    elif st.session_state.page == "BoxScoreAnalysis":
        show_header(hide_bg=st.session_state.show_results)
        uploaded = st.file_uploader("Upload boxscore", type=["png","jpg","jpeg","pdf"])
        team = st.text_input("Team Abbreviation")
        opps = st.text_input("Opponent Abbreviation")
        if uploaded and st.button("Extract Boxscore 🏀"):
            try:
                st.session_state.boxscore = extract_boxscore(uploaded, team_name="My Team")
                st.success("✅ Boxscore extracted successfully")
            except Exception as e:
                st.error(f"Boxscore extraction failed: {e}")
        if "boxscore" in st.session_state:
            if st.button("Save to MongoDB") and team and opps:
                inserted_id = store_boxscore(st.session_state.boxscore, team, opps)
                st.success(f"Boxscore stored with ID: {inserted_id}")
            team_name, players_df, scores_df = boxscore_to_tables(st.session_state.boxscore)
            st.subheader(f"🏀 {team_name} – Score by Period")
            st.table(scores_df)
            st.subheader("👤 Player Boxscore")
            st.dataframe(players_df, use_container_width=True, hide_index=True)
            with st.form("analysis_form"):
                insights = st.slider("Number of insights", 1, 10, 5)
                focus = st.text_input("Focus (Offense, Defense, Offense and Defense,...)")
                analyze_button = st.form_submit_button("Analyze Boxscore 📊")
            if analyze_button:
                with st.spinner("Analyzing boxscore…"):
                    analysis_text = analyze_boxscore(st.session_state.boxscore, insights, focus)
                    st.text_area("Analysis", analysis_text, height=300)
            if st.button("Suggest practice drills"):
                weaknesses = st.session_state.boxscore_analysis.extract_weaknesses(st.session_state.boxscore)
                with st.spinner("Generating drills..."):
                    practice_text = st.session_state.boxscore_analysis.drills_suggestor(weaknesses)
                    st.text_area("Practice Drills", practice_text, height=300)

    elif st.session_state.page == "Practice":
        show_header(hide_bg=st.session_state.show_results)
        st.session_state.level = st.selectbox("Team Level",["U10","U12","U14","U16","U18","Amateur","SemiPro","Pro"])
        st.session_state.focus = st.selectbox("Training Focus",["Offense","Defense","Rebounding","Passing","Shooting","Hustle","Finishing","Everything"])
        st.session_state.practice_time = st.number_input("Practice Duration (minutes)", min_value=30, step=15)
        st.session_state.practice_venue = st.selectbox("Venue",["Half Court","Full Court","Two Courts","Three Courts"])
        n_equip = st.number_input("Add Equipment/Personnel", min_value=0, step=1)
        if "equip_dict" not in st.session_state: st.session_state.equip_dict = {}
        for i in range(int(n_equip)):
            mat = st.text_input(f"Equipment/Personnel {i+1}", key=f"mat{i}")
            num = st.number_input(f"Amount {i+1}", key=f"num{i}", step=1)
            st.session_state.equip_dict[mat] = num
        if st.button("Generate plan 🏀") and st.session_state.equip_dict:
            with st.spinner("Generating drills..."):
                practice_plan = generate_practice(
                    st.session_state.level, st.session_state.practice_time,
                    st.session_state.focus, st.session_state.practice_venue,
                    st.session_state.equip_dict
                )
                st.text_area("Practice Drills", practice_plan, height=300)
                
    elif st.session_state.page == "Conversations":
        show_header(hide_bg=st.session_state.show_results)
        
        st.markdown(
            "<style>div[data-testid='stPopover'] { position: fixed; bottom: 31px; left: calc(50% - 335px); z-index: 999999; } "
            "div[data-testid='stPopover'] button { background: transparent !important; border: none !important; font-size: 20px !important; color: #808080 !important; } "
            "[data-testid='stChatInput'] textarea { padding-left: 50px !important; }</style>", 
            unsafe_allow_html=True
        )

        if user_input := st.chat_input("Ask your question here..."):
            st.session_state.show_results = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # --- Use traced wrapper instead of raw send_message ---
            try:
                response_text = send_traced_message(
                    message=user_input,
                    chat_session=st.session_state.gemini_chat,
                    user_id=st.session_state.get("user")
                )
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Chat error: {e}")
            
            st.rerun()

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    