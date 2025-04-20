import streamlit as st
from PIL import Image
import openai
from gtts import gTTS
import os

# Page settings
st.set_page_config(page_title="Maraman.ai", layout="centered")
st.title("Maraman.ai - Your Friendly AI Explainer")

st.write("Upload a medical image, X-ray, or prescription. I’ll explain it simply and speak like a human.")

# Upload file
image_file = st.file_uploader("Upload Image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if image_file:
    # Show image
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.info("Analyzing the image...")

    # Step 1: Temporary fake caption (later we add image analysis)
    fake_caption = "This X-ray shows a possible mild infection in the lungs."

    # Step 2: Use OpenAI to explain the issue in friendly words
    openai.api_key = st.secrets["openai_api_key"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a kind doctor who explains things like a friend."},
            {"role": "user", "content": f"Explain to a patient: {fake_caption}"}
        ]
    )

    answer = response.choices[0].message.content
    st.success("Explanation:")
    st.write(answer)

    # Step 3: Convert text to speech
    tts = gTTS(answer)
    tts.save("voice.mp3")
    st.audio("voice.mp3")
