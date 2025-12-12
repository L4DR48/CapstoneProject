import streamlit as st
from typing import List, Dict
import time
import base64

# ---------- Simulated Gemini Service ----------
def fetch_info(query: str, search_type: str) -> Dict[str, any]:
    """
    Simulates fetching sports information like the Gemini service.
    Replace this with a real API call later if needed.
    """
    time.sleep(2)  # simulate API delay
    
    # Dummy data
    data = {
        "text": f"Here’s some detailed information about '{query}' ({search_type})."
    }
    return data


def floating_stickers():
    # ---- 4 sticker image paths ----
    sticker_paths = [
        r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\nba.png",
        r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\basketballworldcup.png",
        r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\nba2k.png",
        r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\wearebasket.png",

    ]

    # ---- Convert all images to Base64 ----
    encoded_imgs = []
    for path in sticker_paths:
        with open(path, "rb") as f:
            encoded_imgs.append(base64.b64encode(f.read()).decode())

    # ---- Inject HTML/CSS ----
    st.markdown(
        f"""
        <style>
        .floating-sticker {{
            position: fixed;
            width: 150px;
            opacity: 0.85;
            
            z-index: 1;
        }}

        /* ---- Sticker positions ---- */
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


# --- Sidebar Navigation ---
st.sidebar.image(r'C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\logo_sys.png', use_container_width=False)


if "page" not in st.session_state:
    st.session_state.page = "Conversations"

if st.sidebar.button("Statstics"):
    st.session_state.page = "Statstics"

if st.sidebar.button("Comparison"):
    st.session_state.page = "Comparison"

if st.sidebar.button("Conversations"):
    st.session_state.page = "Conversations"

page = st.session_state.page


if page == "Statstics":
    st.markdown(
    f"""
    <style>
    /* Base positioning (sidebar closed) */
    .side-img{{
        position: fixed;
        top: 25%;
        left: 120px;  /* moved from 8% to fixed px so sidebar push is predictable */
        width: 360px;
        opacity: 0.9;
        z-index: 99;
        
    }}

    /* When sidebar expands — Streamlit adds aria-expanded="true" */
    [data-testid="stSidebar"][aria-expanded="true"] ~ div .side-img {{
        left: 255px;  /* shift the image to the right to avoid overlap */
    }}
    </style>

    <img src="data:image/png;base64,{base64.b64encode(open(r'C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\mascot.png','rb').read()).decode()}" class="side-img">
    """,
    unsafe_allow_html=True
)



    # --- Logo at the top-left ---
    logo_path = r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\logo_sys.png"

    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" 
                style="height:150px; margin-right: 40px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Title and Description ---
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


    # --- Search Form ---
    with st.form("search_form"):
        query = st.text_input("Enter a team or player name:")
        submitted = st.form_submit_button("Search 🏀")

    # --- Results Area ---
    if submitted:
        if not query.strip():
            st.error("Please enter a search query.")
        else:
            with st.spinner("Fetching information..."):
                try:
                    result = fetch_info(query, search_type)
                    st.success("Results fetched successfully!")
                    
                    # Display Result
                    st.markdown("### 🏆 Result")
                    st.write(result["text"])

                    # Display Sources
                    st.markdown("### 📚 Sources")
                    st.write("You will get your answers soon enough, boy.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # --- Footer ---
    st.markdown(
        """
        <hr style='margin-bottom: 2rem; bottom: 1rem;' />
        <p style='text-align: center; color: gray; font-size: 0.9rem;'>
            Powered by  Sunshine Group
        </p>
        """,
        unsafe_allow_html=True,
    )

    floating_stickers()


elif page == "Comparison":

    st.markdown(
    f"""
    <style>
    /* Base positioning (sidebar closed) */
    .side-img{{
        position: fixed;
        top: 25%;
        left: 120px;  /* moved from 8% to fixed px so sidebar push is predictable */
        width: 360px;
        opacity: 0.9;
        z-index: 99;
        
    }}

    /* When sidebar expands — Streamlit adds aria-expanded="true" */
    [data-testid="stSidebar"][aria-expanded="true"] ~ div .side-img {{
        left: 255px;  /* shift the image to the right to avoid overlap */
    }}
    </style>

    <img src="data:image/png;base64,{base64.b64encode(open(r'C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\mascot.png','rb').read()).decode()}" class="side-img">
    """,
    unsafe_allow_html=True
)
    # --- Logo at the top-left ---
    logo_path = r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\logo_sys.png"

    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" 
                style="height:150px; margin-right: 40px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.title("Player Comparison🏀")

    player1 = st.text_input("Player 1")
    player2 = st.text_input("Player 2")

    compare_btn = st.button("Compare 🏀")

    if compare_btn:
        if not player1 or not player2:
            st.error("Please enter both player names.")
        else:
            st.success(f"Comparing {player1} vs {player2}...")

    floating_stickers()


elif page == "Conversations":
    st.markdown(
    f"""
    <style>
    /* Base positioning (sidebar closed) */
    .side-img{{
        position: fixed;
        top: 25%;
        left: 120px;  /* moved from 8% to fixed px so sidebar push is predictable */
        width: 360px;
        opacity: 0.9;
        z-index: 99;
        
    }}

    /* When sidebar expands — Streamlit adds aria-expanded="true" */
    [data-testid="stSidebar"][aria-expanded="true"] ~ div .side-img {{
        left: 255px;  /* shift the image to the right to avoid overlap */
    }}
    </style>

    <img src="data:image/png;base64,{base64.b64encode(open(r'C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\mascot.png','rb').read()).decode()}" class="side-img">
    """,
    unsafe_allow_html=True
)



    # --- Logo at the top-left ---
    logo_path = r"C:\Users\FNAC\OneDrive\Documents\GitHub\CapstoneProject\images\logo_sys.png"

    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" 
                style="height:150px; margin-right: 40px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💬 STATYOURSQUAD")

    # Search-style input bar
    user_input = st.text_input(
        " ",                         # hides label
        placeholder="Enter your prompt here...",  
        key="prompt_input"
    )

    if st.button(" SEND🏀"):
        if not user_input.strip():
            st.error("Please enter a prompt.")
        else:
            st.success(f"You asked: {user_input}")

    floating_stickers()
