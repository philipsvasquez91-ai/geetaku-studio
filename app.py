import streamlit as st
import google.generativeai as genai
import urllib.parse
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GeeTaku-San Studio", layout="centered", page_icon="⛩️")

# Pull keys from the secure vault
try:
    G_KEY = st.secrets["GEMINI_API_KEY"]
    P_KEY = st.secrets["POLLINATIONS_API_KEY"]
    genai.configure(api_key=G_KEY)
    
    # 2026 Stable Model: Gemini 3.1 Flash
    model = genai.GenerativeModel('gemini-3.1-flash-preview')
except Exception as e:
    st.error("⚠️ API Keys Missing! Please add 'GEMINI_API_KEY' and 'POLLINATIONS_API_KEY' to Streamlit Secrets.")

# --- 2. THE ENGINE FUNCTIONS ---
def generate_image_url(prompt):
    """Generates a high-quality image via Pollinations 2026 Engine"""
    # Clean the prompt for the web
    clean_prompt = urllib.parse.quote(prompt)
    # The new 2026 verified endpoint
    return f"https://gen.pollinations.ai/image/{clean_prompt}?key={P_KEY}&width=1024&height=1024&nologo=true"

# --- 3. THE INTERFACE ---
st.title("⛩️ GeeTaku-San Content Studio")
st.markdown("#### The All-in-One Engine for Anime, Wrestling & Pop Culture")

with st.container():
    topic = st.text_input("What's trending?", placeholder="e.g. Gear 5 Luffy, Cody Rhodes news, MCU rumors...")
    uploaded_file = st.file_uploader("Optional: Drop an article or notes (.txt)", type=['txt'])

st.sidebar.header("Studio Controls")
do_script = st.sidebar.checkbox("📝 TikTok Script", value=True)
do_image = st.sidebar.checkbox("🎨 Green Screen Asset", value=True)
do_story = st.sidebar.checkbox("🎬 Production Storyboard", value=False)

# --- 4. THE MAGIC BUTTON ---
if st.button("🚀 Create Content"):
    if not topic and not uploaded_file:
        st.warning("Enter a topic first!")
    else:
        # Process input
        final_topic = topic
        if uploaded_file:
            final_topic += " [Context: " + uploaded_file.getvalue().decode("utf-8")[:1000] + "]"
        
        st.info(f"Generating assets for: {topic}...")

        # -- MODULE A: VIRAL SCRIPT --
        if do_script:
            st.subheader("📝 Viral TikTok Script")
            prompt = f"""
            Act as the head strategist for the 'GeeTaku-San' TikTok. 
            Topic: {final_topic}
            Write a 60s script with:
            1. AGGRESSIVE HOOK (0-3s)
            2. VISUAL CUES for green screen
            3. HIGH-ENERGY BODY CONTENT (Pop culture/Anime/Wrestling focus)
            4. COMMENT-BASED CTA
            5. TOP 5 VIRAL HASHTAGS
            """
            with st.spinner("Writing script..."):
                try:
                    response = model.generate_content(prompt)
                    st.success("Script Ready!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Script Error: {e}")

        # -- MODULE B: LIMITLESS IMAGE --
        if do_image:
            st.subheader("🎨 Custom Visual Asset")
            with st.spinner("Painting your background..."):
                img_prompt = f"Vibrant anime and pro-wrestling aesthetic digital art of {topic}, cinematic lighting, 4k, trending on artstation."
                url = generate_image_url(img_prompt)
                # Show the image
                st.image(url, caption=f"GeeTaku-San Exclusive Asset: {topic}")
                st.caption(f"[Download link]({url})")

        # -- MODULE C: STORYBOARD --
        if do_story:
            st.subheader("🎬 Video Storyboard")
            with st.spinner("Directing shots..."):
                try:
                    sb_response = model.generate_content(f"Create a 5-shot visual storyboard for a viral video about {topic}")
                    st.markdown(sb_response.text)
                except:
                    st.error("Storyboard failed. Try again.")
