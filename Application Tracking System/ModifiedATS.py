from dotenv import load_dotenv
import streamlit as st 
import google.generativeai as genai 
import PyPDF2 as pdf
import os 
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel('gemini-2.0-flash-exp')
def get_response(input,prompt,job_description):
    response=model.generate_content([prompt,job_description,input])
    return response._result.candidates[0].content.parts[0].text
def pdf_to_pages_to_text(pdf_file):
    reader=pdf.PdfReader(pdf_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
 
    return text

input_prompt="""
Hey Act like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field, software 
engineer, Your task is to evaluate the resume based on the given job description, you must consider the job market is very competitive 
and you should provide best assistance for improving the resumes. Assign the percentage matching based on Jd and the missing keywords with high accuracy

I want only this in my response 
"JD Match":"%",
"MissingKeywords:[]",
"Profile Summary":""
"""

st.set_page_config(page_title="ImprovedATS",page_icon='🤖')
st.title('Smart ATS 🤖')
st.text('Improve Your resume ATS')
jd=st.text_area('Paste the Job Description')
uploaded_file=st.file_uploader("Upload your resume",type="pdf",help="Please Upload your resume")
submit= st.button('Submit')
if submit:
    if uploaded_file is not None: 
        text=pdf_to_pages_to_text(uploaded_file)
        response=get_response(text,input_prompt,jd)
        st.subheader('Generated Response')
        st.write(response)
    
