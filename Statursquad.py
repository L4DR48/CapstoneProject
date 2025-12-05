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

# ---------- Streamlit App ----------
st.set_page_config(page_title="STATYOURSQUAD", page_icon="🏀", layout="centered")


st.markdown(
    f"""
    <style>
    .side-img-left {{
        position: fixed;
        top: 35%;
        left: 8%;
        width: 320px;
        opacity: 0.9;
        z-index: 99;
    }}

    .side-img-right {{
        position: fixed;
        top: 35%;
        right: 8%;
        width: 320px;
        opacity: 0.9;
        z-index: 99;
    }}
    </style>
    <img src="data:image/png;base64,{base64.b64encode(open(r'C:\Users\pc\Documents\GitHub\CapstoneProject\mascot.png','rb').read()).decode()}" class="side-img-left">
    <img src="data:image/png;base64,{base64.b64encode(open(r'C:\Users\pc\Documents\GitHub\CapstoneProject\mascot.png','rb').read()).decode()}" class="side-img-right">
    """,
    unsafe_allow_html=True
)


# --- Logo at the top-left ---
logo_path = r"C:\Users\pc\Documents\GitHub\CapstoneProject\logo_sys.png"

logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()

st.markdown(
    f"""
    <div style="display: flex; align-items: left;">
        <img src="data:image/png;base64,{logo_base64}" 
             style="height:80px; margin-right: 15px;">
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
    <hr style='margin-top: 2rem; bottom: 1rem;' />
    <p style='text-align: center; color: gray; font-size: 0.9rem;'>
        Powered by  Sunshine Group
    </p>
    """,
    unsafe_allow_html=True,
)
