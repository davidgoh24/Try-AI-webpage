import os
import json
import streamlit as st
from groq import Groq


# _streamlit page configuration
st.set_page_config(
    page_title = "Chatbot",
    page_icon = "🤖",
    layout = "centered"
)


# Add custom CSS for background image
background_image_url = "https://hips.hearstapps.com/wdy.h-cdn.co/assets/17/39/1600x1066/gallery-1506709524-cola-0247.jpg?resize=1200:*"  # Replace with your image URL

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_image_url});
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# loading config.json file
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROA_API_KEY"]

# save the api key to environment variable
os.environ['GROQ_API_KEY'] = GROQ_API_KEY

# initate the groq client
client = Groq()

# building userinterface
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# create a page title / streamlit page title
st.markdown("<h1 style='text-align: center;'>🤖David's Aibot</h1>", unsafe_allow_html=True)

# display chat history using for loop
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):  # will show either the user or AI
        st.markdown(message["content"])

# input field for user's message
user_prompt = st.chat_input("Ask ChatAI...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to AI and get response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display AI's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
