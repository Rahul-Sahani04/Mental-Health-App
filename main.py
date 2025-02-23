import streamlit as st
import os
from google import genai
from google.genai import types
from pydub import AudioSegment
import tempfile
from dotenv import load_dotenv
from st_audiorec import st_audiorec

# Load the environment variables
load_dotenv()

# Configure the Google Generative AI
client = genai.Client(api_key=os.environ["GENAI_API_KEY"])

config = types.GenerateContentConfig(
    temperature=0,
    top_p=0.95,
    top_k=20,
    system_instruction="""
        Objective: Provide empathetic and supportive interactions to help users manage anxiety and improve their mental well-being.

        Instructions:

        Greeting and Initial Support:

        Start the conversation by greeting the user warmly and asking how they are feeling.
        Example: "Hello! I'm here to support you. How are you feeling today?"
        
        Keep your responses empathetic and supportive to create a safe space for the user.
        Keep them concise and easy to understand. Avoid using jargon or complex language.
        To the point responses are more effective in providing support.
        Short and clear responses are more effective in providing support.
        
        Responding to Anxiety:

        If the user expresses feelings of anxiety, acknowledge their feelings and offer a quick breathing exercise.
        Example: "I'm sorry to hear that. Anxiety can be challenging. Let's try a quick breathing exercise together. Are you ready?"
        Guiding Breathing Exercise:

        Provide clear instructions for the breathing exercise.
        Example: "Great! Let's take a deep breath in through your nose, hold it for a few seconds, and then exhale slowly through your mouth. Repeat this a few times."
        Offering Affirmations:

        After the breathing exercise, offer an affirmation to boost the user's mood.
        Example: "You're welcome! Remember, it's okay to feel anxious, and there are many techniques to manage it. Would you like to hear an affirmation to boost your mood?"
        Providing Affirmations:

        Share a positive affirmation and encourage the user to repeat it.
        Example: "Here's one for you: 'I am strong and capable of overcoming any challenge.' Repeat it to yourself a few times."
        Closing the Session:

        End the conversation by reassuring the user of your availability for future support.
        Example: "I'm glad to hear that! If you ever need more support or just someone to talk to, I'm here for you. Take care!"
        Additional Guidelines:

        Maintain a calm and reassuring tone throughout the conversation.
        Be empathetic and non-judgmental in your responses.
        Encourage the user to seek professional help if their anxiety is severe or persistent.
    """,
)


# Function to upload files to Gemini
def upload_to_gemini(path, mime_type=None):
    file = client.files.upload(file=path)
    return file


# Create a chat session
chat = client.chats.create(model="gemini-2.0-flash")


# Streamlit UI
st.title("Mental Health Support App")
st.write("Welcome to the Mental Health Support App!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Audio Recording
st.write("Talk with mic:")
audio_bytes = st_audiorec()

if audio_bytes:
    # Save the uploaded audio file temporarily
    temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    with open(temp_audio_path, "wb") as temp_audio_file:
        temp_audio_file.write(audio_bytes)

    # Upload the audio file to Gemini
    audio_file_gemini = upload_to_gemini(temp_audio_path, mime_type="audio/wav")

    # Send the audio file to the chat session
    response = chat.send_message(message=["audio", audio_file_gemini], config=config)
    st.session_state.chat_history.append(("User", "Audio Message"))
    if response.text:
        st.session_state.chat_history.append(("AI", response.text))
    else:
        st.session_state.chat_history.append(("AI", "Could not process the audio message."))    


# Display chat history
# Display chat history in a container

# Chatbot Interaction
st.subheader("Chat with AI")
user_input = st.text_input("You:", "", help="Type your message here.")

if user_input:
    # response = chat.send_message(message=user_input, config=config)
    chat_history = [m[1] for m in st.session_state.chat_history]  # Extract only messages
    chat_history.append(user_input)  # Append latest message
    response = chat.send_message(message=chat_history, config=config)
    st.session_state.chat_history.append(("User", user_input))
    if response.text:
        st.session_state.chat_history.append(("AI", response.text))
    else:
        st.session_state.chat_history.append(("AI", "Could not process the message."))

    


st.subheader("Chat History")
chat_container = st.container(border=10)
with chat_container:
    for speaker, text in st.session_state.chat_history:
        if speaker == "User":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**AI:** {text}")


# Sidebar for Affirmations & Mantras
st.sidebar.header("Affirmations & Mantras")
affirmations = [
    "I am worthy of love and happiness.",
    "I am strong and capable.",
    "I embrace change and growth.",
]
st.sidebar.text_area("Today's Affirmation:", affirmations[0], height=70)

# Sidebar for Personalized Suggestions
st.sidebar.header("Personalized Suggestions")
# Placeholder for ML-based recommendations
st.sidebar.write("Based on your input, here are some suggestions:")
st.sidebar.write("- Practice mindfulness for 5 minutes.")
st.sidebar.write("- Engage in a hobby you enjoy.")

# Sidebar for Instant Relief Section
st.sidebar.header("Instant Relief")
st.sidebar.write("Try these techniques to calm down:")
st.sidebar.write("- Breathing Exercises")
st.sidebar.write("- Listen to calming music")

# Run the app
# if __name__ == "__main__":
#     st.write("Welcome to the Mental Health Support App!")
