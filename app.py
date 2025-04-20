import streamlit as st
from PIL import Image
import openai
from gtts import gTTS

st.set_page_config(page_title="Maraman.ai", layout="centered")
st.title("Maraman.ai - Friendly AI Explainer")

st.write("Upload a medical image, X-ray, or prescription. I’ll explain and speak like a human.")

image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Step 1: Dummy caption for now
    fake_caption = "Chest X-ray showing mild lung infection."

    # Step 2: Use OpenAI to explain
    openai.api_key = st.secrets["openai_api_key"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful doctor who explains things simply."},
            {"role": "user", "content": f"Explain this to a patient: {fake_caption}"}
        ]
    )
    answer = response.choices[0].message.content
    st.success(answer)

    # Step 3: Convert to speech
    tts = gTTS(answer)
    tts.save("voice.mp3")
    st.audio("voice.mp3")
