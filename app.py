import streamlit as st
from PIL import Image
from openai import OpenAI
from gtts import gTTS
import os

# App Configuration
st.set_page_config(page_title="Maraman.ai", layout="centered")
st.title("🩺 Maraman.ai - Your Friendly AI Explainer")

st.write("Upload a medical image, X-ray, or prescription. I’ll explain it simply and speak like a human.")

# Image Upload
image_file = st.file_uploader("📤 Upload Image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if image_file:
    # Display Uploaded Image
    image = Image.open(image_file)
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    st.info("⏳ Analyzing the image...")

    # Step 1: Fake AI-generated caption (placeholder for real image analysis)
    fake_caption = "This X-ray shows a possible mild infection in the lungs."

    # Step 2: Generate Explanation using OpenAI (new SDK syntax)
    client = OpenAI(api_key=st.secrets["openai_api_key"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a kind doctor who explains things like a friend."},
            {"role": "user", "content": f"Explain this to a patient in simple terms: {fake_caption}"}
        ]
    )

    answer = response.choices[0].message.content
    st.success("💬 Explanation:")
    st.write(answer)

    # Step 3: Text-to-Speech
    tts = gTTS(answer)
    audio_path = "voice.mp3"
    tts.save(audio_path)
    st.audio(audio_path)
