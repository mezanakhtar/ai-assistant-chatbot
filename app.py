import time
import streamlit as st
from datetime import datetime
from chatbot import get_response

# Custom CSS Styling
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00FFAA;
}

.stChatInput input {
    border-radius: 10px;
    border: 2px solid #00FFAA;
}

.stButton button {
    border-radius: 10px;
    background-color: #00FFAA;
    color: black;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.title("AI Assistant")

    st.write("Built using NLP & Machine Learning")
    st.caption(
         "AI, ML, Career Guidance & Study Assistant"
    )

    st.write("⚡ Python")
    st.write("⚡ NLTK")
    st.write("⚡ TF-IDF")
    st.write("⚡ Streamlit")

    st.divider()

    # Export chat
    chat_text = ""

    for msg in st.session_state.messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        chat_text += f"{role}: {content}\n"

    st.download_button(
        label="📥 Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(
        "Developed by Mezan Akhtar"
        )
    st.caption("AI Engineer Aspirant")
    
st.metric(
    "Knowledge Intents",
    "15+"
)
    

if len(st.session_state.messages) == 0:
        st.info(
            "👋 Welcome to AI Assistant! Try asking: • What is AI? • What is Machine Learning? • Resume Tips • How to become an AI Engineer? • Motivate me"
        )        

# Display chat history
for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div style="
                background-color:#1E293B;
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
                text-align:right;
                color:white;
            ">
            👨 {msg["content"]}

            <br>
            <small style="color:gray;">{msg["time"]}</small>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="
                background-color:#262730;
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
                text-align:left;
                color:white;
            ">
            🤖 {msg["content"]}
            
            <br>
            <small style="color:gray;">{msg["time"]}</small>

            </div>
            """,
            unsafe_allow_html=True
        )

# User input
user_input = st.chat_input("Ask me about AI, ML, Python, Careers...")

if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%I:%M %p")
        }
    )

    # Animated typing dots
    typing_placeholder = st.empty()

    for i in range(3):
        typing_placeholder.markdown(
            f"🤖 Typing{'.' * (i + 1)}"
        )
        time.sleep(0.3)

    # Generate chatbot response
    response = get_response(str(user_input))

    typing_placeholder.empty()

    # Typing animation
    full_response = ""
    response_placeholder = st.empty()

    for word in response.split():
        full_response += word + " "
        time.sleep(0.05)

        response_placeholder.markdown(
            f"""
            <div style='
                background-color:#262730;
                padding:12px;
                border-radius:10px;
                color:white;
                margin-bottom:10px;
            '>
            🤖 {full_response}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "time": datetime.now().strftime("%I:%M %p")
        }
    )

    st.rerun()