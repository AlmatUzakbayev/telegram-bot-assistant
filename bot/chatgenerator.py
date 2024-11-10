import os
import pathlib
from bot.constants import TEXT_PROMPT, VOICE_PROMPT, IMAGE_PROMPT

from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from bot.config import GOOGLE_API_KEY

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def clean_text(text: str) -> str:
    return text.replace("**", "").replace("\n", " ").replace("*", "")


def voice_ask(file_name: str) -> str:
    # Create the prompt.
    prompt = VOICE_PROMPT

    model = genai.GenerativeModel("gemini-1.5-flash")
    # Load the samplesmall.mp3 file into a Python Blob object containing the audio
    # file's bytes and then pass the prompt and the audio to Gemini.
    response = model.generate_content([
        prompt,
        {
            "mime_type": "audio/ogg",
            "data": pathlib.Path(file_name).read_bytes()
        }
    ])

    # Output Gemini's response to the prompt and the inline audio.
    print(response.text)
    return response.text


def ask(user_text):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    messages = [
        (
            "system",
            TEXT_PROMPT,
        ),
        ("human", user_text),
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg.content)
    return clean_text(ai_msg.content)

def image_ask(file_name: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    myfile = genai.upload_file(file_name)
    result = model.generate_content(
        [myfile, "\n\n", IMAGE_PROMPT]
    )
    return clean_text(result.text)