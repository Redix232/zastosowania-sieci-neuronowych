import streamlit as st
from openai import OpenAI
import os

st.set_page_config(layout="wide", page_title="OpenRouter chatbot app")
st.title("OpenRouter chatbot app")

# api_key, base_url = os.environ["API_KEY"], os.environ["BASE_URL"]
api_key, base_url = st.secrets["API_KEY"], st.secrets["BASE_URL"]

FREE_MODELS = {
    "Gemma 3 1B (Google)": "google/gemma-3-1b-it:free",
    "Gemma 3 4B (Google)": "google/gemma-3-4b-it:free",
    "Mistral 7B Instruct": "mistralai/mistral-7b-instruct:free",
    "Llama 3.2 3B Instruct (Meta)": "meta-llama/llama-3.2-3b-instruct:free",
    "Phi-3 Mini 128k Instruct (Microsoft)": "microsoft/phi-3-mini-128k-instruct:free",
}

with st.sidebar:
    st.header("Model settings")
    model_label = st.selectbox("Open-source model", list(FREE_MODELS.keys()))

selected_model = FREE_MODELS[model_label]

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.info("Invalid API key.")
        st.stop()
    client = OpenAI(api_key=api_key, base_url=base_url)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model=selected_model,
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)