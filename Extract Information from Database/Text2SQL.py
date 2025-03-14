from dotenv import load_dotenv
load_dotenv() # loading all the environment vairables from .env file 
import google.generativeai as genai
import streamlit as st
import os
import sqlite3
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel('gemini-1.5-flash-8b-exp-0924')
prompt=[
"""
You are an expert in converting english question to SQL query!
The SQL database has the name STUDENT and has the following columns NAME,CLASS,SECTION,MARKS
For example
Example 1- How many entries of records are present? The SQL command will be something SELECT COUNT(*) FROM STUDENT;
Example 2- Tell me all the students studying in 10th class? The SQL command will be something SELECT * FROM STUDENT where CLASS='10th';

Also sql query should not have ``` in the begining the and the end and sql word in the output



"""
]
def get_response(query,prompts):
    message=prompts[0] +' '+query
    
    response=model.generate_content(message)
    return response._result.candidates[0].content.parts[0].text
def read_sql_query(sql_query,database):
    connection=sqlite3.connect(database)
    cursor=connection.cursor()
    cursor.execute(sql_query)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    for row in rows: 
        print(row)
    return rows    

    
st.set_page_config(page_title='Text to SQL',page_icon='📲')
st.title('Fetch from the SQL database')
query=st.text_input('Write Query: ', key='input')
submit=st.button('Ask the question')

if submit:
    response=get_response(query, prompt)
    print(response)
    data=read_sql_query(response,'Student.db')
    st.subheader('Generated Response')
    for row in data:
        st.write(row)
    