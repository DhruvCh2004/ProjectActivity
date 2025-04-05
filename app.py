# 🔹 Non-Streamlit imports
from transformers import pipeline
import torch

# 🔹 First Streamlit import
import streamlit as st

# ✅ Page config MUST be right after importing streamlit and before any other Streamlit commands
st.set_page_config(page_title="Emotion Detector", layout="centered")

# Title and UI
st.title("AI-Based Emotion Detection")

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="cirimus/modernbert-base-go-emotions", top_k=None)

classifier = load_model()

text = st.text_area("Enter some text to analyze emotions:")

if st.button("Detect Emotion") and text:
    predictions = classifier(text)
    for pred in predictions[0]:
        st.write(f"{pred['label']}: {round(pred['score']*100, 2)}%")


