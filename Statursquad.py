import streamlit as st
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
from google import genai

# ---------- Load environment variables ----------
load_dotenv()

# ---------- Gemini Client Initialization ----------
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL = "gemini-2.5-flash-lite"

# ---------- Project Paths ----------
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

def img_to_base64(filename: str) -> str:
    """Load image from images/ and return base64 string."""
    path = IMAGES_DIR / filename
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def floating_stickers():
    """Floating stickers for all pages."""
    sticker_files = [
        "nba.png",
        "basketballworldcup.png",
        "nba2k.png",
        "wearebasket.png",
    ]
    encoded_imgs = [img_to_base64(name) for name in sticker_files]

    st.markdown(
        f"""
        <style>
        .floating-sticker {{
            position: fixed;
            width: 150px;
            opacity: 0.85;
            z-index: 1;
        }}
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

# ---------- Streamlit App ----------
st.set_page_config(page_title="STATYOURSQUAD", page_icon="🏀", layout="centered")

# Sidebar logo
st.sidebar.image(IMAGES_DIR / "logo_sys.png")

# --- Sidebar Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "Conversations"

if st.sidebar.button("Statstics"):
    st.session_state.page = "Statstics"
if st.sidebar.button("Comparison"):
    st.session_state.page = "Comparison"
if st.sidebar.button("Conversations"):
    st.session_state.page = "Conversations"

page = st.session_state.page

# --- Initialize Gemini Chat for Conversation page ---
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
        model=MODEL,
        config={
            "temperature": 0.7,
            "system_instruction": "You are a helpful assistant."
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Page Header Helper ---
def show_header():
    # Mascot side image
    st.markdown(
        f"""
        <style>
        .side-img {{
            position: fixed;
            top: 25%;
            left: 120px;
            width: 360px;
            opacity: 0.9;
            z-index: 99;
        }}
        [data-testid="stSidebar"][aria-expanded="true"] ~ div .side-img {{
            left: 255px;
        }}
        </style>
        <img src="data:image/png;base64,{img_to_base64('mascot.png')}" class="side-img">
        """,
        unsafe_allow_html=True
    )

    # Logo top-left
    logo_base64 = img_to_base64("logo_sys.png")
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" style="height:150px; margin-right: 40px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# --- STATISTICS PAGE ---
if page == "Statstics":
    show_header()
    st.markdown(
        """
        <h1 style='text-align: left; 
                background: -webkit-linear-gradient(#10b981, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: orange;
                font-size: 3rem;'>
            STATYOURSQUAD
        </h1>
        <p style='text-align: left; color: white; font-size: 1.1rem;'>
            Instant insights on your favorite teams and players.
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("stats_form"):
        query = st.text_input("Enter a team or player name for stats:")
        submitted = st.form_submit_button("Get Stats 🏀")

    if submitted:
        if not query.strip():
            st.error("Please enter a search query.")
        else:
            with st.spinner("Fetching statistics..."):
                try:
                    # Send prompt to Gemini
                    prompt = f"Provide detailed basketball statistics about {query}."
                    response = st.session_state.gemini_chat.send_message(prompt)
                    st.success("Results fetched successfully!")
                    st.markdown("### 🏆 Result")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error fetching stats: {e}")

    floating_stickers()

# --- COMPARISON PAGE ---
elif page == "Comparison":
    show_header()
    st.title("Player Comparison🏀")

    player1 = st.text_input("Player 1")
    player2 = st.text_input("Player 2")
    compare_btn = st.button("Compare 🏀")

    if compare_btn:
        if not player1 or not player2:
            st.error("Please enter both player names.")
        else:
            with st.spinner(f"Comparing {player1} vs {player2}..."):
                try:
                    # Gemini prompt for comparison
                    prompt = f"Compare the basketball performance of {player1} and {player2} in detail."
                    response = st.session_state.gemini_chat.send_message(prompt)
                    st.success("Comparison complete!")
                    st.markdown(f"### 🏀 Comparison: {player1} vs {player2}")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error comparing players: {e}")

    floating_stickers()

# --- CONVERSATIONS PAGE ---
elif page == "Conversations":
    show_header()
    st.markdown("### 💬 STATYOURSQUAD")

    # Chat input
    if user_input := st.chat_input("Ask your question here...", key="chat_input"):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Gemini response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.gemini_chat.send_message(user_input)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")

    # Display previous messages
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    floating_stickers()

