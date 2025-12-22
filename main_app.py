import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
from google import genai
from tools.boxscore2_0 import BoxScoreMaker
from tools.mongo_tools import save_document, get_documents_from_mongo
from utils.mongo_utils import init_mongo
import json
# ---------- Load environment variables ----------
load_dotenv()

# ---------- MongoDB Initialization ----------
collection = init_mongo()

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

# ---------- Initialize Session States ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "form_mode" not in st.session_state:
    st.session_state.form_mode = "Login"
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "page" not in st.session_state:
    st.session_state.page = "Conversations"
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL = "gemini-2.0-flash-lite"
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

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
    st.sidebar.image(IMAGES_DIR / "logo_sys.png")
    st.sidebar.write(f"Welcome, **{st.session_state.user}**")
    
    if st.sidebar.button("Statistics"): 
        st.session_state.page, st.session_state.show_results = "Statstics", False
        st.rerun()
    if st.sidebar.button("Comparison"): 
        st.session_state.page, st.session_state.show_results = "Comparison", False
        st.rerun()
    if st.sidebar.button("Conversations"): 
        st.session_state.page, st.session_state.show_results = "Conversations", False
        st.rerun()
    if st.sidebar.button("Practice"):
        st.session_state.page, st.session_state.show_results = "Practice", False
        st.rerun()
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
            model=MODEL, config={"temperature": 0.7}
        )
    if "messages" not in st.session_state: st.session_state.messages = []

    # --- PAGES ---
    if st.session_state.page == "Statstics":
        show_header(hide_bg=st.session_state.show_results)
        st.markdown("<h1 style='color: orange;'>STATYOURSQUAD</h1>", unsafe_allow_html=True)
        with st.form("stats_form"):
            query = st.text_input("Enter team/player:")
            if st.form_submit_button("Get Stats 🏀") and query:
                st.session_state.show_results = True
                st.rerun()
        if st.session_state.show_results:
            response = st.session_state.gemini_chat.send_message(f"Stats for {query}")
            st.write(response.text)

    elif st.session_state.page == "Comparison":
        show_header(hide_bg=st.session_state.show_results)
        p1 = st.text_input("Player 1")
        p2 = st.text_input("Player 2")
        if st.button("Compare 🏀") and p1 and p2:
            st.session_state.show_results = True
            st.rerun()
        if st.session_state.show_results:
            response = st.session_state.gemini_chat.send_message(f"Compare {p1} and {p2}")
            st.write(response.text)

    elif st.session_state.page == "Conversations":
        show_header(hide_bg=st.session_state.show_results)
        
        st.markdown("""
        <style>
        div[data-testid='stPopover'] { position: fixed; bottom: 31px; left: calc(50% - 335px); z-index: 999999; }
        div[data-testid='stPopover'] button { background: transparent !important; border: none !important; font-size: 20px !important; color: #808080 !important; }
        [data-testid='stChatInput'] textarea { padding-left: 50px !important; }
        </style>""", unsafe_allow_html=True)

        # --- File uploader popover ---
        with st.popover("ADD FILES➕"):
            uploaded_image = st.file_uploader("Images", type=["png", "jpg", "jpeg"], key="c_img")
            uploaded_pdf = st.file_uploader("Documents", type=["pdf"], key="c_doc")

        # --- Process uploaded file ---
        uploaded_file = uploaded_image or uploaded_pdf
        if uploaded_file is not None:
            bsm = BoxScoreMaker(client=st.session_state.gemini_client, model=MODEL)
            boxscore_json = bsm.get_stats(uploaded_file)  # directly get JSON dict
            doc_id = save_document(boxscore_json)  # save to Mongo

            # First AI analysis message
            team_name = list(boxscore_json.keys())[0]
            json_str_for_ai = json.dumps(boxscore_json)
            prompt = f"Here is a basketball boxscore for {team_name}. Summarize key insights."
            response = st.session_state.gemini_chat.send_message(prompt)

            # Add AI's analysis to chat
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.session_state.show_results = True
            st.success(f"Boxscore saved to MongoDB! Document ID: {doc_id}")

        # --- User input ---
        if user_input := st.chat_input("Ask your question here..."):
            st.session_state.show_results = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Send user's message to AI
            response = st.session_state.gemini_chat.send_message(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        # --- Display chat history ---
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    elif st.session_state.page == "Practice":
        show_header(hide_bg=st.session_state.show_results)
        mat = st.text_input("Equipment (What do you have?)")
        num = st.text_input("Amount")
        if st.button("Start 🏀") and mat and num:
            st.session_state.show_results = True
            st.rerun()
        if st.session_state.show_results:
            response = st.session_state.gemini_chat.send_message(f"Practice drills for {num} {mat}")
            st.write(response.text)
