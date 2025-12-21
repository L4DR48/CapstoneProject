import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
from google import genai

# Langfuse
from langfuse.decorators import observe
from langfuse import Langfuse

from utils.langfuse_utils import init_tracing
from utils.mongo_utils import init_mongo

# ---------- Load environment variables ----------
load_dotenv()

# ---------- Initialize Langfuse Tracing ----------
init_tracing()

# ---------- Langfuse client singleton ----------
_langfuse_client = None

def get_client():
    global _langfuse_client
    if _langfuse_client is None:
        _langfuse_client = Langfuse()
    return _langfuse_client

# ---------- Initialize MongoDB Collection ----------
if "mongo_collection" not in st.session_state:
    st.session_state.mongo_collection = init_mongo()

collection = st.session_state.mongo_collection

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
    c.execute(
        'INSERT INTO userstable(username, password) VALUES (?,?)',
        (username, hashed_pswd)
    )
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    hashed_pswd = hashlib.sha256(str.encode(password)).hexdigest()
    c.execute(
        'SELECT * FROM userstable WHERE username =? AND password = ?',
        (username, hashed_pswd)
    )
    data = c.fetchall()
    conn.close()
    return data

# ---------- Initialize Session States ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "form_mode" not in st.session_state:
    st.session_state.form_mode = "Login"

if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )

MODEL = "gemini-2.5-flash-lite"
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

# ============================================================================
# TRACED CHAT FUNCTION
# ============================================================================

@observe(name="gemini_chat_send")
def send_traced_message(
    message: str,
    chat_session,
    user_id: str | None = None
) -> str:
    """Send a message in Gemini chat session (Langfuse-traced)."""

    if user_id:
        langfuse = get_client()
        langfuse.update_current_trace(
            user_id=user_id,
            tags=["streamlit", "chat", "production"],
            metadata={
                "model": MODEL,
                "environment": "streamlit",
            },
        )

    response = chat_session.send_message(message)
    return response.text

# ---------- Helper Functions ----------
def img_to_base64(filename: str) -> str:
    path = IMAGES_DIR / filename
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def floating_stickers():
    sticker_files = ["nba.png", "basketballworldcup.png", "nba2k.png", "wearebasket.png"]
    try:
        encoded_imgs = [img_to_base64(name) for name in sticker_files]
        st.markdown(
            f"""
            <style>
            .floating-sticker {{ position: fixed; width: 150px; opacity: 0.85; z-index: 1; }}
            .sticker-1 {{ top: 14%; right: 8%; transform: rotate(-4deg); }}
            .sticker-2 {{ top: 53%; right: 8%; transform: rotate(3deg); }}
            .sticker-3 {{ top: 33%; right: 8%; transform: rotate(5deg); }}
            .sticker-4 {{ top: 83%; right: 6%; transform: rotate(5deg); }}
            </style>
            <img src="data:image/png;base64,{encoded_imgs[0]}" class="floating-sticker sticker-1" />
            <img src="data:image/png;base64,{encoded_imgs[1]}" class="floating-sticker sticker-2" />
            <img src="data:image/png;base64,{encoded_imgs[2]}" class="floating-sticker sticker-3" />
            <img src="data:image/png;base64,{encoded_imgs[3]}" class="floating-sticker sticker-4" />
            """,
            unsafe_allow_html=True
        )
    except:
        pass

def show_header():
    st.markdown(
        f"""
        <style>
        .side-img {{ position: fixed; top: 25%; left: 120px; width: 360px; opacity: 0.9; z-index: 99; }}
        [data-testid="stSidebar"][aria-expanded="true"] ~ div .side-img {{ left: 255px; }}
        </style>
        <img src="data:image/png;base64,{img_to_base64('mascot.png')}" class="side-img">
        """,
        unsafe_allow_html=True
    )

    logo_base64 = img_to_base64("logo_sys.png")
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" style="height:150px; margin-right: 40px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Page Config ----------
st.set_page_config(
    page_title="STATYOURSQUAD",
    page_icon="🏀",
    layout="centered"
)

create_usertable()

# =========================================================
# 1. LOGIN SCREEN
# =========================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image(str(IMAGES_DIR / "logo_sys.png"), width=200)
        except:
            st.warning("Logo not found in images/ folder")

        st.markdown(
            "<h1 style='text-align: center;'>STATYOURSQUAD</h1>",
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.subheader(st.session_state.form_mode)
            user = st.text_input("Username")
            pswd = st.text_input("Password", type="password")

            if st.session_state.form_mode == "Sign Up":
                if st.button("Create Account", use_container_width=True):
                    if user and pswd:
                        add_userdata(user, pswd)
                        st.success("Account created! Now please Log In.")
                        st.session_state.form_mode = "Login"
                        st.rerun()
                st.button(
                    "Back to Login",
                    on_click=lambda: st.session_state.update({"form_mode": "Login"})
                )
            else:
                if st.button("Login", use_container_width=True):
                    if login_user(user, pswd):
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid Username/Password")

                st.markdown("---")
                st.button(
                    "Don't have an account? Sign Up",
                    on_click=lambda: st.session_state.update({"form_mode": "Sign Up"})
                )

# =========================================================
# 2. MAIN APP
# =========================================================
else:
    st.sidebar.image(IMAGES_DIR / "logo_sys.png")
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")

    if "page" not in st.session_state:
        st.session_state.page = "Conversations"

    if st.sidebar.button("Statistics"):
        st.session_state.page = "Statstics"
    if st.sidebar.button("Comparison"):
        st.session_state.page = "Comparison"
    if st.sidebar.button("Conversations"):
        st.session_state.page = "Conversations"

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    page = st.session_state.page

    # Gemini chat init
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = (
            st.session_state.gemini_client.chats.create(
                model=MODEL,
                config={
                    "temperature": 0.7,
                    "system_instruction": "You are a helpful assistant.",
                },
            )
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------- ROUTING ----------
    if page == "Statstics":
        show_header()
        st.markdown(
            "<h1 style='color: orange;'>STATYOURSQUAD</h1>",
            unsafe_allow_html=True
        )

        with st.form("stats_form"):
            query = st.text_input("Enter a team or player name for stats:")
            if st.form_submit_button("Get Stats 🏀"):
                with st.spinner("Fetching..."):
                    assistant_text = send_traced_message(
                        f"Stats for {query}",
                        st.session_state.gemini_chat,
                        st.session_state.user,
                    )
                    st.write(assistant_text)

        floating_stickers()

    elif page == "Comparison":
        show_header()
        st.title("Player Comparison 🏀")

        p1 = st.text_input("Player 1")
        p2 = st.text_input("Player 2")

        if st.button("Compare 🏀"):
            assistant_text = send_traced_message(
                f"Compare {p1} and {p2}",
                st.session_state.gemini_chat,
                st.session_state.user,
            )
            st.write(assistant_text)

        floating_stickers()

    elif page == "Conversations":
        show_header()
        st.markdown("### 💬 STATYOURSQUAD")

        if user_input := st.chat_input("Ask your question here..."):
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            assistant_text = send_traced_message(
                user_input,
                st.session_state.gemini_chat,
                st.session_state.user,
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_text}
            )

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        floating_stickers()
