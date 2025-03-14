# PDF to Text 
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
import streamlit as st 
from PIL import Image
from langchain.vectorstores import FAISS
import csv
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel('gemini-2.0-flash-exp')
def generate_text_from_image(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response._result.candidates[0].content.parts[0].text
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
st.set_page_config(page_title='Image_2_Text',page_icon='📲')
st.title('Convert your Image to Text 📲')
input=st.text_input("Write Query: ", key='input')
upload_file=st.file_uploader("Choose an image...",type=['jpg','jpeg','png'])
image=''
if upload_file is not None: 
    image=Image.open(upload_file)
    st.image(image,caption='Uploaded Image.',use_column_width=True)#  display the image in there
    
submit=st.button('Tell me about this image ')
input_prompt="""

You are an expert in understanding images. We will upload a image  and you will have to describe the image 

"""
if submit:
    image_data=input_image_setup(upload_file)
    response=generate_text_from_image(input_prompt,image_data,input)
    st.subheader('Generated Response ')
    st.write(response)
    



# st.header("Gemini Health App")
# input=st.text_input("Input Prompt: ",key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image=""   
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)


# submit=st.button("Tell me the total calories")

# input_prompt="""
# You are an expert in nutritionist where you need to see the food items from the image
#                and calculate the total calories, also provide the details of every food items with calories intake
#                is below format

#                1. Item 1 - no of calories
#                2. Item 2 - no of calories
#                ----
#                ----


# """

# ## If submit button is clicked

# if submit:
#     image_data=input_image_setup(uploaded_file)
#     response=get_gemini_repsonse(input_prompt,image_data,input)
#     st.subheader("The Response is")
#     st.write(response)
