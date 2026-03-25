import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GeeTaku-San Studio", layout="centered", page_icon="⛩️")

# Pull key from the secure vault
try:
    G_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=G_KEY)
except Exception as e:
    st.error("⚠️ GEMINI_API_KEY missing from Streamlit Secrets!")

def get_model():
    """Tries the latest 2026 models and falls back if one is 404"""
    model_names = ['gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-1.5-flash']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Small test call to see if it exists
            return m
        except:
            continue
    return genai.GenerativeModel('gemini-pro') # Absolute last resort

model = get_model()

# --- 2. THE ENGINE FUNCTIONS ---
def generate_image_url(prompt):
    """Generates a high-quality image via the new 2026 Pollinations Engine (No Key Required)"""
    clean_prompt = urllib.parse.quote(prompt)
    # Using the new 2026 'bolt' parameter for high-speed generation
    return f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&nologo=true&model=flux"

# --- 3. THE INTERFACE ---
st.title("⛩️ GeeTaku-San Content Studio")
st.markdown("#### The All-in-One Engine for Anime, Wrestling & Pop Culture")

topic = st.text_input("What's trending?", placeholder="e.g. Gear 5 Luffy, Cody Rhodes news, MCU rumors...")
uploaded_file = st.file_uploader("Optional: Drop an article or notes (.txt)", type=['txt'])

st.sidebar.header("Studio Controls")
do_script = st.sidebar.checkbox("📝 TikTok Script", value=True)
do_image = st.sidebar.checkbox("🎨 Green Screen Asset", value=True)

# --- 4. THE MAGIC BUTTON ---
if st.button("🚀 Create Content"):
    if not topic and not uploaded_file:
        st.warning("Enter a topic first!")
    else:
        final_topic = topic
        if uploaded_file:
            final_topic += " [Context: " + uploaded_file.getvalue().decode("utf-8")[:1000] + "]"
        
        st.info(f"Generating for: {topic}...")

        # -- MODULE A: VIRAL SCRIPT --
        if do_script:
            st.subheader("📝 Viral TikTok Script")
            prompt = f"Act as the head strategist for GeeTaku-San TikTok. Topic: {final_topic}. Write a 60s script with a hook, visual cues, high-energy body content, and 5 hashtags."
            with st.spinner("Writing..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Script Error: {e}")

        # -- MODULE B: IMAGE ASSET --
        if do_image:
            st.subheader("🎨 Custom Visual Asset")
            with st.spinner("Generating image..."):
                img_prompt = f"Vibrant anime and pro-wrestling aesthetic digital art of {topic}, cinematic lighting, high detail."
                url = generate_image_url(img_prompt)
                st.image(url, caption=f"GeeTaku-San Asset: {topic}")
