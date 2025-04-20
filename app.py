import streamlit as st
from openai import OpenAI  # ✅ New OpenAI SDK import
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from gtts import gTTS
import os

# Streamlit page config
st.set_page_config(page_title="Maraman.ai", layout="centered")
st.title("Maraman.ai - Your Friendly Digital Friend")
st.write("Upload an image or PDF. I will explain it simply and talk to you like a friend.")

# Initialize OpenAI client with key from secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])  # ✅ updated access

# File uploader
uploaded_file = st.file_uploader("Upload Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_type = uploaded_file.type
    content_text = ""

    if "pdf" in file_type:
        st.info("📄 Reading PDF...")
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            content_text += page.extract_text()
    else:
        st.info("🖼️ Reading Image...")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        content_text = pytesseract.image_to_string(image)

    if content_text:
        st.success("🧠 Got the content. Asking Maraman to explain...")

        prompt = f"Explain this to a person in very simple and friendly way like a teacher or coach:\n\n{content_text}"

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a kind teacher who explains things like a friend."},
                    {"role": "user", "content": prompt}
                ]
            )

            explanation = response.choices[0].message.content
            st.success("💬 Explanation:")
            st.write(explanation)

            # Convert to audio
            tts = gTTS(explanation)
            tts.save("output.mp3")
            st.audio("output.mp3")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("🚫 Could not extract any text. Please try another file.")
