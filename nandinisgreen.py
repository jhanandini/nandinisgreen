import os
import streamlit as st

from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Local .env file se secret key load karna
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini Client setup
client = genai.Client(api_key=api_key)

# Web page ki styling aur title
st.set_page_config(page_title="nandinisgreen - Your Librarian", page_icon="📚")
st.title("nandinisgreen")
st.caption("Your personalized, friendly book recommender & literary connoisseur.")

# System Instructions
instructions = """
Your name is nandinisgreen. You are an authentic, smart, and friendly professional librarian.
Your superpower is understanding the user's mood and suggesting the perfect books.
CRITICAL RULE: Never use overly formal, poetic, or pure/heavy Shuddh Hindi/Urdu. 
Speak exactly like a supportive, helpful peer or friend—using a mix of casual Hindi, English, and Hinglish. Keep your tone adaptive, insightful, clear, and slightly witty.
Give 2-3 amazing book recommendations based on the user's mood, and briefly explain in a fun, conversational way why they should read it.
"""

# Chat history (memory) ko maintain karne ke liye Streamlit ka session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages ko screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ka input (Chat Box)
if user_input := st.chat_input("Tell me your mood or what kind of book you want to read..."):
    
    # 1. User ka message screen par dikhao aur save karo
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Gemini se response lena
    with st.chat_message("assistant", avatar="📚"):
        response_placeholder = st.empty()
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
                temperature=0.8,
            )
        )
        
        # 3. Response ko screen par dikhao aur save karo
        ai_response = response.text
        response_placeholder.markdown(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})