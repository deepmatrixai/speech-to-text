import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from io import BytesIO

# Load environment variables
load_dotenv()

# Set up page configuration
st.set_page_config(page_title="Text-to-Speech App", layout="wide")

# Background image
page_bg_img = '''
<style>
.stApp {
    background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("https://imageio.forbes.com/specials-images/imageserve/6271151bcd7b0b7ffd1fa4e2/Artificial-intelligence-robot/960x0.jpg");
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# App title
st.title("Text-to-Speech App")

# Check if the API key is already stored in session_state
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

# Sidebar for API key input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state["openai_api_key"])

# Update session_state with the entered API key
if openai_api_key:
    st.session_state["openai_api_key"] = openai_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Main area for text input
user_input = st.text_area("Enter your text here:", height=150)

# Text to append at the end of user input
default_text = " Please follow for more and hit a like button."

# Voice selection dropdown
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
selected_voice = st.selectbox("Select a voice:", voices)

# Button to generate speech
if st.button("Generate Speech"):
    if not st.session_state["openai_api_key"]:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_input:
        st.error("Please enter some text to convert to speech.")
    else:
        # Append the default text to the user input
        final_input = user_input.strip() + default_text
        
        try:
            client = OpenAI(api_key=st.session_state["openai_api_key"])
            audio = client.audio.speech.create(
                model="tts-1-hd",
                voice=selected_voice,
                input=final_input
            )
            
            # Save audio to a file
            audio_path = "output.mp3"
            audio.stream_to_file(audio_path)
            
            # Display audio player
            st.audio(audio_path)
            
            # Provide download link for the generated speech
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="Download Speech",
                    data=file,
                    file_name="output.mp3",
                    mime="audio/mpeg"
                )
            
            st.success("Speech generated and ready for download!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# This is without the background image and by default openai api key is set to the .env file
# import streamlit as st
# import pandas as pd
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# from io import BytesIO

# # Load environment variables
# load_dotenv()

# # Set up page configuration
# st.set_page_config(page_title="Text-to-Speech App", layout="wide")

# # App title
# st.title("Text-to-Speech App")

# # Load OpenAI API key from .env file
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     st.error("OpenAI API Key not found. Please make sure you have a .env file with the OPENAI_API_KEY variable set.")
# else:
#     os.environ["OPENAI_API_KEY"] = openai_api_key

# # Main area for text input
# user_input = st.text_area("Enter your text here:", height=150)

# # Button to generate speech
# if st.button("Generate Speech"):
#     if not user_input:
#         st.error("Please enter some text to convert to speech.")
#     else:
#         try:
#             client = OpenAI(api_key=openai_api_key)
#             audio = client.audio.speech.create(
#                 model="tts-1",
#                 voice="echo",
#                 input=user_input
#             )
            
#             # Save audio to a file
#             audio_path = "output.mp3"
#             audio.stream_to_file(audio_path)
            
#             # Display audio player
#             st.audio(audio_path)
            
#             # Provide download link for the generated speech
#             with open(audio_path, "rb") as file:
#                 st.download_button(
#                     label="Download Speech",
#                     data=file,
#                     file_name="output.mp3",
#                     mime="audio/mpeg"
#                 )
            
#             st.success("Speech generated and ready for download!")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")

# # Instructions
# st.markdown("""
# ### How to use:
# 1. Make sure your OpenAI API key is saved in a `.env` file.
# 2. Type or paste your text in the text area above.
# 3. Click the 'Generate Speech' button to convert your text to speech.
# 4. Listen to the generated audio using the player that appears.
# 5. Download the audio file using the 'Download Speech' button.
# """)
