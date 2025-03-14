# Chat with history
from dotenv import load_dotenv
load_dotenv()
import os 
import google.generativeai as genai
import streamlit as st 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel('gemini-1.5-flash-8b-exp-0924')
chat=model.start_chat(history=[]) # it will store all the chat history we interact with the model and the chat itself is actually the copy of the model.start_chat method 

def gemini_ai_response(question):
    response=chat.send_message(question) # LLM model gives you the response so stream equal True we don't need to wait for the entire content, in chunks we would be getting
    return response

st.set_page_config(page_title='Chat History ©',page_icon='💬')
st.title('Custom ChatBot with Chat History🗣️')
if 'chat_history' not in st.session_state:  #Starting session 
    st.session_state['chat_history']=[] # will execute just once to initialise this in dictionary , beacuse at the very begining we don't have such key value pair in this st.session_state dict, (chat_history)=key and value is array

input=st.text_input('Write Query: ', key='input')
inputs=input # So we don't want to append the whole input with the with previous chat in the char_history , beacuse we needed the previous chat only for the query, but if we append input then there will be repetition like the chat history will again merged in appended which is not a good solution token exausting 
submit=st.button('Ask Question')
new=''
for role,text in st.session_state['chat_history']:
    new+=f'{text} ' # ignoring the role , it will take all the history
input=new+'\n'+input
if submit and input:
    response=gemini_ai_response(input) # we are feeding with history
    # for appending do not append the input , because input itself containing all the history , so if we append again , it is totally redundant, from the next the same history will be repeated part by part and once merged again for the last input append whihc we don't want
    # but for seeing how it is taking the prompt you can put input instead of inputs in the below
    st.session_state['chat_history'].append(('You',inputs)) # appends in array or list so we can't append two items, we can one element ('You',input) at a time  , we just append the new query=inputs not the whole 'input' beacuse it will append the merged the result of all the chat history we don't want that ,the input itself already taken the previous chat we needed for the prompt 
    st.subheader('Generated Response')
    st.write(response._result.candidates[0].content.parts[0].text)
    st.session_state['chat_history'].append(('Bot',response._result.candidates[0].content.parts[0].text))
    # for chunk in response: 
    #     st.write(chunk.text)
    #     st.session_state['chat_history'].append(('Bot',chunk.text))

st.subheader('The Chat History ')
for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
    
    
