import os
import streamlit as st

from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load the secret API key from the local .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# Configure web page styling and title
st.set_page_config(page_title="nandinisgreen - Your Librarian", page_icon="📚")
st.title("nandinisgreen")
st.caption("Your personalized, friendly book recommender & literary connoisseur.")

# System Instructions for the AI persona
instructions = """
Your name is nandinisgreen. You are an authentic, smart, and friendly professional librarian.
Your superpower is understanding the user's mood and suggesting the perfect books.
CRITICAL RULE: Never use overly formal, poetic, or pure/heavy Shuddh Hindi/Urdu. 
Speak exactly like a supportive, helpful peer or friend—using a mix of casual Hindi, English, and Hinglish. Keep your tone adaptive, insightful, clear, and slightly witty.
Give 2-3 amazing book recommendations based on the user's mood, and briefly explain in a fun, conversational way why they should read it.
"""

# Initialize Streamlit session state to maintain chat history (memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box for the user
if user_input := st.chat_input("Tell me your mood or what kind of book you want to read..."):
    
    # 1. Display the user's message on the screen and save it to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Fetch the response from the Gemini model
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
        
        # 3. Display the AI response on the screen and save it to history
        ai_response = response.text
        response_placeholder.markdown(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})