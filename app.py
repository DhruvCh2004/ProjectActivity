import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from datetime import datetime

# Configure API key
genai.configure(api_key="AIzaSyBK3x0R654IECXjjk7GFsdjGRmozjCxtiA")  # Replace with your Gemini API key

# Initialize model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Save messages to CSV
def save_message(user_input, emotion, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[timestamp, user_input, emotion, response]], columns=["timestamp", "user_input", "emotion", "response"])
    if os.path.exists("chat_data.csv"):
        existing = pd.read_csv("chat_data.csv")
        updated = pd.concat([existing, new_row], ignore_index=True)
    else:
        updated = new_row
    updated.to_csv("chat_data.csv", index=False)

# Streamlit UI
st.set_page_config(page_title="Emotion Detection Chat", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #111827;
        }
        .user-message {
            background-color: #d1fae5;
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 60%;
            margin: 10px 0 10px auto;
            font-size: 16px;
        }
        .bot-message {
            background-color: white;
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 60%;
            margin: 10px auto 10px 0;
            font-size: 16px;
            border: 1px solid #ccc;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Emotion Detection & Support Chat")
user_input = st.text_input("How are you feeling today?")

if user_input:
    # Detect emotion with Gemini
    emotion_prompt = f"Identify the dominant emotion in the following message: '{user_input}'. Just return the single-word emotion."
    emotion_response = model.generate_content(emotion_prompt)
    dominant_emotion = emotion_response.text.strip().lower()

    # Generate personalized supportive response
    response_prompt = f"The user is feeling {dominant_emotion}. Their message is: '{user_input}'. Give a compassionate, empathetic response tailored to their message."
    response = model.generate_content(response_prompt)
    bot_reply = response.text.strip()

    # Display messages
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="bot-message">
            <strong>**Emotion:**</strong> {dominant_emotion}<br>
            <strong>Response:</strong> {bot_reply} 💙❤️
        </div>
    """, unsafe_allow_html=True)

    # Save to CSV
    save_message(user_input, dominant_emotion, bot_reply)

