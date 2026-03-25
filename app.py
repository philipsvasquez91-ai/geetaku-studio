import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- API CONFIGURATION ---
# Pulling the secure key from Streamlit Cloud's secret vault
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")

def generate_image_url(prompt):
    """Generates a free image URL using Pollinations.ai"""
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"

# --- APP UI & LOGIC ---
st.set_page_config(page_title="GeeTaku-San Studio", layout="centered", page_icon="⛩️")

st.title("⛩️ GeeTaku-San Content Studio")
st.markdown("Your limitless mobile engine for anime, wrestling, and pop culture content.")

st.divider()

# --- 1. INPUT SECTION ---
st.header("1. Feed the Engine")
keyword = st.text_input("Enter a trending keyword:", placeholder="e.g., WrestleMania fallout, new Pokémon TCG set, Minecraft lore...")
uploaded_file = st.file_uploader("Or upload a text file/article for context:", type=['txt'])

st.divider()

# --- 2. OUTPUT CONTROL PANEL ---
st.header("2. Output Control Panel")
st.markdown("Select exactly what assets you need for this post:")

col1, col2, col3 = st.columns(3)
with col1:
    want_script = st.checkbox("📝 Viral Script", value=True)
with col2:
    want_images = st.checkbox("🎨 Image Assets", value=True)
with col3:
    want_storyboard = st.checkbox("🎬 Video Storyboard")

st.divider()

# --- 3. GENERATION TRIGGER ---
if st.button("🚀 Generate Content"):
    
    topic = keyword
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        topic = f"{keyword} (Context from file: {file_content[:500]}...)"
        
    if not topic:
        st.warning("Please enter a keyword or upload a file to get started!")
    else:
        st.success("Processing your request...")

        # -- MODULE A: SCRIPT GENERATION --
        if want_script:
            st.subheader("📝 Your TikTok Script")
            prompt = f"""
            You are the head content strategist for 'GeeTaku-San', a fast-paced TikTok channel dedicated to pop culture, anime, and professional wrestling.
            
            Topic: {topic}
            
            Write a highly engaging, 60-second TikTok script for this topic. 
            You must include:
            1. Hook: A controversial or highly engaging opening line (0-3 seconds).
            2. Visual Cues: Instructions on what should be shown on the green screen.
            3. The Body: Fast-paced delivery of the information.
            4. Call to Action: Ask a specific question to drive comments.
            5. SEO: Provide the 5 best hashtags for the TikTok algorithm.
            """
            with st.spinner("Drafting script..."):
                try:
                    script_response = model.generate_content(prompt)
                    st.write(script_response.text)
                except Exception as e:
                    st.error(f"Error generating script: {e}")

        # -- MODULE B: LIMITLESS IMAGE GENERATION --
        if want_images:
            st.subheader("🎨 Green Screen / B-Roll Assets")
            img_prompt = f"High quality digital art of {topic}. Vibrant pop culture style, visually striking, highly detailed."
            with st.spinner("Generating visuals via Pollinations..."):
                image_url = generate_image_url(img_prompt)
                st.image(image_url, caption=f"Generated asset for: {keyword}")

        # -- MODULE C: VIDEO STORYBOARD --
        if want_storyboard:
            st.subheader("🎬 Video Production Storyboard")
            sb_prompt = f"Create a shot-by-shot video storyboard for a highly engaging short-form video about {topic}. Detail the exact camera angles, text-on-screen (pop-ups), and sound effects for each 3-second segment to maximize viewer retention."
            with st.spinner("Mapping out video shots..."):
                try:
                    sb_response = model.generate_content(sb_prompt)
                    st.write(sb_response.text)
                except Exception as e:
                    st.error(f"Error generating storyboard: {e}")
