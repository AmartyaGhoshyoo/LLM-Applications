from dotenv import load_dotenv
import google.generativeai as genai
import os 
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model= genai.GenerativeModel('gemini-2.0-flash-exp')
prompt="""You are Youtube video summarizer, You will be taking the transcript text and summarizing the entire video
and providing the important summary in points within 250 words, Give me the summary of this   """
def generate_gemini_content(transcript_text):
    response=model.generate_content(prompt+transcript_text)
    return response._result.candidates[0].content.parts[0].text
def generate_text_from_youtube(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text: 
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e 
        
st.set_page_config(page_title='YouTube',page_icon='🤖')
st.title('YouTube Transcript to Detailed Notes Converter')
input=st.text_input('Enter YouTube video link: ')
if input:
    video_id = input.split("v=")[1].split("&list")[0]
    print(video_id) 
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")
    
if st.button('Get detailed Notes'):
    transcript=generate_text_from_youtube(input)
    if transcript:
        summary=generate_gemini_content(transcript)
        st.markdown('Notes')
        st.write(summary)