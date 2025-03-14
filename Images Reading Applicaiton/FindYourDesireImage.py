from dotenv import load_dotenv
import google.generativeai as genai 
import streamlit as st
from PIL import Image
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import util

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

st.set_page_config(page_title='Image Searching', page_icon='🤖')

upload_files = st.sidebar.file_uploader('Upload Images....', accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
if upload_files:
    st.sidebar.write('Files uploaded successfully')

prompt = "You are an expert in describing the image, you will be provided an image you have to describe about the image."

def converting_to_embedding(text):
    embedding = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    return embedding.embed_query(text)

def convert_image_byte(upload_image):
    if upload_image:
        byte_stream = upload_image.getvalue()
        image_parts = [
            {
                "mime_type": upload_image.type,
                "data": byte_stream
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No file has been uploaded')

def generate_description(prompt, image):
    response = model.generate_content([prompt, image[0]])
    return response._result.candidates[0].content.parts[0].text

img_des = []
img_emb = []

if upload_files:
    for file in upload_files:
        image = convert_image_byte(file)
        response = generate_description(prompt, image)
        img_des.append(response)
        embeddings = converting_to_embedding(response)
        img_emb.append((file, embeddings))

st.title('Search Images with Query')
query = st.text_input('Write Description:', key='input')
# threshold = st.slider('Set Similarity Threshold', 0.0, 0.5, 1.0)

if query:
    query_embeddings = converting_to_embedding(query)
    similarities = [(upload_file, util.pytorch_cos_sim(query_embeddings, img_embeddings).item()) for upload_file, img_embeddings in img_emb]
    similarities.sort(key=lambda x: x[1], reverse=True)
    st.write('Relevant Images')
    # for upload_file, similarity in similarities:
    #     if similarity>=threshold:
    if similarities:
        image = Image.open(similarities[0][0])
        st.image(image, caption=f'{similarities[0][0].name}, (Similarity: {similarities[0][1]:.2f})')
        
        
#Balaghal Ula Bi Kamaalihi | Ali Zafar | Naat