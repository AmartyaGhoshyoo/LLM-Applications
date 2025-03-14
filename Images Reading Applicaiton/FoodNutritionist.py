from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os
load_dotenv()
from PIL import Image
genai.configure(api_key=os.getenv('GOOLE_API_KEY'))
model=genai.GenerativeModel('gemini-2.0-flash-exp')
def get_response(input,image,prompt):
    response=model.generate_content([prompt,image[0],input])
    return response._result.candidates[0].content.parts[0].text
# we are converting just because google gemini ai model accept in that way
def converting_the_image(image):
    if image is not None: 
        bytes_data=image.getvalue()
        image_part=[
            {
                'mime_type':image.type,
                'data':bytes_data
            }
        ] 
        return image_part
    else:
        raise FileNotFoundError('No File Uploaded')
st.set_page_config(page_title='FOOD',page_icon='🤖')
st.title('Have your diet chart📊')
input=st.text_input('Write Query',key='input')
upload_file=st.file_uploader('Upload The photo....',type=['png','jpg','jpeg']) 
image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(upload_file,caption='Uploaded Image ')
submit=st.button('Tell me the total calories')
input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
"""
if submit:
    image_data=converting_the_image(upload_file)
    response=get_response(input_prompt,image_data,input)
    st.subheader('Generated Response ')
    st.write(response)
